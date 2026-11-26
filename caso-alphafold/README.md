# El caso de AlphaFold: una pregunta que atraviesa el curso

Esta carpeta guarda, **congelado**, el caso que sostiene las sesiones del curso: el análisis
propio, el documento escrito con TheAIWriter y los informes de comprobación y revisión, tal
como se obtuvieron el 26 de noviembre de 2026.

Está congelado a propósito. Repetir el análisis o volver a ejecutar las herramientas **da
resultados distintos**: el docking tiene aleatoriedad y cada redacción del documento cambia el
texto y los avisos. En clase se abren estos archivos; no se vuelven a generar.

## La pregunta

Empieza amplia en la sesión 2 —¿podemos fiarnos de AlphaFold en los bolsillos de unión?— y se
afila hasta algo medible: **¿la confianza de AlphaFold en el bolsillo (pLDDT) avisa de si el
docking va a funcionar?**

## Qué hay aquí

| Carpeta | Qué contiene |
|---|---|
| `analisis/codigo/` | los scripts que hicieron el análisis |
| `analisis/resultados/` | las tablas y figuras: una fila por complejo |
| `analisis/LEEME.md` | método, resultados y límites, en corto |
| `analisis/EXPLICACION.md` | el caso explicado desde cero, sin dar por sabida la biología |
| `documento/` | el plan, el borrador y la bibliografía que escribió TheAIWriter |
| `documento/informes/pasada-1-0858/` | la primera comprobación, **transcrita** (ver su PROCEDENCIA.md) |
| `documento/informes/pasada-2-0912/` | la segunda comprobación y la revisión, archivos originales |

## Las dos pasadas

El orden importa, y es la lección:

**comprobar** → 42 de 43 cifras con origen, 35 de 36 frases apoyadas, tres avisos
**corregir** → se aplican los arreglos
**comprobar otra vez** → 43 de 43, 36 apoyadas, y **un aviso nuevo** que la corrección destapó

El aviso nuevo es mejor que los tres anteriores: señala que la frase atribuye a Holcomb una
comparación que pertenece a este documento, no a su artículo.

## Lo que este caso no demuestra

Las cifras absolutas no son comparables con la literatura: la preparación del receptor aquí es
básica. Lo que sí aguanta es la dirección, porque cada ligando se acopló también sobre la
estructura experimental como control. Está detallado en `analisis/LEEME.md`, apartado
«Límites», y conviene leerlo antes de citar cualquier número de aquí.

Hay además un error propio, encontrado al escribir el documento y corregido el 26/11/2026: las
notas describían una correlación con un alcance que el código no calculaba. Se cuenta entero en
`analisis/EXPLICACION.md`, apartado 8.
