"""Comprueba que los datos de la sesión 3 están completos y que Python funciona en este ordenador."""
import hashlib
import sys
import time
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
DATOS = CARPETA / "datos"
TABLAS = {
    "bolsillos.csv": ("d711ffddae3bbb7fe6e00eaea10a304563038e2eb981807657b008ed255a3db6", 428),
    "docking_caja_ajustada.csv": ("7ffb20d5ed29180aa3401847d84bb863d9a7dedbad249654cb823699c2ee15ec", 90),
}
PRUEBA = CARPETA / "prueba_instalacion.png"


def huella(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for trozo in iter(lambda: f.read(1 << 20), b""):
            h.update(trozo)
    return h.hexdigest()


def comprobar_datos():
    for nombre, (esperada, _) in TABLAS.items():
        ruta = DATOS / nombre
        if not ruta.exists():
            sys.exit(f"FALLO  Falta datos/{nombre}.\n"
                     "Vuelve a descomprimir el ZIP de la sesión 3 sin sacar los archivos de su carpeta.")
        if huella(ruta) != esperada:
            sys.exit(f"FALLO  datos/{nombre} no coincide con el que usa el curso.\n"
                     "Vuelve a descomprimir el ZIP; si sigue igual, avisa al docente.")
        print(f"OK  datos/{nombre} está completo")


def comprobar_librerias():
    try:
        import matplotlib
        import pandas as pd
        import scipy
    except ImportError as e:
        sys.exit(f"FALLO  Falta una librería: {e.name}\nRepite el paso 2 de PREPARAR.md.")
    print(f"OK  librerías: pandas {pd.__version__}, scipy {scipy.__version__}, "
          f"matplotlib {matplotlib.__version__}")


def probar():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd
    from scipy.stats import spearmanr

    inicio = time.time()
    for nombre, (_, filas) in TABLAS.items():
        tabla = pd.read_csv(DATOS / nombre)
        if len(tabla) != filas:
            sys.exit(f"FALLO  datos/{nombre} no tiene {filas} filas. Avisa al docente.")
        print(f"OK  datos/{nombre}: {len(tabla)} filas y {tabla.shape[1]} columnas")

    bolsillos = pd.read_csv(DATOS / "bolsillos.csv")
    utiles = bolsillos[bolsillos["estado"] == "ok"]
    spearmanr(utiles["plddt_bolsillo"], utiles["rmsd_atomos_bolsillo"])
    plt.figure(figsize=(6, 4))
    plt.scatter(utiles["plddt_bolsillo"], utiles["rmsd_atomos_bolsillo"], s=18, alpha=0.6)
    plt.xlabel("Confianza de AlphaFold en el bolsillo")
    plt.ylabel("Diferencia con el experimental (Å)")
    plt.title(f"Prueba de instalación · {len(utiles)} filas con estado ok")
    plt.tight_layout()
    plt.savefig(PRUEBA, dpi=110)
    plt.close()
    print(f"OK  una figura de prueba se ha guardado en {PRUEBA.name} ({time.time() - inicio:.0f} s)")
    print("    Ábrela para comprobar que se ve bien. Puedes borrarla.")


if __name__ == "__main__":
    comprobar_datos()
    comprobar_librerias()
    probar()
    print("\nTodo listo para la sesión 3.")
