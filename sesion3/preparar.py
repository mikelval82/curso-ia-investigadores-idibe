"""Descarga los datos de la sesión 3, comprueba que están completos y prueba las librerías."""
import hashlib
import sys
import time
import urllib.request
from pathlib import Path

ORIGEN = ("https://raw.githubusercontent.com/Lucy-Moctezuma/"
          "ML-Tutorial-for-Antibiotic-Resistance-Predictions-for-E.-Coli/main/Datasets/")
HUELLAS = {
    "Metadata.csv": "5222bfde1e10e8007c133d949a80675cc1dfb20769b5c1b2d193e24dcf2e4efc",
    "AccessoryGene.csv": "87a8c1f3074fc7c83ecf130823d8da0ae20a14ae9cdc8a13d1c15d6ceaceb53f",
}
DATOS = Path(__file__).resolve().parent / "datos"


def huella(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for trozo in iter(lambda: f.read(1 << 20), b""):
            h.update(trozo)
    return h.hexdigest()


def descargar():
    DATOS.mkdir(exist_ok=True)
    for nombre, esperada in HUELLAS.items():
        destino = DATOS / nombre
        if destino.exists() and huella(destino) == esperada:
            print(f"OK  {nombre} ya estaba y está completo")
            continue
        print(f"... descargando {nombre}")
        temporal = destino.with_name(nombre + ".parcial")
        try:
            urllib.request.urlretrieve(ORIGEN + nombre, temporal)
        except OSError as e:
            sys.exit(f"FALLO  No se pudo descargar {nombre}: {e}\n"
                     "Comprueba la conexión y vuelve a ejecutar este programa.")
        if huella(temporal) != esperada:
            temporal.unlink()
            sys.exit(f"FALLO  {nombre} no coincide con el que usa el curso. Avisa al docente.")
        temporal.replace(destino)
        print(f"OK  {nombre}")


def probar():
    try:
        import matplotlib  # noqa: F401
        import pandas as pd
        import sklearn
        import xgboost  # noqa: F401
        from sklearn.ensemble import RandomForestClassifier
    except ImportError as e:
        sys.exit(f"FALLO  Falta una librería: {e.name}\nRepite el paso 2 de PREPARAR.md.")
    print(f"OK  librerías: pandas {pd.__version__}, scikit-learn {sklearn.__version__}")
    inicio = time.time()
    metadatos = pd.read_csv(DATOS / "Metadata.csv")
    genes = pd.read_csv(DATOS / "AccessoryGene.csv", index_col=0)
    print(f"OK  datos leídos: {len(metadatos)} aislados y {genes.shape[1]} genes")
    tabla = metadatos.dropna(subset=["CIP"]).set_index("Isolate").join(genes, how="inner")
    X = tabla[genes.columns[:500]].to_numpy()
    RandomForestClassifier(50, random_state=0).fit(X, tabla["CIP"] == "R")
    print(f"OK  un modelo de prueba se entrena en este ordenador ({time.time() - inicio:.0f} s en total)")


if __name__ == "__main__":
    descargar()
    probar()
    print("\nTodo listo para la sesión 3.")
