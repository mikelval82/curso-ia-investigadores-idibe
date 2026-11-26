# Revisión del borrador

Origen de los criterios: genéricos (resultados)

Esta evaluación automática y orientativa no sustituye a la de la convocatoria o revista.

Estado: terminado

## Prioridades

1. Completar los Métodos para que el muestreo de los 90 complejos, la caja principal, la elección de la pose evaluada y los descartes puedan reproducirse, y aclarar cuál es el protocolo principal.
2. Añadir incertidumbre estadística (intervalos, test que compare las dos correlaciones, test pareado de la caja) y separar en Resultados los datos de su interpretación, reconociendo la potencia limitada de n = 65 y n = 21.
3. Ajustar el alcance de la discusión y la conclusión a un solo programa de docking con preparación básica (rebajar 'necesaria y claramente insuficiente', tratar el mecanismo como hipótesis, matizar el título) y explicitar la novedad frente a Holcomb.

## Pregunta y aportación

Nivel: bien

### Fortalezas

- La pregunta es explícita y práctica: si el pLDDT del bolsillo sirve como semáforo antes de hacer docking.
- Separa con claridad dos cuestiones, la calidad geométrica del bolsillo y el acierto de la pose, y las mide sobre los mismos complejos.
- El diseño con doble docking (modelo y estructura experimental) como control caso por caso está bien justificado.
- La conclusión resume la aportación: el pLDDT avisa de lo primero y no de lo segundo, y el tamaño de la caja condiciona las cifras.

### Carencias

- Introducción: La introducción presenta la literatura previa como unánime ('todas apuntan en la misma dirección') y Holcomb ya planteó la misma pregunta con AutoDock. La novedad real respecto a ese trabajo (otro conjunto, control pareado, cruce de las dos medidas) queda sin enunciar de forma explícita.
- Discusión: La Discusión dice que se 'reproduce' el resultado de Holcomb, pero no se precisa qué conocimiento nuevo añade este trabajo más allá de la confirmación sobre PoseBusters.

### Trabajo

Formular de manera explícita, al final de la introducción, qué aporta este estudio frente a Holcomb, Karelina y Feidakis (conjunto de datos, control pareado, cruce de las dos mitades) y declarar si el objetivo es confirmar o extender. Reflejar esa diferencia también en la discusión.

## Métodos reproducibles

Nivel: mejorable

### Fortalezas

- Indica versiones de software (Vina 1.2.7, base AlphaFold v6), parámetros (exhaustiveness 16, 9 poses, umbral de 2 Å, 6 Å para el bolsillo) y herramientas (Meeko, Open Babel, RDKit).
- Remite a scripts y tablas concretos, y a un script que recalcula todas las cifras.
- Reconoce que la preparación es básica y la compara con la de los trabajos publicados.
- Explica el flujo de exclusiones de 428 a 374 complejos.

### Carencias

- Docking: La muestra de 90 complejos se describe como 'uno por proteína y repartidos en cuatro tramos de pLDDT', pero no se dan los límites de los tramos, el criterio de selección ni la semilla aleatoria. Eso impide reproducir la muestra.
- Docking: El tamaño de la caja en los Métodos no figura; solo aparece en Resultados, con dos tandas distintas. No queda claro cuál es el protocolo principal ni por qué se eligió la caja ajustada.
- Datos: Los 54 descartes se enumeran por causas, pero sin recuento por causa. La diferencia entre 308 y 428 entradas (probablemente múltiples ligandos por complejo) no se explica.
- Medida del bolsillo: No se detalla cómo se trató la elección de 'la cadena con más residuos de bolsillo' en complejos con varias copias ni cómo se superponen modelo y estructura antes del docking en cuanto a cofactores y metales.
- Docking: No se describe cómo se eligió la pose evaluada de las 9 (¿la primera por puntuación, la mejor RMSD?). Es una decisión que cambia el acierto.

### Trabajo

Completar los Métodos con los límites de los cuatro tramos de pLDDT, el procedimiento y la semilla del muestreo, el recuento de descartes por causa, el criterio para elegir la pose evaluada, y el tamaño de caja de cada tanda indicando cuál es la principal. Aclarar el manejo de cadenas, cofactores y metales en la preparación.

## Resultados claros y con origen en los datos

Nivel: bien

### Fortalezas

- Los resultados se presentan en orden lógico: primero el bolsillo, luego el docking, luego el efecto de la caja.
- Las cifras tienen procedencia comprobada (43 con origen, ninguna sin origen) y se recalculan con un script.
- Se usa el control para acotar los casos relevantes (65 resueltos por Vina; 21 con bolsillo bueno y control resuelto).
- Se reportan p-valores y se admite que las correlaciones del docking no alcanzan significación.
- Se informa de lo que no explica la diferencia (metal) y de los casos de confianza alta con bolsillo malo (24 de 316).

### Carencias

- El docking cae mucho, y la confianza ya no avisa: Las frases 'Tener el bolsillo bien modelado no basta' y 'el núcleo de este trabajo' mezclan interpretación con resultado. Además la correlación con p = 0,06 y p = 0,12 se lee como ausencia de relación, cuando con n = 65 la potencia es limitada.
- El docking cae mucho, y la confianza ya no avisa: No se da intervalo de confianza para las proporciones (8 de 21, 22 % de 65) ni para las correlaciones. El contraste entre −0,56 y −0,20 se hace sin test y sobre poblaciones distintas (374 frente a 65).
- El tamaño de la caja mueve la cifra: Los 83 complejos de las dos tandas y los 5 frente a 1 casos que cambian son recuentos pequeños; no se presenta ningún test pareado ni se indica la sensibilidad a otros tamaños de caja.
- La confianza sí avisa de la calidad del bolsillo: Solo hay dos tramos de confianza (alta y media) porque no hay bolsillos de baja confianza, de modo que la tabla no ilustra el rango en el que el semáforo sería más útil.

### Trabajo

Separar en los resultados el dato de su lectura, moviendo las valoraciones a la discusión. Añadir intervalos de confianza para las proporciones y correlaciones clave, un test que compare las dos correlaciones o al menos un análisis sobre el mismo conjunto de complejos, y un test pareado para el efecto de la caja. Aclarar la potencia limitada de n = 65.

## Discusión proporcionada a los datos, con limitaciones

Nivel: mejorable

### Fortalezas

- La sección de límites es extensa y honesta: receptor rígido sin minimizar, caja centrada en el ligando experimental (mejor caso), posible fuga por plantillas posteriores a 2021, una sola cadena y un solo intento.
- Señala que la cifra absoluta del 17 % no debe citarse como dato de la literatura y que la dirección del resultado sí está respaldada por el control.
- Delimita el alcance: el resultado habla de la pose de un ligando completo, no de la detección del sitio ni del cribado de fragmentos.
- Reconoce que la caída de 72 % a 17 % probablemente exagera la pérdida real.

### Carencias

- Lo que ya estaba publicado, y dónde encaja esto: Se afirma que las dos correlaciones 'son esa afirmación medida sobre los mismos complejos', pero la no significación (p = 0,12) no demuestra ausencia de relación, y las dos correlaciones se calculan sobre muestras distintas.
- Lo que ya estaba publicado, y dónde encaja esto: Se propone el mecanismo de Feidakis (pLDDT como indicador de variabilidad) para explicar los resultados, pero este estudio no lo contrasta con datos propios; queda como hipótesis.
- Límites: La preparación básica del receptor (protonación, rigidez) puede ser lo que explica el fallo y no el modelo en sí. El texto lo reconoce, pero mantiene que la dirección es sólida y titula el trabajo en términos generales sobre AlphaFold.
- Conclusión: 'Condición necesaria y claramente insuficiente' va más allá de los datos: no se ha mostrado necesidad, y la insuficiencia está medida con un solo programa de docking y un protocolo simple.
- Límites: La posible inflación por plantillas se plantea como riesgo sin cuantificarla ni comprobar qué entradas del conjunto estaban en la base de plantillas.

### Trabajo

Rebajar las afirmaciones de la conclusión y la discusión a lo que respalda un único programa (Vina), un protocolo básico y n = 65 o 21. Presentar el mecanismo de Feidakis y el efecto de las cadenas laterales como hipótesis. Valorar si la preparación del receptor, con un análisis de sensibilidad (por ejemplo, minimización o protonación), puede apoyar la afirmación de que la dirección es robusta, y matizar el título.

## Relación con la literatura

Nivel: bien

### Fortalezas

- Hay un diálogo sustantivo con Holcomb, Karelina, Feidakis, Scardino, Díaz-Rovira, Lee, Bekar-Cesaretli, Škrinjar y Buttenschoen, con coincidencias y diferencias concretas.
- Compara cifras propias con las de Holcomb (17 % frente a 17 %; 72 % frente a 41 %) y con Vina en PoseBusters (58 %), y propone una explicación de la diferencia.
- Compara la preparación con la de Karelina y Feidakis, y señala dónde no es equivalente.
- Incluye literatura que matiza la conclusión (fragmentos, Bekar-Cesaretli).
- La verificación sitúa 36 frases como apoyadas y una como parcial; las 10 citas están en la colección y no hay obras sin citar.

### Carencias

- Introducción: Hay una frase señalada en la verificación como parcialmente apoyada; el autor debe localizarla y ajustar la atribución a lo que la fuente dice.
- Lo que ya estaba publicado, y dónde encaja esto: Se dice que el resultado 'reproduce' el de Holcomb y que coincide con Scardino, y la comparación se queda en la coincidencia. Se dedica poco espacio a las diferencias de diseño (docking con AutoDock-GPU sobre PDBbind frente a Vina sobre PoseBusters) que limitan esa equivalencia.
- Límites: La comparación 17 % con 17 % se presenta como coincidencia entre conjuntos y programas muy distintos; la afinidad de cifras puede ser casual y no debería leerse como validación.

### Trabajo

Revisar la frase señalada como parcialmente apoyada y ajustar su redacción a lo que dice la fuente. Ampliar la comparación con Holcomb y Karelina para indicar qué diferencias de diseño pueden explicar o no la coincidencia, y tratar la igualdad de cifras como un dato anecdótico, no como validación.
