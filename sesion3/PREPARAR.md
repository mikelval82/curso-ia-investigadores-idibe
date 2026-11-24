# Sesión 3 · Prepara tu ordenador antes de venir

Objetivo: llegar al 16 de diciembre con Python y los datos listos. Unos 15 minutos, la mayor parte descargando. **Hazlo en casa:** en clase no habrá tiempo.

Necesitas **uv**, que ya instalaste en la sesión 1, conexión a internet y 1 GB libre.

## 1. Abre una terminal en esta carpeta

- **Windows:** abre la carpeta, haz clic en la barra de direcciones, escribe `powershell` y pulsa Intro.
- **Mac:** clic derecho en la carpeta → Servicios → Nuevo terminal en la carpeta. Si no aparece, abre Terminal, escribe `cd ` (con un espacio), arrastra la carpeta a la ventana y pulsa Intro.
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

✔ Termina con **«Todo listo para la sesión 3»**. Descarga unos 10 MB y deja en `datos/` tres tablas y un `LEEME.md` que las describe.

## De dónde salen los datos

Expresión génica de islotes pancreáticos de 63 donantes fallecidos, 54 sin diabetes y 9 con diabetes tipo 2, del Nordic Islet Transplantation Programme. Los publicaron [Taneera y colaboradores (2012)](https://doi.org/10.1016/j.cmet.2012.06.006) y están en GEO con el código [GSE38642](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE38642). El programa los descarga de GEO y comprueba que el archivo es el mismo que usa el curso. Cita el artículo si los usas.

## Si algo falla

| Síntoma | Qué hacer |
|---|---|
| `uv` no se reconoce | Cierra la terminal y ábrela de nuevo. Si sigue, repite el paso de uv de la receta de la sesión 1 |
| No se puede descargar | Prueba con otra red o más tarde: a veces GEO no responde |
| «no coincide con el que usa el curso» | Avisa al docente: el archivo ha cambiado |
| El ordenador va muy lento | Sigue igualmente; en clase se puede trabajar por parejas |
