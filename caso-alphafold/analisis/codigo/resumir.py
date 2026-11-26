"""Resume bolsillos.csv: ¿la confianza de AlphaFold en el bolsillo avisa de si el bolsillo está bien?"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

BASE = Path(__file__).resolve().parent.parent
R = BASE / "resultados"
t = pd.read_csv(R / "bolsillos.csv")
print("Complejos:", len(t))
print(t["estado"].str[:45].value_counts().to_string(), "\n")

ok = t[(t.estado == "ok") & (t.identidad_bolsillo >= 0.9)].copy()
print(f"Con modelo y bolsillo equivalente (identidad >= 90 %): {len(ok)}  ·  proteínas distintas: {ok.uniprot.nunique()}")

rho, p = stats.spearmanr(ok.plddt_bolsillo, ok.rmsd_atomos_bolsillo)
print(f"Spearman pLDDT del bolsillo frente a RMSD de átomos del bolsillo: {rho:.2f} (p = {p:.1e})")
rho2, p2 = stats.spearmanr(ok.plddt_bolsillo, ok.rmsd_ca_bolsillo)
print(f"Spearman pLDDT frente a RMSD de Cα del bolsillo: {rho2:.2f} (p = {p2:.1e})\n")

ok["confianza"] = pd.cut(ok.plddt_bolsillo, [0, 70, 90, 101], right=False,
                         labels=["baja (< 70)", "media (70–90)", "alta (≥ 90)"])
ok["bien_1A"] = ok.rmsd_atomos_bolsillo < 1.0
ok["bien_2A"] = ok.rmsd_atomos_bolsillo < 2.0
tabla = ok.groupby("confianza", observed=True).agg(
    complejos=("complejo", "size"),
    rmsd_mediana=("rmsd_atomos_bolsillo", "median"),
    bolsillo_bien_1A=("bien_1A", "mean"),
    bolsillo_bien_2A=("bien_2A", "mean"))
print(tabla.round(2).to_string(), "\n")
tabla.to_csv(R / "resumen_por_confianza.csv")

# una fila por proteína (la primera), para que no pesen más las repetidas
una = ok.drop_duplicates("uniprot")
rho3, p3 = stats.spearmanr(una.plddt_bolsillo, una.rmsd_atomos_bolsillo)
print(f"Una por proteína ({len(una)}): Spearman {rho3:.2f} (p = {p3:.1e})")
alta = ok[ok.plddt_bolsillo >= 90]
print(f"Con confianza alta, bolsillos con RMSD de átomos >= 2 Å: {(alta.rmsd_atomos_bolsillo >= 2).sum()} de {len(alta)}")

fig, ax = plt.subplots(figsize=(6, 4.2))
ax.scatter(ok.plddt_bolsillo, ok.rmsd_atomos_bolsillo, s=14, alpha=0.6, color="#397fab")
ax.axhline(2, color="#b15d10", lw=1, ls="--")
ax.axvline(90, color="#888", lw=0.8, ls=":")
ax.set_xlabel("Confianza de AlphaFold en el bolsillo (pLDDT medio)")
ax.set_ylabel("Diferencia con el bolsillo experimental\n(RMSD de átomos, Å)")
ax.set_yscale("log")
ax.set_title(f"PoseBusters, {len(ok)} complejos · Spearman {rho:.2f}", fontsize=10)
fig.tight_layout()
fig.savefig(R / "confianza_frente_a_bolsillo.png", dpi=200)
print("Figura:", R / "confianza_frente_a_bolsillo.png")
