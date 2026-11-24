# Ficha: tarea programada para mantener al día una colección de Zotero

## Qué hace

Una vez por semana (por ejemplo, los lunes a las 8:30), Claude:

1. Busca artículos nuevos sobre tu pregunta en las fuentes que le indiques.
2. Añade los que cumplen tus criterios a la subcolección **«Novedades semanales»** de la colección de tu pregunta.
3. Te deja un **registro** con lo que ha añadido, de dónde lo ha sacado y por qué, en una nota del elemento «Registro de novedades».

Tú revisas «Novedades semanales» cuando te viene bien y mueves a otras subcolecciones lo que te interese.

---

## Qué necesitas antes de empezar

| Qué | Para qué |
|---|---|
| **Zotero conectado a Claude (MCP)** | Para guardar los artículos. Quedó instalado en la sesión 1 |
| **App de escritorio de Claude abierta** | El conector de Zotero se ejecuta dentro de la app. Claude guarda en tu biblioteca en línea y tu Zotero la recibe al sincronizar |
| **Colección de tu pregunta con su subcolección «Novedades semanales»** | Para que lo nuevo no se mezcle con lo que ya has revisado |
| **Conectores de búsqueda activos** (PubMed, bioRxiv…) | Para buscar en las bases y no solo en la web |

> ⚠️ **Importante:** la tarea se ejecuta con la app de Claude abierta. Si está cerrada o el ordenador apagado a esa hora, se ejecutará cuando vuelvas a abrirla.

> 💡 **Si sale vacía, no es que falle.** Con una pregunta muy concreta, muchas semanas no habrá nada nuevo. En el ejemplo de AlphaFold, Europe PMC no dio ningún artículo en las dos últimas semanas, 1 en el último mes y 6 en tres meses (comprobado el 22/11/2026). **Para probarla, cambia `[7]` por `[90]` días.** Después vuelve a 7, o hazla mensual si tu pregunta es muy específica.

---

## Cómo se configura

1. **Crea la subcolección** «Novedades semanales» dentro de la colección de tu pregunta.
2. **Copia la plantilla** de abajo y cambia lo que va entre `[corchetes]`.
3. **Pídele a Claude que cree la tarea**: *«Crea una tarea programada semanal, los [lunes a las 8:30], con estas instrucciones.»*
4. **Revisa los permisos.** La tarea se ejecuta cuando no estás delante: si cada paso pide permiso, se quedará parada. Permítele solo lo que necesita (buscar y añadir a Zotero), no borrar ni enviar nada.
5. **Haz una prueba.** Pídele que la ejecute una vez ahora y comprueba que aparecen artículos en «Novedades semanales» y que te deja el registro.

---

## Plantilla de instrucciones

```
Eres mi asistente de actualización bibliográfica. Cada vez que se ejecute esta tarea:

1. TEMA. Mi pregunta es:
   [¿Podemos fiarnos de AlphaFold en los bolsillos de unión de ligandos?]

2. BUSCA artículos publicados en los últimos [7] días en:
   [PubMed y bioRxiv].
   Usa como punto de partida esta consulta, la misma que usé en Europe PMC. Busca
   solo en título y resumen; adáptala a cada fuente sin ampliarla al texto completo:
   [TITLE_ABS:(AlphaFold OR "AlphaFold2") AND TITLE_ABS:(pLDDT OR confidence)
    AND TITLE_ABS:("binding site" OR pocket)]
   Si una fuente no permite buscar por palabras clave, dilo en el registro.

3. INCLUYE solo los que cumplan estos criterios:
   [- estudian la fiabilidad estructural de AlphaFold en sitios de unión;
    - artículos originales, revisiones o preprints con métodos descritos].
   Descarta los que solo mencionan el tema de pasada.

4. GUARDA en Zotero, en la colección
   «[AlphaFold · bolsillos de unión] › Novedades semanales»:
   - Añade cada artículo por DOI (o por ID de arXiv/bioRxiv si no tiene DOI).
   - Antes de añadir, comprueba que no esté ya en la biblioteca.
   - Solo añade: no borres, no muevas y no modifiques nada que ya exista.
   - Añade la etiqueta "novedad-auto".
   - Como mucho, [10] artículos por semana. Si hay más, quédate con los más pertinentes.

5. DEJA UN REGISTRO en una nota titulada "Novedades – semana del [fecha]".
   El conector de Zotero solo crea notas dentro de un elemento. Si en esa
   subcolección no existe, crea uno de tipo "document" titulado
   "Registro de novedades" y añade ahí la nota; si ya existe, reutilízalo.
   Para cada artículo: referencia, fuente, consulta usada y una frase sobre por
   qué lo has incluido. Si no hay nada nuevo, dilo. Si Zotero no responde,
   indícalo en tu respuesta de esta tarea. No envíes correos ni mensajes.
```

---

## Mantenimiento

- **Demasiado ruido:** endurece los criterios del paso 3 o baja el máximo de artículos.
- **Se queda corto:** añade sinónimos a la consulta o una fuente más.
- **Revisar lo añadido:** en Zotero, filtra por la etiqueta `novedad-auto`.
- **Pausar o borrar:** pídeselo a Claude o hazlo desde la lista de tareas programadas.

## Problemas típicos

| Síntoma | Causa probable | Solución |
|---|---|---|
| No aparece nada en Zotero | Ordenador apagado o app cerrada | Cambia la hora o deja la app abierta |
| La tarea no termina | Está esperando una aprobación | Revisa los permisos de la tarea |
| Artículos repetidos | El artículo estaba con otro identificador | Pide que compare también por título |
| Artículos fuera de tema | Consulta demasiado amplia | Ajusta la consulta y los criterios |
