"""Descarga los datos de la sesión 3, comprueba que están completos, los ordena en tablas y prueba las librerías."""
import gzip
import hashlib
import io
import sys
import time
import urllib.request
from pathlib import Path

GEO = "https://ftp.ncbi.nlm.nih.gov/geo/"
SERIE = ("GSE38642_series_matrix.txt.gz", GEO + "series/GSE38nnn/GSE38642/matrix/GSE38642_series_matrix.txt.gz",
         "aa9513381d5e13a3ba08fc0665d88a36b08d98f712b451781298fffad0633bcb")
# GEO actualiza a veces la anotación de las sondas: se comprueba su contenido, no su huella
ANOTACION = ("GPL6244.annot.gz", GEO + "platforms/GPL6nnn/GPL6244/annot/GPL6244.annot.gz")
CARPETA = Path(__file__).resolve().parent / "datos"
ORIGINALES = CARPETA / "originales"

LEEME = """# Datos de la sesión 3

Expresión génica de islotes pancreáticos humanos de 63 donantes fallecidos (GEO GSE38642).
Son públicos. Los ha descargado `preparar.py`; no los modifiques.

## donantes.csv · una fila por donante

| Columna | Qué es |
|---|---|
| muestra | Código de la muestra en GEO (GSM…) |
| donante | Identificador del donante en el estudio |
| sexo | hombre o mujer |
| edad | Años |
| imc | Índice de masa corporal (kg/m²) |
| hba1c | Hemoglobina glicada (%). Vacía si no se midió |
| diagnostico | sin diabetes o diabetes tipo 2, según el estudio |

## expresion.csv · una fila por sonda, una columna por muestra

Expresión normalizada por los autores con RMA, en escala log2 (microarray Affymetrix Human Gene 1.0 ST).

## sondas.csv · qué gen mide cada sonda

Según la anotación de GEO (GPL6244). Algunas sondas no tienen gen y otras tienen varios, separados por `///`.

## Origen

- Taneera J. et al. (2012). *Cell Metabolism* 16:122-134. https://doi.org/10.1016/j.cmet.2012.06.006
- Islotes del Nordic Islet Transplantation Programme. Datos en https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE38642
- `originales/` guarda los archivos tal como se descargaron.
"""


def huella(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for trozo in iter(lambda: f.read(1 << 20), b""):
            h.update(trozo)
    return h.hexdigest()


def bajar(nombre, url):
    temporal = ORIGINALES / (nombre + ".parcial")
    print(f"... descargando {nombre}")
    try:
        urllib.request.urlretrieve(url, temporal)
    except OSError as e:
        sys.exit(f"FALLO  No se pudo descargar {nombre}: {e}\n"
                 "Comprueba la conexión y vuelve a ejecutar este programa.")
    return temporal


def descargar():
    ORIGINALES.mkdir(parents=True, exist_ok=True)
    nombre, url, esperada = SERIE
    destino = ORIGINALES / nombre
    if destino.exists() and huella(destino) == esperada:
        print(f"OK  {nombre} ya estaba y está completo")
    else:
        temporal = bajar(nombre, url)
        if huella(temporal) != esperada:
            temporal.unlink()
            sys.exit(f"FALLO  {nombre} no coincide con el que usa el curso. Avisa al docente.")
        temporal.replace(destino)
        print(f"OK  {nombre}")
    nombre, url = ANOTACION
    destino = ORIGINALES / nombre
    if destino.exists():
        print(f"OK  {nombre} ya estaba")
    else:
        bajar(nombre, url).replace(destino)
        print(f"OK  {nombre}")


def ordenar():
    import pandas as pd

    lineas = gzip.open(ORIGINALES / SERIE[0], "rt").read().splitlines()
    campos = {}
    caracteristicas = []
    for linea in lineas:
        partes = [x.strip('"') for x in linea.split("\t")]
        if partes[0] in ("!Sample_geo_accession", "!Sample_title"):
            campos[partes[0]] = partes[1:]
        elif partes[0] == "!Sample_characteristics_ch1":
            caracteristicas.append(partes[1:])
    valores = {c[0].split(":")[0].strip().lower(): [x.split(":", 1)[1].strip() for x in c] for c in caracteristicas}
    donantes = pd.DataFrame({
        "muestra": campos["!Sample_geo_accession"],
        "donante": [t.replace("human islets, ", "") for t in campos["!Sample_title"]],
        "sexo": [{"Male": "hombre", "Female": "mujer"}[x] for x in valores["sex"]],
        "edad": pd.to_numeric(valores["age"]),
        "imc": pd.to_numeric(valores["bmi"]),
        "hba1c": pd.to_numeric(pd.Series(valores["hba1c"]).replace("--", None)),
        "diagnostico": ["diabetes tipo 2" if x.startswith("T2D") else "sin diabetes" for x in valores["status"]],
    })

    inicio, fin = lineas.index("!series_matrix_table_begin"), lineas.index("!series_matrix_table_end")
    expresion = pd.read_csv(io.StringIO("\n".join(lineas[inicio + 1:fin])), sep="\t", index_col=0)
    expresion.index.name = "sonda"

    with gzip.open(ORIGINALES / ANOTACION[0], "rt", encoding="utf-8", errors="replace") as f:
        texto = f.read()
    tabla = texto[texto.index("!platform_table_begin") + len("!platform_table_begin\n"):]
    anotacion = pd.read_csv(io.StringIO(tabla), sep="\t", usecols=["ID", "Gene symbol"], dtype=str)
    anotacion = anotacion[anotacion["ID"].str.isdigit()]
    sondas = pd.DataFrame({"sonda": anotacion["ID"].astype(int), "gen": anotacion["Gene symbol"]})
    sondas = sondas[sondas["sonda"].isin(expresion.index)]

    if len(donantes) != 63 or expresion.shape != (18808, 63) or sondas["gen"].notna().sum() < 15000:
        sys.exit("FALLO  Los datos no tienen la forma esperada. Avisa al docente.")
    donantes.to_csv(CARPETA / "donantes.csv", index=False)
    expresion.to_csv(CARPETA / "expresion.csv")
    sondas.to_csv(CARPETA / "sondas.csv", index=False)
    (CARPETA / "LEEME.md").write_text(LEEME, encoding="utf-8")
    print(f"OK  tablas: {len(donantes)} donantes, {expresion.shape[0]} sondas, "
          f"{sondas['gen'].notna().sum()} con gen")


def probar():
    try:
        import matplotlib  # noqa: F401
        import pandas as pd
        import scipy
        import statsmodels.formula.api as smf
    except ImportError as e:
        sys.exit(f"FALLO  Falta una librería: {e.name}\nRepite el paso 2 de PREPARAR.md.")
    print(f"OK  librerías: pandas {pd.__version__}, scipy {scipy.__version__}")
    inicio = time.time()
    donantes = pd.read_csv(CARPETA / "donantes.csv")
    expresion = pd.read_csv(CARPETA / "expresion.csv", index_col=0)
    tabla = donantes.dropna(subset=["hba1c"])
    tabla = tabla.assign(y=expresion.iloc[0][tabla["muestra"]].to_numpy())
    smf.ols("y ~ hba1c + edad + imc + sexo", tabla).fit()
    print(f"OK  un modelo de prueba funciona en este ordenador ({time.time() - inicio:.0f} s)")


if __name__ == "__main__":
    try:
        import pandas  # noqa: F401
    except ImportError:
        sys.exit("FALLO  Falta una librería: pandas\nRepite el paso 2 de PREPARAR.md.")
    descargar()
    ordenar()
    probar()
    print("\nTodo listo para la sesión 3.")
