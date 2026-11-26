# ¿Sirven los modelos de AlphaFold para hacer docking? Confianza del bolsillo frente a acierto de la pose

## Introducción

AlphaFold ha dejado de ser una promesa para convertirse en un punto de partida por defecto. La
base de datos AlphaFold contiene más de 200 millones de modelos, uno por secuencia conocida, y
muchos de ellos con confianza alta [@feidakis2026tale]. Esos modelos se usan cada vez más como
punto de partida para la predicción de sitios de unión, el docking molecular y el cribado
virtual, tareas en las que la forma del bolsillo de unión suele decidir el resultado
[@feidakis2026tale]. Para una parte grande del proteoma esto abre una puerta que antes estaba
cerrada: en los proteomas de once especies modelo, AlphaFold cubre de media un 44 % de residuos
más que los modelos previos de SWISS-MODEL Repository, y alrededor del 25 % de los residuos
quedan cubiertos con predicciones nuevas y de confianza, con pLDDT por encima de 70
[@akdel2022structural].

La pregunta de si esos modelos sirven para docking ya tiene varias respuestas publicadas, y
todas apuntan en la misma dirección. Scardino y colaboradores compararon el cribado de alto
rendimiento sobre modelos de AlphaFold «as-is» con el de sus estructuras correspondientes del
PDB en 22 dianas y concluyen que el rendimiento de los modelos es consistentemente peor, con
factores de enriquecimiento nulos en varias proteínas [@scardino2023good]. Díaz-Rovira y
colaboradores llegan a una recomendación práctica: los modelos de AlphaFold2 recién salidos no
son el escenario ideal para una campaña de cribado virtual, y aconsejan añadir un
post-procesado que lleve el sitio de unión hacia un modelo holo más realista
[@diazrovira2023deep]. En receptores acoplados a proteína G, el cribado virtual sobre modelos
de AlphaFold rindió algo peor que sobre las estructuras experimentales nativas, aunque mejor
que sobre los modelos por homología, de forma consistente entre herramientas de docking
[@lee2023evaluating].

El hallazgo más incómodo de esa literatura es que la calidad estructural y la utilidad para
docking no van de la mano. Karelina y colaboradores encontraron que los modelos de AlphaFold2
capturan la estructura de los bolsillos de unión mucho mejor que los modelos por homología
tradicionales, hasta el punto de que la diferencia típica entre el bolsillo de un modelo y el
de una estructura experimental es solo algo mayor que la que hay entre dos estructuras
experimentales de la misma proteína con ligandos distintos; y sin embargo las poses predichas
sobre modelos de AlphaFold2 no son significativamente más precisas que las predichas sobre
modelos tradicionales, y son mucho menos precisas que las obtenidas sobre estructuras
experimentales [@karelina2023accurately]. En la misma línea, el rendimiento del docking cae al
pasar de holo a apo y de apo a modelado, y el docking sobre modelos de AlphaFold recupera las
poses cristalográficas menos veces que el docking sobre estructuras holo «even where the
modelled pocket is accurate» [@feidakis2026tale].

Queda entonces una pregunta práctica que un investigador se hace delante del modelo que acaba
de descargar: ¿puede usar la confianza que AlphaFold le da, el pLDDT, como semáforo antes de
gastar tiempo en docking? Holcomb y colaboradores plantearon el problema para AutoDock
comparando estructuras predichas por AlphaFold2 con estructuras resueltas experimentalmente en
ejercicios de redocking [@holcomb2023evaluation]. Este trabajo aborda esa pregunta separando de
forma explícita dos cosas que suelen ir juntas y que no tienen la misma respuesta: si el pLDDT
del bolsillo avisa de la calidad geométrica de ese bolsillo, y si avisa del acierto de la pose
que se obtendrá al acoplar sobre él. Medimos las dos sobre los mismos complejos y, para la
segunda, acoplamos cada ligando dos veces, de modo que la estructura experimental actúe como
control caso por caso.

## Métodos

### Datos

Partimos del PoseBusters Benchmark set, un conjunto de complejos proteína-ligando
cristalográficos seleccionados del PDB, recientes, de alta calidad y con moléculas de tipo
fármaco; contiene solo complejos publicados desde 2021 y, por tanto, ninguno presente en el
PDBbind General Set v2020 con el que se entrenaron muchos métodos [@buttenschoenPoseBustersAIbasedDocking2024].
El artículo describe el conjunto con 308 proteínas y 308 ligandos únicos
[@buttenschoenPoseBustersAIbasedDocking2024]; la distribución que descargamos contiene 428
entradas, y es sobre esas 428 sobre las que trabajamos.

Las cadenas se asociaron a UniProt mediante la API de SIFTS y los modelos se descargaron de la
base de datos AlphaFold, versión 6.

### Medida del bolsillo

El bolsillo se define como los residuos con algún átomo pesado a menos de 6 Å del ligando en la
estructura experimental, en la cadena con más residuos de bolsillo. Se alinean las secuencias
del PDB y del modelo, se superponen los Cα del bolsillo y se mide la desviación cuadrática
media (RMSD) de los Cα y de todos los átomos pesados comunes. El código está en
`analisis/medir_bolsillos.py` y las tablas en `resultados/bolsillos.csv`.

De las 428 entradas de partida quedaron 374 complejos con modelo y bolsillo equivalente, de 339
proteínas distintas; se descartaron 54, por falta de UniProt en SIFTS, falta de modelo, falta de
equivalencia entre bolsillos, límite de la API o identidad del bolsillo por debajo del 90 %.

### Docking

Sobre una muestra de 90 complejos, uno por proteína y repartidos en cuatro tramos de pLDDT,
cada ligando se acopló dos veces con AutoDock Vina 1.2.7: sobre el modelo de AlphaFold
superpuesto por los Cα del bolsillo, y sobre la estructura experimental como control. En las
dos corridas se usó el mismo ligando y la misma caja. El control indica qué casos sabe resolver
Vina; solo en esos tiene sentido preguntar si el modelo estropea el resultado.

El ligando se preparó con Meeko y el receptor se trató como rígido, preparado con Open Babel y
sin revisar los estados de protonación ni minimizar el modelo. La caja se centró en el ligando
experimental, con exhaustiveness 16 y 9 poses por corrida. La RMSD de la pose se calculó con
corrección de simetría (`rdMolAlign.CalcRMS`) y se consideró acierto una RMSD por debajo de 2 Å,
el criterio habitual y recomendado para ligandos de tamaño normal
[@buttenschoenPoseBustersAIbasedDocking2024].

Conviene situar esta preparación frente a la de los trabajos publicados, porque no es
equivalente. Karelina y colaboradores prepararon todas las estructuras y modelos con el
Protein Preparation Wizard de Schrödinger incluyendo minimización de energía, y definieron la
rejilla con una caja interior de 15 Å de lado y una exterior de 30 Å
[@karelina2023accurately]. Feidakis y colaboradores usaron una caja cúbica centrada en el
centro de masas de los residuos del bolsillo, con un lado que depende del radio de giro de esos
residuos y acotado entre 16 y 30 Å, con una mediana de 24,1 Å [@feidakis2026tale]. Nuestra
preparación es deliberadamente básica, y eso tiene consecuencias que se discuten más abajo.

### Cifras del texto

Todas las cifras propias de este documento se recalculan con `analisis/cifras_del_texto.py`,
que las escribe en `resultados/cifras_del_texto.csv` con su procedencia. Las correlaciones de
Spearman entre la confianza o el parecido del bolsillo y el error de la pose se calculan, como
en `analisis/resumir_docking.py`, sobre los complejos que Vina resuelve con la estructura
experimental y contra la RMSD de la pose sobre el modelo.

## Resultados

### La confianza sí avisa de la calidad del bolsillo

En los 374 complejos analizados, el pLDDT medio de los residuos del bolsillo correlaciona con
la RMSD de los átomos del bolsillo frente al experimental: Spearman −0,56 (p = 1,05e-31). La
relación va en la dirección esperada y es la más fuerte que medimos en todo el trabajo.

Por tramos de confianza, el aviso es claro:

| Confianza del bolsillo | Complejos | RMSD mediana | Por debajo de 1 Å | Por debajo de 2 Å |
|---|---|---|---|---|
| Alta (pLDDT ≥ 90) | 316 | 0,95 Å | 58 % | 92 % |
| Media (pLDDT 70-90) | 58 | 1,64 Å | 12 % | 67 % |

No hay prácticamente bolsillos de confianza baja en este conjunto: el pLDDT de bolsillo más
bajo es 73,4. La figura `resultados/confianza_frente_a_bolsillo.png` muestra la relación
completa.

El aviso no es una garantía. Aun con confianza alta, 24 de los 316 bolsillos difieren 2 Å o más
del experimental.

### El docking cae mucho, y la confianza ya no avisa

Sobre los 90 complejos acoplados por duplicado, el docking acierta en el 72 % de los casos
sobre la estructura experimental y en el 17 % sobre el modelo de AlphaFold.

El control permite ir más lejos que esa comparación global. De los 65 complejos que Vina
resuelve con la estructura experimental, sobre el modelo acierta solo en el 22 %. En esos mismos
65 casos, la mediana del error de la pose es de 0,69 Å sobre la estructura experimental y de
4,67 Å sobre el modelo.

El resultado principal aparece al cruzar las dos mitades del trabajo. De los 21 complejos que
reúnen las dos condiciones favorables —bolsillo a menos de 1 Å del experimental y un caso que
Vina resuelve con la estructura buena—, el docking sobre el modelo acierta solo en 8, un 38 %.
Tener el bolsillo bien modelado no basta.

Coherentemente, ni la confianza ni el parecido del bolsillo predicen el error de la pose sobre
el modelo en esos 65 complejos: Spearman −0,20 (p = 0,12) para el pLDDT del bolsillo y 0,23
(p = 0,06) para la RMSD de átomos del bolsillo. Ninguna de las dos alcanza significación al 5 %.
El contraste con el −0,56 de la sección anterior es el núcleo de este trabajo: la misma medida
de confianza informa de una cosa y no de la otra.

El metal en el bolsillo no explica la diferencia: el acierto sobre el modelo es del 16 % en los
75 complejos sin metal y del 20 % en los 15 que lo tienen.

### El tamaño de la caja mueve la cifra

La primera tanda de docking usó una caja de ligando más 10 Å con un mínimo de 20 Å; la segunda,
ligando más 5 Å con un mínimo de 12 Å. Sobre los 83 complejos presentes en las dos tandas:

| Caja | Acierto sobre experimental | Acierto sobre AlphaFold | Error mediano sobre el modelo |
|---|---|---|---|
| Grande | 67 % | 12 % | 7,96 Å |
| Ajustada | 73 % | 17 % | 4,86 Å |

Cinco casos pasan de fallo a acierto y uno al revés. Con la caja grande el ligando se iba a otro
hueco de la proteína; con la ajustada se queda en el bolsillo correcto pero mal colocado. La
figura `resultados/docking_caja_ajustada.png` recoge la comparación. Una decisión de método que
no suele aparecer en el apartado de resultados mueve la cifra principal cinco puntos.

## Discusión

### Lo que ya estaba publicado, y dónde encaja esto

Nuestro resultado central reproduce con otro conjunto de datos y otra implementación de
AutoDock el de Holcomb y colaboradores [@holcomb2023evaluation]. Ellos encontraron que la
mayoría de las estructuras predichas
se alineaban bien con las cocristalizadas y que el pLDDT de los residuos del bolsillo
correlacionaba con ese alineamiento [@holcomb2023evaluation]. Al mismo tiempo, informan de que
ese alineamiento «is not predictive of docking performance», y describen el conjunto como «a
disparity between the structural metrics used to assess prediction quality and docking
performance» [@holcomb2023evaluation]. Lo cierran diciendo que una predicción de alta calidad
medida con la RMSD que se usa para evaluar AlphaFold2 en CASP «is not indicative of the ability
to use these structures for docking» [@holcomb2023evaluation]. Nuestras dos correlaciones,
−0,56 para la geometría del bolsillo y −0,20 para el error de la pose, son esa afirmación
medida sobre los mismos complejos y en el mismo trabajo.

El hallazgo de los 21 complejos tiene además un precedente cuantitativo preciso. Karelina y
colaboradores calcularon la precisión de la pose en función de la precisión del bolsillo y
encontraron que, a igual RMSD del bolsillo, el docking sobre una estructura experimental da
poses más precisas que sobre un modelo de AlphaFold2, con una diferencia estadísticamente
significativa para todos los valores de RMSD del bolsillo por debajo de 1,1 Å
[@karelina2023accurately]. Nuestro subconjunto de bolsillos por debajo de 1 Å cae justo en ese
tramo, y el 38 % de acierto frente al 100 % del control es la misma observación vista desde el
lado del recuento.

Hay además un mecanismo publicado que explica por qué el pLDDT no puede funcionar como semáforo
para docking. Feidakis y colaboradores describen el pLDDT del bolsillo como un indicador de
cuánto varía un bolsillo, no de en qué estado se encuentra: sobre 237.922 bolsillos, el pLDDT del bolsillo caía
a medida que aumentaba la diversidad conformacional, con Spearman −0,49, y ese efecto se
mantenía incluso entre los bolsillos modelados por encima de 90, con −0,44
[@feidakis2026tale]. Su lectura es que el pLDDT estima cuánto se parecerá el modelo a una
estructura experimental y, por tanto, registra la heterogeneidad del registro experimental sin
indicar el estado [@feidakis2026tale]. Para los modelos más alejados de ambos estados añaden
que «neither pLDDT nor the winning probability warns of these models» [@feidakis2026tale]. Si
el pLDDT no distingue entre un bolsillo apo y uno holo, no puede anticipar si el ligando
encontrará sitio, que es precisamente lo que decide el docking.

La conclusión práctica de Scardino y colaboradores coincide con nuestros 21 complejos: la
precisión de AlphaFold al reproducir la topología de la proteína y la anatomía del sitio de
unión con buenos valores de pLDDT «is not enough to guarantee that AF models can be reliably
used for molecular docking purposes» [@scardino2023good]. Ellos observan además que variaciones
muy pequeñas dentro del sitio de unión, a veces solo en las cadenas laterales, pueden tener un
impacto enorme en el factor de enriquecimiento [@scardino2023good]. Esto sugiere por qué un
bolsillo con la RMSD de átomos por debajo de 1 Å todavía puede fallar, aunque nuestros datos no
separan la contribución del esqueleto y la de las cadenas laterales.

### Qué se puede hacer en su lugar

La literatura de estas colecciones no se queda en el diagnóstico. Holcomb y colaboradores
encontraron que, en sistemas donde el docking directo sobre el modelo fracasaba, el resultado
mejoraba sustancialmente con manipulaciones sencillas del receptor: el docking flexible resolvía
choques de cadenas laterales que impedían la unión, y eliminar regiones de baja confianza
despejaba sitios de unión ocluidos [@holcomb2023evaluation]. Advierten, eso sí, de que esas
intervenciones son difíciles de aplicar de forma sistemática en algo que imite un cribado
prospectivo, aunque quien trabaje sobre una diana concreta o un conjunto pequeño sí puede
mejorar la estimación inicial [@holcomb2023evaluation]. Díaz-Rovira y colaboradores apuntan en
la misma dirección con un protocolo de induced fit: aplicado al ligando cristalográfico en el
modelo de ADRB2, partiendo de una pose inicial a 4,3 Å, recuperaron una pose casi nativa
[@diazrovira2023deep]. Su recomendación general es que los modelos de AlphaFold2 pueden servir
como buena semilla inicial para generar dianas, más que como diana directa de cribado virtual
[@diazrovira2023deep]. En el caso de los receptores acoplados a proteína G, la estrategia de
modelado del receptor y la consideración de la flexibilidad del receptor son críticas para el
docking de moléculas pequeñas y el cribado virtual [@lee2023evaluating]. Nuestro protocolo, con
receptor rígido y sin minimizar, es justamente el que esa literatura recomienda no usar, y eso
acota lo que nuestras cifras absolutas pueden decir.

También conviene no convertir «la confianza no predice el acierto del docking» en «la confianza
no sirve para nada», ni extender la conclusión a cualquier tarea sobre el bolsillo.
Bekar-Cesaretli y colaboradores describen un caso, la diana con UniProt P08709, en el que más
de la mitad de los residuos del sitio de unión estaban predichos con baja confianza y el hot
spot más fuerte del modelo se conservaba igual que en la estructura cristalográfica unida
[@bekarcesaretli2024conservation]. Su conclusión es que los modelos generados por AlphaFold2
resultan adecuados para los enfoques computacionales del descubrimiento de fármacos basado en
fragmentos, en parte porque la unión de fragmentos es mucho menos sensible a la geometría del
bolsillo y a las conformaciones de las cadenas laterales que el docking de compuestos más
grandes [@bekarcesaretli2024conservation]. La tarea importa: nuestro resultado habla del
acierto de la pose de un ligando completo, no de la detección del sitio ni del mapeo de
fragmentos.

### Límites

El primero y más importante es la preparación del receptor. Nuestro 17 % de acierto sobre
modelos de AlphaFold se obtuvo con Open Babel, estados de protonación sin revisar, receptor
rígido y modelo sin minimizar. A eso se añade la dificultad del conjunto: el PoseBusters
Benchmark set se eligió como un conjunto de prueba difícil, que no contiene ningún complejo
presente en los datos de entrenamiento de los métodos evaluados
[@buttenschoenPoseBustersAIbasedDocking2024]. La dirección del resultado es sólida porque el
control la respalda complejo a complejo, pero la cifra absoluta es nuestra y no debe citarse
como un dato de la literatura.

Dicho eso, conviene ponerla al lado de las publicadas, porque la comparación resulta menos
desfavorable de lo esperado. Holcomb y colaboradores, trabajando con 2474 complejos del
conjunto refinado de PDBbind y AutoDock-GPU v1.5.3, obtuvieron un 41 % de acierto en el
redocking sobre la estructura cristalográfica y un 17 % sobre las estructuras predichas por
AlphaFold2 [@holcomb2023evaluation]. Nuestro 17 % sobre el modelo coincide con el suyo. Lo que
difiere es el control: nuestro 72 % está por encima de su 41 % y también por encima del 58 %
que AutoDock Vina alcanzó en el PoseBusters Benchmark set atendiendo solo al criterio de RMSD
[@buttenschoenPoseBustersAIbasedDocking2024]. La explicación más probable es que nosotros
centramos la caja en el ligando experimental, lo que hace el control más fácil que un redocking
convencional; si es así, la caída del 72 % al 17 % exagera la pérdida que vería alguien que no
sepa dónde está el sitio.

Esto lleva al segundo límite. Centrar la caja en el ligando experimental es información que en
un caso real no se tiene. Škrinjar y colaboradores recuerdan que el docking se beneficia
enormemente de una definición del bolsillo, con el centro y un tamaño aproximado de caja
prefijados, y que sin esa información, en docking a ciegas, cabe esperar un rendimiento bastante
pobre [@skrinjar2026evaluating]. Nuestras cifras describen por tanto el mejor caso en cuanto a
localización del sitio.

Tercero, los modelos provienen de la versión 6 de la base de datos AlphaFold, generada en 2025,
que pudo usar como plantilla estructuras del PDB posteriores a 2021, incluidas posiblemente
algunas de las de este conjunto; el parecido entre modelo y experimental podría estar inflado.
El razonamiento general lo respaldan Buttenschoen y colaboradores, que argumentan que la
partición de entrenamiento y test basada solo en la fecha de publicación es insuficiente para
comprobar la generalización a dianas nuevas y que hay que informar de la identidad de secuencia
entre las proteínas de entrenamiento y las de test [@buttenschoenPoseBustersAIbasedDocking2024].
Evitarlo exigiría generar los modelos sin plantillas.

Cuarto, se usó una sola cadena por complejo y un solo intento por complejo, y se ignoraron los
cofactores, las demás cadenas y el estado de oligomerización. Este último punto importa porque
Holcomb y colaboradores encontraron que la naturaleza oligomérica del complejo no afectaba
sustancialmente al acierto del docking, mientras que la ausencia de un cofactor presente en el
complejo cristalográfico sí obstaculizaba las dos tareas de docking [@holcomb2023evaluation].

## Conclusión

El pLDDT del bolsillo responde bien a una pregunta y mal a otra. Avisa de si el bolsillo del
modelo se parecerá al experimental, con un Spearman de −0,56 y una mediana de 0,95 Å cuando la
confianza es alta. No avisa de si el docking sobre ese modelo dará la pose correcta: entre los
complejos que Vina resuelve con la estructura experimental, la correlación con el error de la
pose es de −0,20 y no alcanza significación. Son dos preguntas distintas y la segunda no se
responde con la primera.

El caso que lo deja más claro es el de los 21 complejos con el bolsillo a menos de 1 Å del
experimental en los que Vina funciona con la estructura buena: sobre el modelo acierta en 8. Un
bolsillo bien modelado es una condición necesaria y claramente insuficiente.

Queda un aviso de método. Cambiar solo el tamaño de la caja de búsqueda movió el acierto sobre
el modelo del 12 % al 17 % y el error mediano de 7,96 Å a 4,86 Å, sin tocar los datos ni el
programa. Cualquier cifra de acierto de docking, la nuestra incluida, hay que leerla junto al
protocolo que la produjo.
