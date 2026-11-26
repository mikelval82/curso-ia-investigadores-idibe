# Qué hemos hecho exactamente, explicado desde cero

Documento de trabajo para preparar la sesión 4. Explica el caso de AlphaFold sin dar por
sabida la biología. No es material para participantes tal cual, pero sirve de base para el
guion y para las notas de las diapositivas.

---

## 1. El problema del mundo real

Casi todos los medicamentos funcionan igual: son moléculas pequeñas que se pegan a una
proteína del cuerpo y le cambian el comportamiento. El ibuprofeno se pega a una enzima
llamada COX y la bloquea; por eso baja la inflamación.

La analogía clásica, imperfecta pero útil:

- **La proteína es una cerradura.** Es una molécula grande, con una forma tridimensional muy
  concreta, y tiene un hueco en su superficie: el **sitio de unión** o **bolsillo**.
- **El fármaco es la llave.** Una molécula mucho más pequeña que encaja en ese hueco.

Si quieres diseñar un fármaco nuevo, necesitas dos cosas:

1. **Saber la forma exacta de la cerradura.** Hasta hace poco esto era carísimo y lento.
2. **Probar qué llaves encajan.** Idealmente en el ordenador, antes de gastar dinero en el
   laboratorio.

Nuestro análisis va sobre si el paso 2 funciona cuando el paso 1 lo ha hecho una IA.

---

## 2. Los conceptos, uno a uno

### Proteína

Una cadena de piezas llamadas **aminoácidos**. Hay 20 tipos distintos, como un alfabeto de
20 letras. Una proteína típica tiene entre 100 y 1.000 aminoácidos encadenados.

Lo importante: **esa cadena no se queda estirada, se pliega sobre sí misma** y adopta una
forma tridimensional concreta, siempre la misma para una proteína dada. Es como si un collar
de cuentas se plegara siempre exactamente de la misma manera al soltarlo.

```
La secuencia (fácil de saber, se lee del ADN):
   M-K-V-L-A-T-G-G-S-E-R-...

La forma plegada en 3D (difícil de saber, y es la que importa):
        ___
      /     \
     |   ()  |   <- el hueco () es el bolsillo:
      \ ___ /       ahí se mete el fármaco
```

El problema de pasar de lo primero a lo segundo se llamó durante 50 años **el problema del
plegamiento de proteínas**. Era uno de los grandes problemas abiertos de la biología.

### Cómo se sabía la forma: cristalografía

El método clásico consiste en cristalizar la proteína y bombardearla con rayos X. Del patrón
de difracción se reconstruyen las posiciones de los átomos. Funciona muy bien, pero puede
costar meses o años por proteína, y muchas proteínas sencillamente no cristalizan.

Los resultados se depositan en una base de datos pública mundial, el **PDB** (Protein Data
Bank), con unas 220.000 estructuras. Cada una tiene un código de cuatro caracteres: `7NP6`,
`5SAK`, `6ZR8`. Cuando en este documento digo **«estructura experimental»**, me refiero a una
de estas: medida en el laboratorio, es nuestra referencia de la verdad.

### AlphaFold

En 2020, DeepMind presentó **AlphaFold 2**, una IA que predice la forma plegada a partir de
la secuencia, y lo hace muy bien. Fue un hito histórico: le dieron el Nobel de Química en
2024. Después publicaron **AlphaFold DB**, una base de datos con la forma predicha de más de
200 millones de proteínas, gratis.

Dos matices que resultan centrales para lo que hemos hecho:

- AlphaFold da **una sola forma** por proteína. Las proteínas reales se mueven y cambian de
  forma, sobre todo al unir un fármaco.
- AlphaFold predice **solo la proteína**. No incluye los iones metálicos, cofactores ni otras
  moléculas que muchas proteínas llevan pegadas y que a veces son esenciales para su función.

### pLDDT: cuánta confianza tiene AlphaFold

AlphaFold no solo da la forma, también da **una nota de confianza para cada aminoácido**, de
0 a 100, llamada **pLDDT**. Es su propia autoevaluación:

| pLDDT | Interpretación habitual |
|---|---|
| 90 o más | muy fiable |
| 70 a 90 | fiable en lo general |
| 50 a 70 | dudoso |
| menos de 50 | probablemente no tiene forma fija |

Esta nota es clave en la práctica: mucha gente la usa como semáforo para decidir si se fía
del modelo. **Una de nuestras dos preguntas es si ese semáforo funciona.**

### Ligando

El nombre técnico de la molécula pequeña que se une a la proteína. En nuestros datos, los
ligandos son fármacos o candidatos a fármaco.

### Docking (acoplamiento molecular)

Un programa de ordenador que, dada la forma de la proteína y la del ligando, intenta
**predecir cómo encaja el ligando en el bolsillo**: en qué posición, con qué orientación y
con qué forma retorcida. Prueba millones de combinaciones y puntúa cada una.

Hemos usado **AutoDock Vina**, el programa de docking gratuito más utilizado del mundo.

```
   Entrada 1: la proteína        Entrada 2: el ligando
        ___                            o-o
      /     \                         /   \
     |   ()  |                       o     o
      \ ___ /

   Vina prueba millones de posiciones dentro de una "caja" de búsqueda
                         |
                         v
   Salida: la postura (pose) que cree correcta, con una puntuación
```

### Pose y RMSD: cómo se mide el acierto

La **pose** es la postura concreta que propone el programa. Para saber si acertó, la
comparamos con la postura real, la que se midió en el laboratorio.

La medida se llama **RMSD** y se expresa en **ångströms (Å)**. Un ångström es la diezmilmillonésima
parte de un metro, más o menos el tamaño de un átomo. El RMSD es, en esencia, **la distancia
media entre cada átomo de la pose predicha y el mismo átomo en la postura real**.

```
   RMSD = 0,5 Å   la pose está prácticamente encima de la real
   RMSD = 2 Å     ligeramente desplazada, pero en el sitio correcto
   RMSD = 8 Å     el ligando está en otro lugar; la predicción es inútil
```

**Por convenio, en todo este campo se considera que el docking ha acertado si el RMSD es
menor de 2 Å.** Ese umbral aparece en todos los artículos y es el que usamos.

### La caja de búsqueda

Vina no busca por toda la proteína: hay que darle una **caja**, una región del espacio donde
buscar. Es un parámetro que decide quien hace el análisis, y resultó importante.

---

## 3. La hipótesis

La pregunta de partida venía de la sesión 2, donde se refinaba una pregunta vaga («¿sirve
AlphaFold para diseñar fármacos?») hasta algo comprobable. Quedó en dos preguntas encadenadas:

> **Pregunta 1.** ¿La confianza de AlphaFold en el bolsillo (el pLDDT medio de los aminoácidos
> que lo forman) indica si ese bolsillo está bien predicho?
>
> **Pregunta 2.** Y aunque el bolsillo esté bien predicho, ¿funciona el docking sobre el modelo
> igual que sobre la estructura experimental?

La hipótesis implícita, la que mucha gente da por buena, sería: *si AlphaFold tiene confianza
alta en el bolsillo, el modelo sirve para hacer docking.*

Es justo esa cadena de razonamiento la que queríamos poner a prueba.

---

## 4. Los datos

### PoseBusters

El conjunto de datos central. Es un **banco de pruebas** publicado en 2024 (Buttenschoen et
al., *Chemical Science*) con **428 complejos proteína-ligando**. Un «complejo» es una
estructura experimental del PDB en la que se ve a la vez la proteína **y** el ligando pegado
en su sitio.

Dos detalles de su diseño que importan:

- Todas las estructuras son **de 2021 en adelante**. Esto es deliberado: AlphaFold 2 se
  entrenó con datos anteriores a 2021, así que son casos que el modelo no pudo memorizar.
- Están **filtradas por calidad**: sin errores químicos, ligandos razonables, buena resolución.

Lo descargamos de Zenodo y comprobamos su huella digital (`sha256`) para asegurarnos de que el
archivo es exactamente el publicado. Cada complejo trae dos archivos: la proteína (`.pdb`) y
el ligando (`.sdf`) en su posición real.

### Los modelos de AlphaFold

Para cada complejo hay que encontrar el modelo de AlphaFold de esa misma proteína. Esto no es
inmediato, porque el PDB identifica las cosas por estructura y AlphaFold por proteína. El
puente son dos recursos públicos:

- **UniProt**, el catálogo mundial de proteínas, donde cada una tiene un identificador
  (`P11838`, `P51449`...).
- **SIFTS**, un servicio del laboratorio europeo de bioinformática que dice qué cadena de qué
  estructura del PDB corresponde a qué entrada de UniProt.

Con el identificador de UniProt, descargamos el modelo de AlphaFold DB por su API.

```
  Complejo de PoseBusters          SIFTS              AlphaFold DB
   5SAK + ligando ZRY    ---->   UniProt P11838  ---->  modelo predicho
   (medido en laboratorio)                              (predicho por IA)
```

De los 428 complejos iniciales llegamos a **374 utilizables**. Se perdieron 54: unos sin
correspondencia en UniProt, otros sin modelo en AlphaFold DB, otros donde las secuencias no
casaban bien. Esto está registrado en el `LEEME.md`, porque **las pérdidas hay que contarlas**:
si no, alguien podría pensar que analizamos los 428.

---

## 5. El análisis, paso a paso

### Parte 1: ¿está bien hecho el bolsillo? (374 complejos)

**Paso 1. Definir el bolsillo.** En la estructura experimental tenemos al ligando metido en su
sitio. Decimos que un aminoácido «forma parte del bolsillo» si tiene algún átomo **a menos de
6 Å del ligando**. Son los aminoácidos que lo están tocando o casi. Típicamente salen entre 15
y 30.

**Paso 2. Encontrar esos mismos aminoácidos en el modelo de AlphaFold.** Aquí hay un detalle
técnico: la estructura experimental suele ser un fragmento de la proteína, con numeración
propia, mientras que el modelo de AlphaFold es la proteína entera. Hay que **alinear las dos
secuencias** (el mismo tipo de alineamiento que se usa para comparar dos textos parecidos) y
emparejar aminoácido con aminoácido.

**Paso 3. Superponer.** El modelo y la estructura están en sistemas de coordenadas distintos,
como dos fotos de la misma casa tomadas desde ángulos diferentes. Hay que girarlos y
desplazarlos hasta que encajen lo mejor posible. Esto se hace con un procedimiento matemático
llamado **algoritmo de Kabsch**, que encuentra la rotación óptima. Lo importante: **superpusimos
usando solo los aminoácidos del bolsillo**, no la proteína entera. Queríamos comparar el
bolsillo, no el conjunto.

**Paso 4. Medir.** Dos números por complejo:

- el **pLDDT medio del bolsillo**: cuánta confianza tiene AlphaFold justo ahí;
- el **RMSD del bolsillo**: cuánto se diferencia del experimental, en ångströms.

**Resultado de la parte 1:**

| Confianza en el bolsillo | Complejos | Diferencia típica | Menos de 2 Å |
|---|---|---|---|
| Alta (90 o más) | 316 | 0,95 Å | 92 % |
| Media (70 a 90) | 58 | 1,64 Å | 67 % |

La correlación (Spearman −0,56) dice que **sí hay relación: a más confianza, mejor bolsillo**.
Pero no es perfecta: con confianza alta, 24 de 316 bolsillos se desvían 2 Å o más.

Hasta aquí, la respuesta a la pregunta 1 es «sí, con matices». Y aquí es donde mucha gente se
habría parado, concluyendo que los modelos con pLDDT alto sirven.

### Parte 2: ¿funciona el docking? (90 complejos)

Esta es la parte que de verdad responde a la pregunta original, y la que cambia la conclusión.

**La idea central: cada complejo se acopla dos veces.**

```
   Mismo ligando, misma caja, mismo programa, dos receptores distintos:

   (A) sobre el MODELO DE ALPHAFOLD   --> ¿acierta?
   (B) sobre la ESTRUCTURA EXPERIMENTAL --> ¿acierta?     <- el CONTROL
```

**Por qué el control es imprescindible.** Si solo hiciéramos (A) y fallara, no sabríamos a
quién echarle la culpa: ¿al modelo de AlphaFold, o a que Vina simplemente no sabe resolver ese
caso? Haciendo también (B), con la estructura buena, lo separamos:

- si (B) acierta y (A) falla → **la culpa es del modelo**;
- si (B) también falla → es un caso que Vina no sabe resolver, y no cuenta contra AlphaFold.

Este es, a mi juicio, el concepto más valioso de todo el ejercicio para la clase: **un número
solo significa algo cuando tienes con qué compararlo.**

**Los pasos concretos:**

1. **Muestra.** De los 374, cogimos 90: una sola entrada por proteína (para que las proteínas
   muy repetidas no pesen de más) y repartidas en cuatro tramos de confianza.
2. **Colocar el modelo en su sitio.** Con la superposición de la parte 1, movemos el modelo de
   AlphaFold al sistema de coordenadas de la estructura experimental. Así el ligando real sirve
   de referencia para los dos dockings.
3. **Preparar las moléculas.** Los programas de docking necesitan un formato propio
   (`PDBQT`) con los hidrógenos añadidos y las cargas eléctricas estimadas. Para el ligando
   usamos **Meeko**; para la proteína, **Open Babel**.
4. **Definir la caja**, centrada en donde está el ligando real.
5. **Acoplar** con Vina, pidiendo 9 posturas candidatas.
6. **Medir el RMSD** de la mejor postura frente a la real. Con una corrección importante: si
   la molécula es simétrica (por ejemplo, un anillo de benceno que da igual cómo se gire), hay
   que tenerlo en cuenta o el RMSD sale falsamente malo.

**Resultado de la parte 2 (90 complejos):**

| | Acierta sobre la experimental | Acierta sobre AlphaFold |
|---|---|---|
| Los 90 | 72 % | 17 % |
| Los 65 que Vina resuelve bien | — | 22 % |
| Y además con el bolsillo bien hecho | — | **38 %** (8 de 21) |

---

## 6. Qué significa todo esto

**El hallazgo principal.** Cogemos los casos en que todo juega a favor: el bolsillo del modelo
es casi idéntico al real (menos de 1 Å) **y** Vina sabe resolver ese caso con la estructura
buena. Son 21 complejos. Sobre el modelo de AlphaFold acierta en 8.

> **Un bolsillo bien predicho no garantiza que el docking funcione.**

La explicación probable es la que apuntábamos al principio: AlphaFold da **una** forma, y
tiende a predecir la proteína tal como está **sin el fármaco puesto**. Las cadenas laterales de
los aminoácidos del bolsillo están colocadas de otra manera, a menudo ocupando parte del hueco.
El bolsillo «está», y medido a grandes rasgos se parece mucho, pero en el detalle fino que
necesita el docking no está abierto como debería.

La cerradura tiene la forma correcta vista de lejos, pero por dentro los pernos están en otra
posición, y la llave no entra.

**El hallazgo secundario, y la corrección que me hizo falta.** La confianza de AlphaFold
correlaciona bien con la calidad del bolsillo (−0,56). Sobre el acierto del docking, la primera
versión de estas notas decía que **no** correlacionaba, con un −0,20 «no significativo». Eso
estaba mal, y el error es instructivo: el −0,20 no mide el acierto, mide **cuánto se desvía la
pose**, y solo entre los 65 complejos que Vina resuelve. Preguntado por el acierto —acierta o no
acierta— sale +0,31 con p = 0,012 en esos 65, y +0,24 con p = 0,023 en los 90. Pero si se
comparan los tramos de confianza con una prueba exacta, la tendencia (13 %, 22 %, 35 %) deja de
ser significativa (p = 0,167).

Tres formas legítimas de hacer la misma pregunta dan «nada», «sí» y «nada». Lo honesto es lo
que aguanta en las tres: la confianza es una señal **débil**, y demasiado débil para decidir con
ella. En el mejor tramo acierta 1 de cada 3, y con el bolsillo casi perfecto, 8 de 21. Como
semáforo no sirve; decir que no dice nada también sería falso.

Dos lecciones, entonces. Una sobre AlphaFold: el pLDDT responde bien a una pregunta y mal a
otra, y es fácil extender indebidamente la conclusión de A a B. Y otra sobre el análisis: la
cifra −0,20 era correcta y estaba bien calculada; lo que estaba mal era **la frase que la
describía**. Un error así no lo encuentra quien revisa los números, sino quien tiene que
explicar de dónde sale cada uno.

**El tercer hallazgo, metodológico.** Al cambiar solo el tamaño de la caja de búsqueda, el
acierto pasó del 12 % al 17 %, y el error típico de 8 Å a 4,9 Å. La misma pregunta, los mismos
datos y el mismo programa dan respuestas distintas según una decisión que no suele aparecer en
ningún resumen. Con la caja grande el ligando se escapaba a otro hueco de la proteína; con la
ajustada se queda en el bolsillo correcto, pero mal colocado.

---

## 7. Lo que este análisis NO demuestra

Esto es tan importante como lo anterior, y conviene tenerlo a mano por si alguien pregunta.

- **El 17 % no es un dato publicable.** La literatura da entre un 30 % y un 40 % para docking
  sobre modelos de AlphaFold. Nuestra preparación del receptor es básica: protonación sin
  revisar, receptor rígido, modelo sin minimizar. La **dirección** del resultado es sólida
  porque el control la respalda caso por caso, pero la cifra absoluta es nuestra, no de nadie
  más.
- **No hemos demostrado que AlphaFold no sirva para descubrir fármacos.** Hemos medido una
  manera concreta de usarlo, la más ingenua: bajar el modelo y acoplar directamente. Existen
  métodos que lo usan mejor, con flexibilidad de las cadenas laterales o refinando el modelo.
- **Posible ventaja injusta para AlphaFold en la parte 1.** Los modelos que descargamos son de
  2025 y pudieron usar como plantilla estructuras del PDB posteriores a 2021, quizá algunas de
  estas mismas. Si acaso, eso haría que los bolsillos se parecieran **más** de lo debido, lo
  que refuerza la conclusión en vez de debilitarla.
- **Una sola cadena por complejo**, ignorando otras cadenas y cofactores.
- **Sabíamos dónde está el bolsillo.** Centramos la caja en el ligando real. En un caso real no
  tendrías esa información, y el problema sería bastante más difícil.

---

## 8. Por qué esto vale para la sesión 4

El recorrido completo es el argumento:

1. Una pregunta vaga («¿sirve AlphaFold para diseñar fármacos?»).
2. Refinada hasta algo medible, con una hipótesis escrita y su condición de refutación (sesión 2).
3. Un primer análisis que da una respuesta tranquilizadora: la confianza funciona (−0,56).
4. **Un segundo análisis que demuestra que esa respuesta no contestaba la pregunta.**
5. Un control que convierte un número suelto en una conclusión defendible.
6. Un detalle de método que mueve el resultado y que nadie menciona: el tamaño de la caja.
7. **Un error en estas notas, encontrado al escribir el documento** (26/11/2026). El −0,20 era
   correcto y estaba en el CSV; lo que estaba mal era la frase que lo describía. No lo detectó
   el juez de citas ni el revisor automático: lo detectó tener que decir de dónde salía cada
   cifra.
8. **Y un segundo giro al leer la literatura.** El número que parecía flojo (nuestro 17 % sobre
   el modelo) coincide con el 17 % de Holcomb. El que estaba inflado era el que parecía
   sólido: el control del 72 %, porque la caja se centró en el ligando experimental. La
   literatura no corrigió el número sospechoso; cambió cuál era el sospechoso.
9. Unos límites escritos, con lo que las cifras absolutas no pueden decir.

Ninguno de los pasos 4 a 9 sale de preguntarle a un chatbot. Salen de tener los datos delante,
de comparar con lo publicado y de desconfiar del propio resultado. Eso es exactamente lo que el
curso quiere enseñar. Y el paso 7 es el que más vale en clase, porque el error era del profesor
y no de un artículo publicado.
