# Prueba para la sesión 4: confianza de AlphaFold y bolsillos de unión

Análisis piloto del 25/11/2026 para rehacer las diapositivas 6 a 11 de la sesión 4 con el caso de AlphaFold de la sesión 2. No es material para participantes.

**Pregunta (versión sencilla de la de la sesión 2):** ¿la confianza de AlphaFold en el bolsillo (pLDDT medio) avisa de si el bolsillo del modelo se parece al experimental?

## Datos

- PoseBusters Benchmark set (Buttenschoen et al., Chem Sci 2024; Zenodo 8278563): 428 complejos proteína-ligando del PDB publicados desde 2021. `datos/posebusters_paper_data.zip`, sha256 495a8f43…e721c.
- Cadena → UniProt: API de SIFTS (PDBe). Modelos: AlphaFold DB, versión 6 (descargados el 25/11/2026).

## Método

`codigo/medir_bolsillos.py`. Bolsillo: residuos con algún átomo pesado a menos de 6 Å del ligando en la estructura experimental, en la cadena con más residuos de bolsillo. Se alinean las secuencias del PDB y del modelo, se superponen los Cα del bolsillo y se mide la RMSD de Cα y de todos los átomos pesados comunes. `codigo/resumir.py` hace la tabla y la figura.

## Resultado

374 complejos con modelo y bolsillo equivalente (339 proteínas distintas); se perdieron 54 (20 sin UniProt en SIFTS, 16 sin modelo, 4 sin equivalencia, 4 por límite de la API, y 10 con identidad del bolsillo menor del 90 %).

- Spearman entre pLDDT del bolsillo y RMSD de átomos del bolsillo: −0,56 (una por proteína: −0,56).
- Confianza alta (≥ 90): 316 complejos, mediana 0,95 Å, 58 % por debajo de 1 Å, 92 % por debajo de 2 Å.
- Confianza media (70–90): 58 complejos, mediana 1,64 Å, 12 % por debajo de 1 Å, 67 % por debajo de 2 Å.
- No hay casi bolsillos con confianza baja: el mínimo es 73.
- Aun con confianza alta, 24 de 316 bolsillos difieren 2 Å o más. Ejemplo: RORγt (P51449, 7NP6 y 8FAV), pLDDT 94 y unos 5,8 Å.

## Paso 2: el docking (25/11/2026)

`codigo/docking.py`. Muestra de 90 complejos (una entrada por proteína, repartida en cuatro
tramos de pLDDT). Cada ligando se acopla **dos veces** con AutoDock Vina 1.2.7: sobre el
modelo de AlphaFold superpuesto por los Cα del bolsillo, y sobre la estructura experimental
como control. Misma caja y mismo ligando en ambos. El control dice qué casos sabe resolver
Vina; solo en esos tiene sentido preguntar si el modelo estropea el resultado.
Ligando con Meeko, receptor rígido con Open Babel, caja centrada en el ligando experimental,
exhaustiveness 16, 9 poses, RMSD con corrección de simetría (`rdMolAlign.CalcRMS`).

Resultados con los 90 complejos:

| | acierta sobre la experimental | acierta sobre AlphaFold |
|---|---|---|
| los 90 | 72 % | 17 % |
| los 65 que Vina resuelve | (100 % por definición) | 22 % |
| y además con el bolsillo bien hecho (< 1 Å) | | 38 % (8 de 21) |

- Mediana del error en los 65 que Vina resuelve: 0,69 Å sobre la experimental y 4,67 Å sobre el modelo.
- El metal en el bolsillo no explica la diferencia (16 % sin metal, 20 % con metal).
- **Corregido el 26/11/2026.** La versión anterior de esta nota decía que la confianza «no
  predice el acierto del docking», con Spearman −0,20. Era un error de alcance: ese −0,20 es
  contra la **RMSD de la pose**, no contra el acierto, y solo entre los 65 que Vina resuelve.
  Medido de las tres formas razonables, la respuesta cambia:

  | lo que se correlaciona con la confianza del bolsillo | Spearman | p |
  |---|---|---|
  | cuánto se desvía la pose (RMSD), en los 65 | −0,20 | 0,12 |
  | acierta o no, en los 90 | +0,24 | 0,023 |
  | acierta o no, en los 65 | +0,31 | 0,012 |

  Y por tramos de confianza, en los 65: menos de 90 → 4 de 30 (13 %); 90 a 95 → 4 de 18 (22 %);
  95 o más → 6 de 17 (35 %). Esa tendencia no es significativa comparando el tramo alto contra
  el resto (Fisher, p = 0,167).

  **Lo que se puede afirmar:** la confianza del bolsillo es una señal **débil** del acierto del
  docking, demasiado débil para usarla como semáforo (en el mejor tramo acierta 1 de cada 3, y
  con el bolsillo casi perfecto 8 de 21). No se puede afirmar que no diga nada, ni que avise.
  Tres formas legítimas de preguntarlo dan −0,20, +0,31 y p = 0,167.
- Lo parecido que sea el bolsillo tampoco decide: +0,23 (p = 0,06) contra la RMSD de la pose y
  −0,29 (p = 0,021) contra el acierto, en los 65.

### El tamaño de la caja cambia el resultado

Primera tanda con caja = ligando + 10 Å y mínimo 20 Å (`docking_caja_grande.csv`, se paró
en 83); segunda con ligando + 5 Å y mínimo 12 Å (`docking_caja_ajustada.csv`, los 90
completos). Comparación sobre los 83 que están en ambas:

| caja | acierta exp | acierta AlphaFold | mediana del error sobre el modelo |
|---|---|---|---|
| grande | 67 % | 12 % | 7,96 Å |
| ajustada | 73 % | 17 % | 4,86 Å |

Con la caja grande el ligando se iba a otro hueco de la proteína; con la ajustada se queda
en el bolsillo correcto pero mal colocado. Cambian 5 casos de fallo a acierto y 1 al revés.
La decisión de método cambia la cifra, y no aparece en ninguna diapositiva.

## Límites

- **La cifra de acierto sobre AlphaFold (17 %) es más baja que el 30–40 % que suele
  publicarse.** La dirección del resultado es sólida (el control lo respalda complejo a
  complejo), pero el número absoluto no es comparable: la preparación del receptor aquí es
  básica (Open Babel, protonación sin revisar, receptor rígido, sin minimizar el modelo) y
  PoseBusters es un conjunto deliberadamente difícil. No usar el 17 % como si fuera un dato
  de la literatura.
- Una sola cadena y un solo intento por complejo, con la caja centrada en el ligando
  experimental: en un caso real no se sabe dónde está el sitio de unión.
- AlphaFold DB v6 se generó en 2025 y pudo usar como plantilla estructuras del PDB posteriores a 2021, incluidas algunas de estas: el parecido podría estar inflado. Para evitarlo habría que generar los modelos sin plantillas.
- Una sola cadena por complejo; se ignoran cofactores, otras cadenas y el estado de oligomerización.
