# Sesión 3 · Prepara tu ordenador antes de venir

Objetivo: llegar al 16 de diciembre con Python y los datos listos. Unos 15 minutos, la mayor parte descargando. **Hazlo en casa:** en clase no habrá tiempo.

Necesitas **uv**, que ya instalaste en la sesión 1, conexión a internet y unos 2 GB libres.

## 1. Abre una terminal en esta carpeta

- **Windows:** abre la carpeta, haz clic en la barra de direcciones, escribe `powershell` y pulsa Intro.
- **Mac:** clic derecho en la carpeta → Servicios → Nuevo terminal en la carpeta.
- **Linux:** clic derecho en la carpeta → Abrir en un terminal.

## 2. Crea el entorno de Python

Ejecuta estas dos órdenes, una detrás de otra:

```
uv venv --python 3.12
uv pip install -r requirements.txt
```

✔ Aparece una carpeta `.venv`. No modifica el Python de tu ordenador.

## 3. Descarga los datos y comprueba todo

```
uv run --no-project preparar.py
```

✔ Termina con **«Todo listo para la sesión 3»**. Descarga unos 70 MB.

## De dónde salen los datos

Son de [Moradigaravand y colaboradores (2018)](https://doi.org/10.1371/journal.pcbi.1006258), en la versión del tutorial de [Orcales y colaboradores (2024)](https://doi.org/10.1371/journal.pcbi.1012579). Se descargan de [su repositorio](https://github.com/Lucy-Moctezuma/ML-Tutorial-for-Antibiotic-Resistance-Predictions-for-E.-Coli): no declara licencia, así que aquí no repartimos copias. Cita los dos artículos si los usas.

## Si algo falla

| Síntoma | Qué hacer |
|---|---|
| `uv` no se reconoce | Cierra la terminal y ábrela de nuevo. Si sigue, repite el paso de uv de la receta de la sesión 1 |
| No se puede descargar | Prueba con otra red: algunas bloquean GitHub |
| «no coincide con el que usa el curso» | Avisa al docente: el archivo ha cambiado |
| En Mac, error de `libomp` al usar xgboost | Puedes seguir sin xgboost: díselo a Claude y anótalo como decisión |
| El ordenador va muy lento | Sigue igualmente; en clase se puede trabajar por parejas |
