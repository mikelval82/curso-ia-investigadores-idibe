# Plan del documento

**Título:** ¿Sirven los modelos de AlphaFold para hacer docking? Confianza del bolsillo frente a acierto de la pose
**Tipo:** resultados · **Idioma:** es
**Colección:** AlphaFold · bolsillos de unión / Prueba sesion 4 (10 obras, 10 con PDF, 329 pasajes)
**Estado:** plan y abstract aprobados por el usuario el 26/11/2026. Borrador escrito en
`borrador/documento.md`. Los tres puntos de «Puntos a resolver» quedaron resueltos: se cita el
308 del artículo y las 428 entradas van como cifra propia; el límite se reescribió alrededor de
la coincidencia con el 17 % de Holcomb; Škrinjar y Akdel se usan donde el plan preveía.

**Corrección encontrada al escribir:** las notas de `materiales/ANALISIS_LEEME.md` presentan el
−0,20 y el 0,23 como correlaciones entre la confianza (o el parecido del bolsillo) y «el acierto
del docking». No es eso lo que calcula `analisis/resumir_docking.py`: son correlaciones contra la
**RMSD de la pose** sobre el modelo, y solo entre los 65 complejos que Vina resuelve con la
estructura experimental. El documento lo dice con ese alcance. Calculada contra el acierto
binario sobre los 90, la correlación con el pLDDT sale distinta, así que el alcance importa.
Todas las cifras del texto se recalculan ahora con `analisis/cifras_del_texto.py` →
`resultados/cifras_del_texto.csv`.

## Objetivo

Separar dos preguntas que suelen ir juntas y que no tienen la misma respuesta:

1. ¿Avisa la confianza de AlphaFold (pLDDT del bolsillo) de si el bolsillo del modelo se parece
   al experimental? → **Sí** (Spearman −0,56).
2. ¿Avisa de si el docking sobre ese modelo va a dar la pose correcta? → **No**
   (Spearman −0,20, p = 0,12), ni siquiera cuando el bolsillo es casi idéntico (< 1 Å: 8 de 21).

El control sobre la estructura experimental es lo que hace sólida la dirección del resultado:
dice caso por caso qué complejos sabe resolver Vina, y solo en esos tiene sentido preguntar si
el modelo estropea el resultado.

## Secciones

### Introducción

**Sostiene:** AlphaFold da un modelo para casi cualquier secuencia y esos modelos se usan ya
como punto de partida para docking y cribado virtual; la literatura coincide en que el docking
sobre modelos rinde peor que sobre estructuras experimentales, y en que una buena geometría del
bolsillo no garantiza una buena pose. Falta por tanto una pregunta práctica: ¿puede el usuario
usar la confianza que AlphaFold le da como semáforo antes de hacer docking?

**Fuentes:**
- `feidakis2026tale` — AFDB da un modelo por proteína para más de 200 millones de secuencias, y
  esos modelos se usan como punto de partida para detección de sitios, docking y cribado; el
  rendimiento cae de holo a apo a modelado, «even where the modelled pocket is accurate».
- `akdel2022structural` — cobertura que añade AF2 sobre los modelos previos y qué fracción de
  residuos es de confianza alta; correlación entre pLDDT y RMSD frente al modelo de referencia.
- `scardino2023good` — el rendimiento de los modelos AF «as-is» en HTD es consistentemente peor
  que el de las estructuras del PDB, con factores de enriquecimiento nulos en varios casos.
- `karelina2023accurately` — en GPCR los bolsillos de AF2 son mucho mejores que los de modelado
  por homología, pero las poses no son significativamente mejores que las de los modelos
  tradicionales y son mucho peores que con estructura experimental.
- `diazrovira2023deep` — los modelos AF2 «out-of-the-box» no son el escenario ideal para cribado
  virtual; recomiendan post-procesado para llevar el sitio hacia un modelo holo.
- `holcomb2023evaluation` — plantea exactamente la pregunta de este documento sobre AutoDock.

### Métodos

**Sostiene:** de dónde salen los datos (PoseBusters), cómo se define y se mide el bolsillo, y
cómo está montado el docking por duplicado con la estructura experimental como control.

**Fuentes y cifras propias:**
- `buttenschoenPoseBustersAIbasedDocking2024` — qué es el PoseBusters Benchmark set: complejos
  del PDB publicados desde 2021, seleccionados para que no estén en PDBbind General Set v2020.
  **Ojo (ver «Puntos a resolver» 1):** el PDF dice 308 proteínas y 308 ligandos, no 428.
- Cifras propias, sin cita, de `resultados/bolsillos.csv` y `resultados/resumen_por_confianza.csv`:
  428 entradas de partida, 374 complejos con modelo y bolsillo equivalente, 339 proteínas
  distintas, 54 descartados y por qué.
- Cifras propias de `resultados/docking_caja_ajustada.csv` y
  `resultados/resumen_docking_ajustada.csv`: muestra de 90 complejos, uno por proteína,
  repartidos en cuatro tramos de pLDDT; AutoDock Vina 1.2.7, exhaustiveness 16, 9 poses, RMSD
  con corrección de simetría; caja centrada en el ligando experimental; receptor rígido.
- Comparación con el protocolo ajeno, con cita: `karelina2023accurately` prepara los receptores
  con minimización de energía y caja interior de 15 Å; `feidakis2026tale` usa una caja cuyo lado
  depende del radio de giro del bolsillo, acotada a 16–30 Å. Sirve para situar honestamente
  nuestra preparación básica (Open Babel, protonación sin revisar, sin minimizar).

### Resultados

**Sostiene** (todo cifra propia, sin cita; de `resultados/`):

1. **La confianza sí avisa de la calidad del bolsillo.** Spearman −0,56 entre pLDDT del bolsillo
   y RMSD de átomos del bolsillo. pLDDT ≥ 90: 316 complejos, mediana 0,95 Å, 92 % por debajo de
   2 Å. pLDDT 70–90: 58 complejos, mediana 1,64 Å, 67 % por debajo de 2 Å. Casi no hay bolsillos
   de confianza baja (mínimo 73). Figura `confianza_frente_a_bolsillo.png`.
2. **Aun con confianza alta hay fallos:** 24 de 316 bolsillos difieren 2 Å o más (ejemplo RORγt,
   pLDDT 94 y unos 5,8 Å).
3. **El docking cae mucho:** 72 % de acierto sobre la experimental frente a 17 % sobre el modelo
   (90 complejos). En los 65 que Vina resuelve con la estructura buena, 22 % sobre el modelo.
   Mediana del error en esos 65: 0,69 Å frente a 4,67 Å.
4. **Hallazgo principal:** de los 21 complejos con bolsillo < 1 Å *y* que Vina resuelve con la
   estructura buena, sobre el modelo acierta solo en 8 (38 %).
5. **La confianza no predice el acierto del docking:** Spearman −0,20 (p = 0,12); lo parecido
   que sea el bolsillo tampoco (0,23; p = 0,06). Ninguna de las dos es significativa.
6. **El metal en el bolsillo no lo explica:** 16 % sin metal, 20 % con metal.
7. **El tamaño de la caja mueve la cifra:** sobre los 83 complejos comunes, caja grande 12 % y
   caja ajustada 17 % (mediana del error 7,96 Å frente a 4,86 Å). Figura
   `docking_caja_ajustada.png`. Una decisión de método cambia el resultado publicable.

### Discusión

**Sostiene:** nuestro resultado reproduce y explica lo que ya está publicado, y la pieza que
aporta es el contraste directo entre las dos correlaciones medidas sobre los mismos complejos.

**Fuentes:**
- `holcomb2023evaluation` — es el espejo más directo. Encontraron que el pLDDT de los residuos
  del bolsillo correlaciona con el alineamiento del bolsillo (Fig. 1c), pero que ese
  alineamiento «is not predictive of docking performance» (Fig. 1b), y hablan de «a disparity
  between the structural metrics used to assess prediction quality and docking performance».
  Añaden que una predicción buena según la RMSD de CASP «is not indicative of the ability to use
  these structures for docking». Cifras suyas: 41 % sobre la estructura cristalográfica y 17 %
  sobre los modelos AF2, en 2474 complejos de PDBbind con AutoDock-GPU.
- `karelina2023accurately` — su Figura 5 es nuestro hallazgo principal visto desde otro ángulo:
  a igual RMSD del bolsillo, el modelo da peores poses que la estructura experimental, y la
  diferencia es significativa «for all binding pocket RMSD values below 1.1 Å». Esto es
  exactamente el tramo de nuestros 21 complejos de < 1 Å.
- `feidakis2026tale` — da el mecanismo de por qué la confianza no sirve de semáforo: el pLDDT
  del bolsillo refleja cuánto varía el sitio entre sus estructuras experimentales (ρ = −0,49),
  no en qué estado está, y eso se mantiene incluso por encima de 90 (ρ = −0,44). Para los
  modelos más alejados de ambos estados, «neither pLDDT nor the winning probability warns».
- `scardino2023good` — su conclusión encaja con nuestro punto 4: buena topología y buenos
  valores de pLDDT en el sitio «is not enough to guarantee that AF models can be reliably used
  for molecular docking purposes»; las cadenas laterales pequeñas bastan para arruinar el
  enriquecimiento.
- `holcomb2023evaluation` + `diazrovira2023deep` — qué hacer en su lugar: cadenas laterales
  flexibles, borrar regiones de baja confianza que ocluyen el sitio, o post-procesado tipo
  induced-fit para llevar el sitio al estado holo.
- `bekarcesaretli2024conservation` — matiz en la otra dirección: hay casos con más de la mitad
  de los residuos del sitio en baja confianza en los que el hot spot sí se conserva. Útil para
  no convertir «la confianza no predice el docking» en «la confianza no sirve para nada».
- `lee2023evaluating` — en GPCR el cribado sobre modelos de AlphaFold rinde algo peor que sobre
  estructuras experimentales pero mejor que sobre modelos por homología; la flexibilidad del
  receptor es crítica. Matiza que el problema es de protocolo tanto como de modelo.
- `holcomb2023evaluation` — también para el límite del cofactor: los cofactores tuvieron un
  efecto más fuerte que la oligomerización en el acierto del docking.

**Límites, con sus cifras propias y sin maquillar:**
- Preparación del receptor básica (Open Babel, protonación sin revisar, rígido, sin minimizar);
  PoseBusters es un conjunto deliberadamente difícil. La dirección es sólida por el control; la
  cifra absoluta es nuestra y no es un dato de la literatura.
- Una cadena, un intento, caja centrada en el ligando experimental: en un caso real no se sabe
  dónde está el sitio. `skrinjar2026evaluating` sirve aquí: el docking se beneficia mucho de
  tener el centro y el tamaño de la caja predefinidos, y a ciegas se espera que rinda bastante
  peor.
- AlphaFold DB v6 se generó en 2025 y pudo usar como plantilla estructuras posteriores a 2021:
  el parecido podría estar inflado. `buttenschoenPoseBustersAIbasedDocking2024` apoya el
  razonamiento general de que la partición por fecha no basta y hay que informar de la identidad
  de secuencia entre entrenamiento y test.

### Conclusión

El pLDDT del bolsillo es un buen indicador de la geometría del bolsillo y un mal indicador del
acierto del docking: son dos preguntas distintas y la segunda no se responde con la primera. Un
bolsillo por debajo de 1 Å no basta. Para la clase, el añadido: la cifra depende de decisiones
de método (el tamaño de la caja) que no suelen aparecer en la diapositiva.

## Puntos a resolver antes de escribir

1. **PoseBusters: 428 o 308.** Nuestro material habla de «428 complejos» y `bolsillos.csv` tiene
   428 filas, pero el PDF de Buttenschoen describe el PoseBusters Benchmark set con 308
   proteínas y 308 ligandos únicos. Atribuir el 428 a esa cita no se sostendría en la
   comprobación. Propuesta: citar los 308 del artículo y decir que partimos de la distribución
   de Zenodo, con sus 428 entradas, como cifra propia sin cita. **Decisión tuya.**

2. **El 17 % no es anómalo: es el mismo 17 % de Holcomb.** El material dice que nuestro 17 % es
   más bajo que «el 30–40 % que suele publicarse». En estas 10 obras no hay ningún pasaje que dé
   un 30–40 % para docking sobre modelos de AlphaFold; esa frase quedaría sin fuente (`[@?]`).
   Lo que sí hay es Holcomb: **41 % sobre la estructura cristalográfica y 17 % sobre los modelos
   AF2**. Es decir, nuestra cifra sobre AlphaFold coincide con la suya. Lo que difiere es el
   control: nuestro 72 % es más alto que su 41 % y que el 58 % de AutoDock Vina en el PoseBusters
   Benchmark set (`buttenschoenPoseBustersAIbasedDocking2024`), seguramente porque centramos la
   caja en el ligando experimental. Propuesta: reescribir el límite así, que es más fuerte y más
   honesto que el original. **Decisión tuya.**

3. **Obras que quedan sin usar o casi:** `skrinjar2026evaluating` (cofolding, solo como apoyo del
   límite de la caja) y `akdel2022structural` (solo en la introducción). Si quieres darles más
   peso, dilo; si no, no se fuerzan.
