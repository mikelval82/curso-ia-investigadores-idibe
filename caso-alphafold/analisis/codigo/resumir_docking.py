"""Resume docking.csv: ¿funciona el docking sobre un modelo de AlphaFold?

Compara cada complejo consigo mismo: el mismo ligando y la misma caja, acoplado
sobre el modelo de AlphaFold y sobre la estructura experimental. El control
experimental dice qué casos puede resolver Vina; solo en esos tiene sentido
preguntar si el modelo estropea el resultado.
"""
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

BASE = Path(__file__).resolve().parent.parent
R = BASE / "resultados"
d = pd.read_csv(R / os.environ.get("SALIDA", "docking.csv"))
print(f"Complejos acoplados: {len(d)}")
print(d["estado"].str[:45].value_counts().to_string(), "\n")

ok = d[d.estado == "ok"].copy()
ok["acierta_af"] = ok.rmsd_af < 2.0
ok["acierta_exp"] = ok.rmsd_exp < 2.0

print(f"Aciertan (RMSD < 2 Å) sobre la estructura experimental: "
      f"{ok.acierta_exp.sum()} de {len(ok)} ({ok.acierta_exp.mean():.0%})")
print(f"Aciertan sobre el modelo de AlphaFold:                  "
      f"{ok.acierta_af.sum()} de {len(ok)} ({ok.acierta_af.mean():.0%})\n")

# los casos que Vina sí resuelve con la estructura buena
res = ok[ok.acierta_exp]
print(f"De los {len(res)} que Vina resuelve con la estructura experimental, "
      f"sobre el modelo aciertan {res.acierta_af.sum()} ({res.acierta_af.mean():.0%})")
print(f"Mediana de la RMSD en esos casos: experimental "
      f"{res.rmsd_exp.median():.2f} Å · modelo {res.rmsd_af.median():.2f} Å\n")

# el metal en el bolsillo, aparte
if "metal_en_bolsillo" in ok:
    for valor, grupo in ok.groupby("metal_en_bolsillo"):
        etiqueta = "con metal en el bolsillo" if valor else "sin metal"
        print(f"{etiqueta}: {len(grupo)} complejos · acierta exp "
              f"{grupo.acierta_exp.mean():.0%} · acierta AlphaFold {grupo.acierta_af.mean():.0%}")
    print()

# ¿avisa la confianza del bolsillo? ¿y lo bien hecho que esté el bolsillo?
for col, nombre in (("plddt_bolsillo", "confianza en el bolsillo (pLDDT)"),
                    ("rmsd_atomos_bolsillo", "parecido del bolsillo (RMSD de átomos)")):
    rho, p = stats.spearmanr(res[col], res.rmsd_af)
    print(f"Entre {nombre} y la RMSD de la pose sobre el modelo: Spearman {rho:.2f} (p = {p:.1e})")

# bolsillo bien hecho y docking fallido: el caso que importa para la clase
buenos = res[res.rmsd_atomos_bolsillo < 1.0]
print(f"\nBolsillo casi igual al experimental (< 1 Å) y Vina lo resuelve con la "
      f"estructura buena: {len(buenos)} complejos")
print(f"  de esos, el docking sobre el modelo acierta en {buenos.acierta_af.sum()} "
      f"({buenos.acierta_af.mean():.0%})")

tabla = pd.DataFrame({
    "complejos": [len(ok), len(res), len(buenos)],
    "acierta_sobre_experimental": [ok.acierta_exp.mean(), 1.0, 1.0],
    "acierta_sobre_alphafold": [ok.acierta_af.mean(), res.acierta_af.mean(),
                                buenos.acierta_af.mean()],
}, index=["todos", "los que Vina resuelve", "y con el bolsillo bien hecho"])
tabla.round(3).to_csv(R / os.environ.get("RESUMEN", "resumen_docking.csv"))
print("\n" + tabla.round(2).to_string())

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.3))
a1.scatter(ok.rmsd_exp, ok.rmsd_af, s=18, alpha=0.65, color="#397fab")
lim = [0.1, max(ok.rmsd_exp.max(), ok.rmsd_af.max()) * 1.2]
a1.plot(lim, lim, color="#888", lw=0.8, ls=":")
a1.axhline(2, color="#b15d10", lw=1, ls="--")
a1.axvline(2, color="#b15d10", lw=1, ls="--")
a1.set_xscale("log"); a1.set_yscale("log"); a1.set_xlim(lim); a1.set_ylim(lim)
a1.set_xlabel("Error de la pose sobre la estructura\nexperimental (RMSD, Å)")
a1.set_ylabel("Error de la pose sobre el modelo\nde AlphaFold (RMSD, Å)")
a1.set_title("Mismo ligando, dos receptores", fontsize=10)

a2.scatter(res.rmsd_atomos_bolsillo, res.rmsd_af, s=18, alpha=0.65, color="#397fab")
a2.axhline(2, color="#b15d10", lw=1, ls="--")
a2.set_yscale("log")
a2.set_xlabel("Diferencia del bolsillo del modelo\nfrente al experimental (RMSD, Å)")
a2.set_ylabel("Error de la pose sobre el modelo\nde AlphaFold (RMSD, Å)")
a2.set_title("Solo los que Vina resuelve con la\nestructura experimental", fontsize=10)

fig.tight_layout()
fig.savefig(R / os.environ.get("FIGURA", "docking_modelo_frente_a_experimental.png"), dpi=200)
print("\nFigura:", R / os.environ.get("FIGURA", "docking_modelo_frente_a_experimental.png"))
