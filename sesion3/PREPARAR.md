# Sesión 3 · Prepara tu ordenador antes de venir

Objetivo: llegar al 16 de diciembre con Python listo. Unos 5 minutos. **Hazlo en casa:** en clase no habrá tiempo.

Necesitas **uv**, que ya instalaste en la sesión 1. Los datos vienen dentro de esta carpeta: no hay que descargar nada.

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

## 3. Comprueba que todo funciona

```
uv run --no-project preparar.py
```

✔ Termina con **«Todo listo para la sesión 3»** y deja una figura, `prueba_instalacion.png`. Ábrela: si se ve, matplotlib funciona. Puedes borrarla.

## Qué hay en datos/

Dos tablas con los resultados ya calculados del análisis del curso sobre AlphaFold:

- `bolsillos.csv`: una fila por complejo proteína-ligando, con la confianza de AlphaFold en el bolsillo y lo que se parece al bolsillo medido en el laboratorio.
- `docking_caja_ajustada.csv`: los 90 complejos en los que además se probó el docking.
- `LEEME.md`: qué es cada columna, de dónde salen los datos y qué no pueden decir. Léelo antes de clase, son dos páginas.

Los datos originales son públicos: PoseBusters (Buttenschoen et al., *Chemical Science* 2024) y los modelos de AlphaFold DB. En clase no se vuelve a ejecutar el análisis: se trabaja sobre estas tablas.

## Si algo falla

| Síntoma | Qué hacer |
|---|---|
| `uv` no se reconoce | Cierra la terminal y ábrela de nuevo. Si sigue, repite el paso de uv de la receta de la sesión 1 |
| «Falta datos/…» | Vuelve a descomprimir el ZIP entero, sin sacar los archivos de su carpeta |
| «no coincide con el que usa el curso» | Descomprime otra vez el ZIP; si sigue, avisa al docente |
| El ordenador va muy lento | Sigue igualmente; en clase se puede trabajar por parejas |
