"""Recalcula todas las cifras propias que se citan en borrador/documento.md.

Solo biblioteca estándar, para que corra sin pandas ni scipy. Lee las tablas de
`resultados/` y escribe `resultados/cifras_del_texto.csv`, con una fila por cifra:
clave, valor y de dónde sale. Ninguna cifra del texto se calcula a mano.

    python3 analisis/cifras_del_texto.py
"""

import csv
import math
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
R = BASE / "resultados"


# --- utilidades -------------------------------------------------------------

def leer(nombre):
    with open(R / nombre, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(fila, campo):
    v = fila.get(campo, "")
    return float(v) if v not in ("", None) else None


def booleano(fila, campo):
    return str(fila.get(campo, "")).strip().lower() in ("true", "1", "yes")


def mediana(xs):
    xs = sorted(xs)
    n = len(xs)
    if n == 0:
        return None
    m = n // 2
    return xs[m] if n % 2 else (xs[m - 1] + xs[m]) / 2


def rangos(xs):
    """Rangos con media en los empates."""
    orden = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(orden):
        j = i
        while j + 1 < len(orden) and xs[orden[j + 1]] == xs[orden[i]]:
            j += 1
        medio = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[orden[k]] = medio
        i = j + 1
    return r


def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else float("nan")


def _betacf(a, b, x, iteraciones=300):
    """Fracción continua de la beta incompleta (Numerical Recipes)."""
    tiny = 1e-30
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, iteraciones + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 3e-16:
            break
    return h


def betainc(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    frente = math.exp(lbeta + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return frente * _betacf(a, b, x) / a
    return 1.0 - frente * _betacf(b, a, 1.0 - x) / b


def spearman(xs, ys):
    """rho de Spearman y p a dos colas por la aproximación t de Student."""
    n = len(xs)
    rho = pearson(rangos(xs), rangos(ys))
    if n < 3 or abs(rho) >= 1:
        return rho, 0.0
    t = rho * math.sqrt((n - 2) / (1 - rho * rho))
    gl = n - 2
    p = betainc(gl / 2, 0.5, gl / (gl + t * t))
    return rho, p


# --- cifras -----------------------------------------------------------------

filas = []


def apunta(clave, valor, fuente):
    if isinstance(valor, float):
        # un p por debajo de la resolución de 4 decimales no se escribe como 0
        if clave.endswith("_p") and 0 < valor < 1e-4:
            valor = f"{valor:.2e}"
        else:
            valor = round(valor, 4)
    filas.append({"clave": clave, "valor": valor, "fuente": fuente})


# Parte 1: calidad del bolsillo
bolsillos = leer("bolsillos.csv")
apunta("bolsillos_entradas_de_partida", len(bolsillos), "bolsillos.csv")

ok = [f for f in bolsillos
      if f["estado"] == "ok" and num(f, "identidad_bolsillo") is not None
      and num(f, "identidad_bolsillo") >= 0.9]
apunta("bolsillos_analizados", len(ok), "bolsillos.csv, estado ok e identidad >= 0,9")
apunta("bolsillos_proteinas_distintas", len({f["uniprot"] for f in ok}), "bolsillos.csv")
apunta("bolsillos_descartados", len(bolsillos) - len(ok), "bolsillos.csv")

plddt = [num(f, "plddt_bolsillo") for f in ok]
rmsd = [num(f, "rmsd_atomos_bolsillo") for f in ok]
rho, p = spearman(plddt, rmsd)
apunta("spearman_plddt_rmsd_bolsillo", rho, "bolsillos.csv")
apunta("spearman_plddt_rmsd_bolsillo_p", p, "bolsillos.csv")
apunta("plddt_bolsillo_minimo", min(plddt), "bolsillos.csv")

for etiqueta, prueba in (("alta_90", lambda v: v >= 90),
                         ("media_70_90", lambda v: 70 <= v < 90)):
    grupo = [f for f in ok if prueba(num(f, "plddt_bolsillo"))]
    rs = [num(f, "rmsd_atomos_bolsillo") for f in grupo]
    apunta(f"confianza_{etiqueta}_n", len(grupo), "bolsillos.csv")
    apunta(f"confianza_{etiqueta}_rmsd_mediana", mediana(rs), "bolsillos.csv")
    apunta(f"confianza_{etiqueta}_frac_bajo_1A", sum(r < 1 for r in rs) / len(rs), "bolsillos.csv")
    apunta(f"confianza_{etiqueta}_frac_bajo_2A", sum(r < 2 for r in rs) / len(rs), "bolsillos.csv")

alta = [f for f in ok if num(f, "plddt_bolsillo") >= 90]
apunta("confianza_alta_n_rmsd_2A_o_mas",
       sum(num(f, "rmsd_atomos_bolsillo") >= 2 for f in alta), "bolsillos.csv")

# Parte 2: docking
dock = [f for f in leer("docking_caja_ajustada.csv") if f["estado"] == "ok"]
apunta("docking_n", len(dock), "docking_caja_ajustada.csv")
apunta("docking_acierto_experimental",
       sum(booleano(f, "acierta_exp") for f in dock) / len(dock), "docking_caja_ajustada.csv")
apunta("docking_acierto_alphafold",
       sum(booleano(f, "acierta_af") for f in dock) / len(dock), "docking_caja_ajustada.csv")

resueltos = [f for f in dock if booleano(f, "acierta_exp")]
apunta("docking_resueltos_n", len(resueltos), "docking_caja_ajustada.csv")
apunta("docking_resueltos_acierto_alphafold",
       sum(booleano(f, "acierta_af") for f in resueltos) / len(resueltos),
       "docking_caja_ajustada.csv")
apunta("docking_resueltos_rmsd_mediana_exp",
       mediana([num(f, "rmsd_exp") for f in resueltos]), "docking_caja_ajustada.csv")
apunta("docking_resueltos_rmsd_mediana_af",
       mediana([num(f, "rmsd_af") for f in resueltos]), "docking_caja_ajustada.csv")

buenos = [f for f in resueltos if num(f, "rmsd_atomos_bolsillo") < 1]
apunta("docking_bolsillo_bueno_n", len(buenos), "docking_caja_ajustada.csv")
apunta("docking_bolsillo_bueno_aciertos",
       sum(booleano(f, "acierta_af") for f in buenos), "docking_caja_ajustada.csv")
apunta("docking_bolsillo_bueno_frac",
       sum(booleano(f, "acierta_af") for f in buenos) / len(buenos), "docking_caja_ajustada.csv")

for etiqueta, prueba in (("con_metal", True), ("sin_metal", False)):
    grupo = [f for f in dock if booleano(f, "metal_en_bolsillo") is prueba]
    apunta(f"docking_{etiqueta}_n", len(grupo), "docking_caja_ajustada.csv")
    apunta(f"docking_{etiqueta}_acierto_alphafold",
           sum(booleano(f, "acierta_af") for f in grupo) / len(grupo),
           "docking_caja_ajustada.csv")

# ¿Avisan la confianza o el parecido del bolsillo del error de la pose? Como en
# resumir_docking.py: sobre los complejos que Vina resuelve con la estructura buena,
# contra la RMSD de la pose sobre el modelo (continua), no contra el acierto binario.
error_pose = [num(f, "rmsd_af") for f in resueltos]
for campo, clave in (("plddt_bolsillo", "plddt"), ("rmsd_atomos_bolsillo", "rmsd_bolsillo")):
    rho, p = spearman([num(f, campo) for f in resueltos], error_pose)
    apunta(f"spearman_{clave}_error_pose", rho, "docking_caja_ajustada.csv, los que Vina resuelve")
    apunta(f"spearman_{clave}_error_pose_p", p, "docking_caja_ajustada.csv, los que Vina resuelve")

# Tamaño de la caja, sobre los complejos presentes en las dos tandas
grande = {f["complejo"]: f for f in leer("docking_caja_grande.csv") if f["estado"] == "ok"}
ajustada = {f["complejo"]: f for f in dock}
comunes = sorted(set(grande) & set(ajustada))
apunta("caja_comunes_n", len(comunes), "docking_caja_grande.csv + docking_caja_ajustada.csv")
for etiqueta, tabla in (("grande", grande), ("ajustada", ajustada)):
    sub = [tabla[c] for c in comunes]
    apunta(f"caja_{etiqueta}_acierto_experimental",
           sum(booleano(f, "acierta_exp") for f in sub) / len(sub), "los dos docking_caja_*.csv")
    apunta(f"caja_{etiqueta}_acierto_alphafold",
           sum(booleano(f, "acierta_af") for f in sub) / len(sub), "los dos docking_caja_*.csv")
    apunta(f"caja_{etiqueta}_rmsd_mediana_af",
           mediana([num(f, "rmsd_af") for f in sub]), "los dos docking_caja_*.csv")
cambia_a_acierto = sum(1 for c in comunes
                       if booleano(ajustada[c], "acierta_af") and not booleano(grande[c], "acierta_af"))
cambia_a_fallo = sum(1 for c in comunes
                     if booleano(grande[c], "acierta_af") and not booleano(ajustada[c], "acierta_af"))
apunta("caja_cambian_a_acierto", cambia_a_acierto, "los dos docking_caja_*.csv")
apunta("caja_cambian_a_fallo", cambia_a_fallo, "los dos docking_caja_*.csv")


salida = R / "cifras_del_texto.csv"
with open(salida, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["clave", "valor", "fuente"])
    w.writeheader()
    w.writerows(filas)

for fila in filas:
    print(f"{fila['clave']:48} {fila['valor']}")
print(f"\n{len(filas)} cifras escritas en {salida}")
