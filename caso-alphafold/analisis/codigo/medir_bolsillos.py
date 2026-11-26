"""Para cada complejo de PoseBusters: confianza de AlphaFold (pLDDT) en el bolsillo
y parecido del bolsillo del modelo con el experimental.

Bolsillo: residuos de la proteína con algún átomo pesado a menos de 6 Å del ligando
en la estructura experimental. Se superponen los Cα del bolsillo (modelo sobre
experimental) y se mide la RMSD de los Cα y de todos los átomos pesados comunes.
"""
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import gemmi
import numpy as np
import pandas as pd
import requests
from Bio import Align

BASE = Path(__file__).resolve().parent.parent
PB = BASE / "datos" / "pb" / "posebusters_benchmark_set"
CACHE = BASE / "datos" / "cache"
AF = BASE / "datos" / "alphafold"
CORTE = 6.0

sesion = requests.Session()


def get_json(url, ruta):
    if ruta.exists():
        return json.loads(ruta.read_text())
    for intento in range(6):
        r = sesion.get(url, timeout=60)
        if r.status_code == 404:
            ruta.write_text("null")
            return None
        if r.status_code == 429:
            time.sleep(5 * (intento + 1))
            continue
        if r.ok:
            ruta.write_text(r.text)
            return r.json()
        time.sleep(2 + 3 * intento)
    raise RuntimeError(f"{url}: {r.status_code}")


def ligando_xyz(sdf):
    lineas = sdf.read_text().splitlines()
    n = int(lineas[3][:3])
    xyz = []
    for l in lineas[4:4 + n]:
        if l[31:34].strip() != "H":
            xyz.append([float(l[0:10]), float(l[10:20]), float(l[20:30])])
    return np.array(xyz)


def tres_a_uno(nombre):
    return gemmi.find_tabulated_residue(nombre).one_letter_code.upper() if gemmi.find_tabulated_residue(nombre) else "X"


def residuos(cadena):
    return [r for r in cadena if gemmi.find_tabulated_residue(r.name) and gemmi.find_tabulated_residue(r.name).is_amino_acid() and r.find_atom("CA", "*")]


def alinear(a, b):
    al = Align.PairwiseAligner(mode="global", open_gap_score=-10, extend_gap_score=-0.5, match_score=1, mismatch_score=-1)
    aln = al.align(a, b)[0]
    mapa = {}
    for (s1, e1), (s2, e2) in zip(*aln.aligned):
        for k in range(e1 - s1):
            mapa[s1 + k] = s2 + k
    return mapa


def kabsch(P, Q):
    pc, qc = P.mean(0), Q.mean(0)
    H = (P - pc).T @ (Q - qc)
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, d]) @ U.T
    return lambda X: (X - pc) @ R.T + qc


def medir(ident):
    carpeta = PB / ident
    pdb_id = ident.split("_")[0].lower()
    fila = {"complejo": ident, "pdb": pdb_id.upper(), "ligando": ident.split("_")[1]}
    try:
        estructura = gemmi.read_structure(str(carpeta / f"{ident}_protein.pdb"))
        lig = ligando_xyz(carpeta / f"{ident}_ligand.sdf")
        modelo = estructura[0]
        # cadena con más residuos en el bolsillo
        mejor = None
        for cadena in modelo:
            res = residuos(cadena)
            bols = [i for i, r in enumerate(res)
                    if np.min(np.linalg.norm(np.array([a.pos.tolist() for a in r if a.element.name != "H"])[:, None] - lig[None], axis=2)) < CORTE]
            if mejor is None or len(bols) > len(mejor[2]):
                mejor = (cadena.name, res, bols)
        nombre_cadena, res, bols = mejor
        fila.update(cadena=nombre_cadena, n_bolsillo=len(bols))
        if len(bols) < 5:
            return {**fila, "estado": "bolsillo con menos de 5 residuos"}
        seq_exp = "".join(tres_a_uno(r.name) for r in res)

        mapeo = get_json(f"https://www.ebi.ac.uk/pdbe/api/mappings/uniprot/{pdb_id}", CACHE / f"sifts_{pdb_id}.json")
        candidatos = []
        for unp, info in (mapeo or {}).get(pdb_id, {}).get("UniProt", {}).items():
            for m in info["mappings"]:
                if m["chain_id"] == nombre_cadena:
                    candidatos.insert(0, unp)
                elif m["struct_asym_id"] == nombre_cadena:  # algunos archivos usan la etiqueta interna
                    candidatos.append(unp)
        if not candidatos:
            return {**fila, "estado": "sin UniProt para la cadena"}
        unp = candidatos[0]
        fila["uniprot"] = unp
        pred = get_json(f"https://alphafold.ebi.ac.uk/api/prediction/{unp}", CACHE / f"afapi_{unp}.json")
        if not pred:
            return {**fila, "estado": "sin modelo en AlphaFold DB"}
        p = pred[0]
        fila["af_version"] = p.get("latestVersion")
        ruta_af = AF / f"{p['modelEntityId']}.pdb"
        if not ruta_af.exists():
            for intento in range(6):  # AlphaFold DB limita la velocidad (429)
                r = sesion.get(p["pdbUrl"], timeout=120)
                if r.status_code != 429:
                    break
                time.sleep(5 * (intento + 1))
            r.raise_for_status()
            ruta_af.write_bytes(r.content)
        af = gemmi.read_structure(str(ruta_af))[0]
        res_af = residuos(af[0])
        seq_af = "".join(tres_a_uno(r.name) for r in res_af)
        mapa = alinear(seq_exp, seq_af)
        pares = [(res[i], res_af[mapa[i]]) for i in bols if i in mapa]
        iguales = sum(a.name == b.name for a, b in pares)
        fila.update(n_mapeados=len(pares), identidad_bolsillo=iguales / max(len(pares), 1))
        if len(pares) < 5:
            return {**fila, "estado": "bolsillo sin equivalencia en el modelo"}
        ca_e = np.array([a.find_atom("CA", "*").pos.tolist() for a, _ in pares])
        ca_m = np.array([b.find_atom("CA", "*").pos.tolist() for _, b in pares])
        mover = kabsch(ca_m, ca_e)
        rmsd_ca = float(np.sqrt(((mover(ca_m) - ca_e) ** 2).sum(1).mean()))
        xe, xm = [], []
        for a, b in pares:
            if a.name != b.name:
                continue
            for at in a:
                if at.element.name == "H":
                    continue
                bt = b.find_atom(at.name, "*")
                if bt:
                    xe.append(at.pos.tolist()); xm.append(bt.pos.tolist())
        xe, xm = np.array(xe), np.array(xm)
        rmsd_todos = float(np.sqrt(((mover(xm) - xe) ** 2).sum(1).mean()))
        plddt = [b.find_atom("CA", "*").b_iso for _, b in pares]
        fila.update(plddt_bolsillo=float(np.mean(plddt)), plddt_min_bolsillo=float(np.min(plddt)),
                    plddt_global=p.get("globalMetricValue"), rmsd_ca_bolsillo=rmsd_ca,
                    rmsd_atomos_bolsillo=rmsd_todos, n_atomos=len(xe), long_uniprot=len(seq_af),
                    estado="ok")
        return fila
    except Exception as e:  # se registra y se sigue
        return {**fila, "estado": f"error: {type(e).__name__}: {e}"[:200]}


if __name__ == "__main__":
    CACHE.mkdir(parents=True, exist_ok=True)
    AF.mkdir(parents=True, exist_ok=True)
    ids = sorted(p.name for p in PB.iterdir() if p.is_dir())
    if len(sys.argv) > 1:
        ids = ids[: int(sys.argv[1])]
    with ThreadPoolExecutor(2) as ex:
        filas = list(ex.map(medir, ids))
    tabla = pd.DataFrame(filas)
    salida = BASE / "resultados" / "bolsillos.csv"
    tabla.to_csv(salida, index=False)
    print(tabla["estado"].str[:40].value_counts().to_string())
    print(f"Guardado {salida} ({len(tabla)} complejos)")
