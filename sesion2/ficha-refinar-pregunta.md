# Ficha: refinar tu pregunta con Claude

## Qué hace

Pasas de una pregunta amplia a una **pregunta que se puede contestar**, con su hipótesis y un esquema de estudio. Claude ordena la evidencia y te pone a prueba; **las decisiones las tomas tú**.

No es una tarea programada: es una conversación de unos 20 minutos, en cinco pasos.

---

## Qué necesitas antes de empezar

| Qué | Para qué |
|---|---|
| **Tu colección de Zotero**, con las subcolecciones | Es la evidencia de partida |
| **Tus artículos con la etiqueta «lectura obligatoria»** | Son los que vas a leer tú |
| **Zotero conectado a Claude (MCP)** | Para que lea tu colección |
| **Conectores de búsqueda activos** (PubMed, bioRxiv…) | Para el paso 3 |
| **La carpeta de la sesión 2 abierta en Claude** (pestaña Code) | Trae en `skills/grilling/` la skill del paso 4 |

> ⚠️ **Importante:** no pegues datos de pacientes ni resultados sin publicar. Para refinar la pregunta no hacen falta.

---

## Los cinco pasos

Copia cada texto, cambia lo que va entre `[corchetes]` y dáselo a Claude. Espera su respuesta antes de pasar al siguiente.

### 1. Matriz de evidencia

```
Mi pregunta: [¿Podemos fiarnos de AlphaFold en los bolsillos de unión?]

Lee los artículos con la etiqueta «lectura obligatoria» de mi colección
«[AlphaFold · bolsillos de unión]» en Zotero. Haz una tabla con: qué afirma
cada uno, con qué datos y qué límite tiene.

Para cada artículo, dime qué has leído: texto completo, fragmentos o solo el
resumen. No modifiques nada en Zotero.
```

**Compruébalo:** abre dos artículos y mira si dicen lo que pone la tabla.

### 2. Posible vacío

```
Con esa tabla, propón una cosa que no esté resuelta. Dímela en una frase,
como una posibilidad, no como un hecho, y explica en qué artículos te apoyas.
```

### 3. Buscar lo que lo invalida

```
Ahora intenta demostrar que te equivocas: busca artículos que ya respondan a
eso o que digan lo contrario. Empieza por los de mi colección que no están
entre los de lectura obligatoria y sigue con [PubMed y bioRxiv].

Dime dónde has buscado y con qué consulta literal. Si no encuentras nada, no
digas que no existe.
```

**Si encuentra algo, vuelve al paso 2** con esa información. En el caso de AlphaFold pasó: un artículo que había quedado fuera de los cinco cambió la pregunta.

### 4. Grill-me: que te interrogue

Este paso usa siempre **grilling**, la skill de Matt Pocock que hace el interrogatorio. Su compañera, grill-me, solo la llama, así que aquí no hace falta.

El ZIP de la sesión 2 ya la trae: abre esa carpeta en Claude (pestaña Code). Si trabajas en otro proyecto, copia en él la carpeta `skills/grilling/`. Después:

```
Lee entero el archivo skills/grilling/SKILL.md de este proyecto y aplícalo a
mi pregunta, al posible vacío del paso 2 y a lo que encontraste en el paso 3.
Dime qué archivo has leído. Si no lo encuentras, avísame y para: no lo
sustituyas por otra skill.

Estas indicaciones mandan sobre la skill:
- En español y en lenguaje sencillo.
- De una en una, no por rondas, y cinco preguntas como mucho.
- Con tu respuesta recomendada en cada una; decido yo.
- No lances subagentes.

Pregúntame qué voy a medir, contra qué lo comparo, con qué datos cuento y qué
resultado me haría cambiar de idea. Si una pregunta es muy técnica, explícala
con un ejemplo. Si digo «para», resume lo acordado.
```

**Compruébalo:** Claude tiene que decirte que ha leído `skills/grilling/SKILL.md`.

**Contesta con lo que sabes tú.** «No lo sé» también es una respuesta, y suele señalar lo que falta.

### 5. Pregunta revisada

```
Resume en una página:
- Pregunta inicial y pregunta revisada.
- Qué la cambió, con los artículos.
- Hipótesis y qué resultado la refutaría.
- Estudio: datos, variable, comparación y medida.
- Qué queda sin comprobar.

Separa lo que he decidido yo de lo que propones tú. Enséñamelo y, cuando te
dé el visto bueno, complétalo en ENTREGA.md.
```

---

## Cómo sabes que has terminado

- [ ] La pregunta cabe en una frase y se entiende sin explicarla.
- [ ] Sabes qué mides y contra qué lo comparas.
- [ ] Sabes qué resultado te haría cambiar de idea.
- [ ] Has leído tú los artículos que la sostienen, o sabes cuáles te faltan.
- [ ] Tienes escrito qué la cambió.

---

## Ejemplo: el caso de AlphaFold

| | |
|---|---|
| **Antes** | ¿Podemos fiarnos de AlphaFold en los bolsillos de unión? |
| **Lo que la cambió** | [Holcomb 2023](https://doi.org/10.1002/pro.4530) dice que la confianza no predice bien el docking; [Lee 2023](https://doi.org/10.1016/j.csbj.2022.11.057), que en GPCR sí avisa |
| **Después** | ¿La confianza de AlphaFold en el bolsillo avisa de si el docking va a funcionar? |
| **Hipótesis** | A más confianza en el bolsillo, más aciertos |
| **La refutaría** | Que acierte igual con confianza alta que baja |

Es un ejemplo para la práctica, no un estudio validado.

---

## Problemas típicos

| Síntoma | Causa probable | Solución |
|---|---|---|
| Claude dice que «nadie lo ha estudiado» | Ha buscado poco | Repite el paso 3 con otros términos y otra base |
| Claude no encuentra `skills/grilling/SKILL.md` | No has abierto la carpeta de la sesión 2 | Ábrela en la pestaña Code y repite el paso 4 |
| Te pierdes con sus preguntas | Va demasiado al detalle | Dile «más sencillo» o «para y resume» |
| Te da la razón en todo | No le has pedido que discuta | Pídele la objeción más fuerte contra tu pregunta |
| La pregunta sigue siendo muy amplia | Falta decir qué se mide | Vuelve al paso 4 y concreta la medida |
| Cita artículos que no encuentras | Puede habérselos inventado | Pide el DOI y ábrelo; si no existe, bórralo |
