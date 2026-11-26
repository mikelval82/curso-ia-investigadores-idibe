"""Paso 2: acoplar cada ligando en el modelo de AlphaFold y ver si acierta la pose.

Para cada complejo de la muestra:
  1. se superpone el modelo de AlphaFold sobre la estructura experimental
     usando los Cα del bolsillo (la misma superposición de medir_bolsillos.py),
     de modo que el ligando experimental sirve de referencia;
  2. se prepara el receptor (modelo movido) y el ligando;
  3. se acopla con AutoDock Vina en una caja centrada en el ligando experimental;
  4. se mide la RMSD de la mejor pose frente a la experimental, con simetría.

Criterio habitual: la pose se considera correcta si la RMSD es menor de 2 Å.
"""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")

import gemmi
import numpy as np
import pandas as pd
from meeko import (MoleculePreparation, PDBQTMolecule, PDBQTWriterLegacy, RDKitMolCreate)
from openbabel import pybel
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem, rdMolAlign
from vina import Vina

sys.path.insert(0, str(Path(__file__).resolve().parent))
from medir_bolsillos import (AF, CACHE, CORTE, PB, alinear, kabsch, ligando_xyz,
                             residuos, tres_a_uno)

RDLogger.DisableLog("rdApp.*")
pybel.ob.obErrorLog.StopLogging()

BASE = Path(__file__).resolve().parent.parent
TRABAJO = BASE / "datos" / "docking"
MARGEN = float(os.environ.get("MARGEN", 5.0))      # Å añadidos al tamaño del ligando
CAJA_MIN = float(os.environ.get("CAJA_MIN", 12.0))  # lado mínimo de la caja
SALIDA = os.environ.get("SALIDA", "docking.csv")
POSES = 9
ESFUERZO = 16      # exhaustiveness de Vina


def modelo_movido(ident, uniprot, cadena_elegida):
    """Devuelve (ruta del modelo de AlphaFold superpuesto, ligando experimental)."""
    carpeta = PB / ident
    estructura = gemmi.read_structure(str(carpeta / f"{ident}_protein.pdb"))
    lig = ligando_xyz(carpeta / f"{ident}_ligand.sdf")
    modelo = estructura[0]
    cadena = next(c for c in modelo if c.name == cadena_elegida)
    res = residuos(cadena)
    bols = [i for i, r in enumerate(res)
            if np.min(np.linalg.norm(
                np.array([a.pos.tolist() for a in r if a.element.name != "H"])[:, None]
                - lig[None], axis=2)) < CORTE]
    seq_exp = "".join(tres_a_uno(r.name) for r in res)

    pred = json.loads((CACHE / f"afapi_{uniprot}.json").read_text())
    af_ruta = AF / f"{pred[0]['modelEntityId']}.pdb"
    af = gemmi.read_structure(str(af_ruta))
    af.setup_entities()
    res_af = residuos(af[0][0])
    seq_af = "".join(tres_a_uno(r.name) for r in res_af)
    mapa = alinear(seq_exp, seq_af)
    pares = [(res[i], res_af[mapa[i]]) for i in bols if i in mapa]
    if len(pares) < 5:
        raise RuntimeError("bolsillo sin equivalencia")

    ca_e = np.array([a.find_atom("CA", "*").pos.tolist() for a, _ in pares])
    ca_m = np.array([b.find_atom("CA", "*").pos.tolist() for _, b in pares])
    mover = kabsch(ca_m, ca_e)
    for cad in af[0]:
        for r in cad:
            for at in r:
                x, y, z = mover(np.array([at.pos.tolist()]))[0]
                at.pos = gemmi.Position(float(x), float(y), float(z))

    salida = TRABAJO / f"{ident}_receptor.pdb"
    af.remove_ligands_and_waters()
    af.remove_hydrogens()
    af.write_pdb(str(salida))
    return salida, lig


def receptor_pdbqt(ruta_pdb):
    """Receptor rígido en PDBQT con Open Babel (cargas de Gasteiger)."""
    salida = ruta_pdb.with_suffix(".pdbqt")
    if not salida.exists():
        mol = next(pybel.readfile("pdb", str(ruta_pdb)))
        mol.OBMol.AddHydrogens(False, True, 7.4)
        mol.write("pdbqt", str(salida), overwrite=True, opt={"r": "", "n": ""})
    return salida


def ligando_pdbqt(sdf):
    """Ligando flexible en PDBQT con Meeko; devuelve (pdbqt, molécula experimental)."""
    exp = Chem.MolFromMolFile(str(sdf), removeHs=True)
    if exp is None:
        raise RuntimeError("el SDF no se puede leer")
    mol = Chem.AddHs(exp, addCoords=True)
    prep = MoleculePreparation()
    conf = prep.prepare(mol)[0]
    pdbqt, ok, err = PDBQTWriterLegacy.write_string(conf)
    if not ok:
        raise RuntimeError(f"Meeko: {err}")
    return pdbqt, exp


METALES = {"ZN", "MG", "MN", "FE", "CU", "CA", "NI", "CO", "CD", "NA", "K"}


def receptor_experimental(ident, cadena_elegida):
    """Control: la misma cadena experimental, sin aguas, conservando los iones metálicos.

    El modelo de AlphaFold no trae cofactores, así que el control sí los tiene y el
    modelo no: esa diferencia forma parte de lo que se quiere medir y se anota aparte
    con la columna metal_en_bolsillo.
    """
    salida = TRABAJO / f"{ident}_experimental.pdb"
    if not salida.exists():
        est = gemmi.read_structure(str(PB / ident / f"{ident}_protein.pdb"))
        est.setup_entities()
        est.remove_waters()
        est.remove_hydrogens()
        for cad in est[0]:
            quitar = [r.name for r in cad
                      if not (gemmi.find_tabulated_residue(r.name)
                              and gemmi.find_tabulated_residue(r.name).is_amino_acid())
                      and r.name.strip().upper() not in METALES]
            for nombre in set(quitar):
                while True:
                    idx = next((i for i, r in enumerate(cad) if r.name == nombre), None)
                    if idx is None:
                        break
                    del cad[idx]
        est.write_pdb(str(salida))
    return salida


def metal_cerca(ident, lig_xyz, corte=3.5):
    """¿Hay un ion metálico a menos de `corte` del ligando experimental?"""
    est = gemmi.read_structure(str(PB / ident / f"{ident}_protein.pdb"))
    for cad in est[0]:
        for r in cad:
            if r.name.strip().upper() not in METALES:
                continue
            for at in r:
                if np.min(np.linalg.norm(lig_xyz - np.array(at.pos.tolist()), axis=1)) < corte:
                    return True
    return False


def _vina(rec, pdbqt, centro, tamano, salida):
    v = Vina(sf_name="vina", cpu=1, seed=42, verbosity=0)
    v.set_receptor(str(rec))
    v.set_ligand_from_string(pdbqt)
    v.compute_vina_maps(center=[float(x) for x in centro],
                        box_size=[float(x) for x in tamano])
    v.dock(exhaustiveness=ESFUERZO, n_poses=POSES)
    v.write_poses(str(salida), n_poses=POSES, overwrite=True)
    return v.energies(n_poses=POSES)


def acoplar(ident, uniprot, cadena):
    fila = {"complejo": ident, "uniprot": uniprot}
    try:
        rec_pdb, lig_xyz = modelo_movido(ident, uniprot, cadena)
        pdbqt, exp = ligando_pdbqt(PB / ident / f"{ident}_ligand.sdf")

        centro = lig_xyz.mean(0)
        tamano = np.maximum(lig_xyz.max(0) - lig_xyz.min(0) + MARGEN, CAJA_MIN)
        fila["caja_A"] = float(tamano.max())
        fila["metal_en_bolsillo"] = metal_cerca(ident, lig_xyz)

        for etiqueta, receptor in (("af", receptor_pdbqt(rec_pdb)),
                                   ("exp", receptor_pdbqt(receptor_experimental(ident, cadena)))):
            salida = TRABAJO / f"{ident}_poses_{etiqueta}.pdbqt"
            energias = _vina(receptor, pdbqt, centro, tamano, salida)
            rmsds = [rdMolAlign.CalcRMS(p, exp) for p in _leer_poses(salida.read_text())]
            if not rmsds:
                raise RuntimeError(f"{etiqueta}: no se pudo leer ninguna pose")
            fila.update({
                f"energia_{etiqueta}": float(energias[0][0]),
                f"rmsd_{etiqueta}": float(rmsds[0]),
                f"rmsd_min_{etiqueta}": float(min(rmsds)),
                f"acierta_{etiqueta}": bool(rmsds[0] < 2.0),
                f"n_poses_{etiqueta}": len(rmsds),
            })
        fila["estado"] = "ok"
        return fila
    except Exception as e:
        return {**fila, "estado": f"error: {type(e).__name__}: {e}"[:200]}


def _leer_poses(texto):
    """Reconstruye las poses de Vina con Meeko, que conserva la química del ligando."""
    pmol = PDBQTMolecule(texto, skip_typing=True)
    moleculas = []
    for conf in RDKitMolCreate.from_pdbqt_mol(pmol, only_cluster_leads=False):
        if conf is None:
            continue
        for i in range(conf.GetNumConformers()):
            m = Chem.Mol(conf, confId=i) if conf.GetNumConformers() == 1 else None
            if m is None:
                m = Chem.Mol(conf)
                m.RemoveAllConformers()
                m.AddConformer(conf.GetConformer(i), assignId=True)
            moleculas.append(Chem.RemoveHs(m))
    return moleculas


if __name__ == "__main__":
    TRABAJO.mkdir(parents=True, exist_ok=True)
    t = pd.read_csv(BASE / "resultados" / "bolsillos.csv")
    ok = t[(t.estado == "ok") & (t.identidad_bolsillo >= 0.9)].copy()

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    # muestra repartida por confianza, una sola vez cada proteína
    ok = ok.sort_values("complejo").drop_duplicates("uniprot")
    ok["tramo"] = pd.cut(ok.plddt_bolsillo, [0, 85, 90, 95, 101], right=False)
    muestra = (ok.groupby("tramo", observed=True, group_keys=False)
                 .apply(lambda g: g.sample(min(len(g), max(1, n // 4)), random_state=42)))
    print(f"Muestra: {len(muestra)} complejos")
    print(pd.cut(muestra.plddt_bolsillo, [0, 85, 90, 95, 101], right=False)
            .value_counts().sort_index().to_string(), "\n", flush=True)

    tareas = [(r.complejo, r.uniprot, r.cadena, r.plddt_bolsillo, r.rmsd_atomos_bolsillo)
              for r in muestra.itertuples()]
    filas = []
    with ProcessPoolExecutor(int(os.environ.get("TRABAJADORES", 8))) as ex:
        futuros = {ex.submit(acoplar, c, u, cad): (c, pl, rb)
                   for c, u, cad, pl, rb in tareas}
        for i, fut in enumerate(as_completed(futuros), 1):
            c, pl, rb = futuros[fut]
            fila = fut.result()
            fila.update(plddt_bolsillo=pl, rmsd_atomos_bolsillo=rb)
            filas.append(fila)
            print(f"[{i}/{len(tareas)}] {c} {fila['estado'][:50]} "
                  f"af={fila.get('rmsd_af', float('nan')):.2f} "
                  f"exp={fila.get('rmsd_exp', float('nan')):.2f}", flush=True)
            pd.DataFrame(filas).to_csv(BASE / "resultados" / SALIDA, index=False)

    tabla = pd.DataFrame(filas)
    print("\n" + tabla["estado"].str[:40].value_counts().to_string())
    print(f"Guardado {BASE / 'resultados' / SALIDA}")
