# Ficha: tarea programada para seguir a los autores clave de tu pregunta

> La lista de investigadores sale de tu colección de Zotero y el resumen se queda en Zotero, sin enviar correos.

## Qué hace

Cada cierto tiempo (por ejemplo, los lunes a las 8:40), Claude:

1. Revisa lo último que han publicado los investigadores de tu lista.
2. Añade los artículos **que de verdad merecen la pena** a la subcolección **«Novedades semanales»** de tu pregunta.
3. Deja **una nota con el resumen** en el elemento «Registro de novedades» de esa subcolección.

Lo lees en Zotero cuando te venga bien. **No envía correos.**

---

## Qué necesitas antes de empezar

| Qué | Para qué |
|---|---|
| **Zotero conectado a Claude (MCP)** | Para guardar los artículos y la nota. Quedó instalado en la sesión 1 |
| **App de escritorio de Claude abierta** | El conector de Zotero se ejecuta dentro de la app. Claude guarda en tu biblioteca en línea y tu Zotero la recibe al sincronizar |
| **Colección de tu pregunta con su subcolección «Novedades semanales»** | Para que lo nuevo no se mezcle con lo que ya has revisado |
| **Lista de investigadores** | Para saber a quién seguir |

> ⚠️ **Importante:** la tarea se ejecuta con la app de Claude abierta. Si está cerrada o el ordenador apagado a esa hora, se ejecutará cuando vuelvas a abrirla.

No hace falta tener cuenta en ninguna red social: Claude solo lee contenido público.

---

## De dónde saca la información

| Fuente | Qué mira | Notas |
|---|---|---|
| **arXiv** | Artículos nuevos del autor | La fuente más fiable |
| **OpenAlex / Semantic Scholar** | Publicaciones en revistas y congresos | Cubre lo que no está en arXiv |
| **Bluesky** | Posts públicos | Cada vez más investigadores publican aquí |
| **Mastodon** | Posts públicos | Menos gente, pero accesible |
| **GitHub** | Repos nuevos | Útil para ver código y herramientas |
| **Blogs / Substack** | Artículos | Si el investigador tiene uno |

❌ **X/Twitter y LinkedIn no sirven:** exigen iniciar sesión y no se pueden leer de forma automática.

---

## Cómo se configura (paso a paso)

### 1. Prepara tu lista a partir de tu colección

Pídele a Claude, con el MCP de Zotero:

> *"En la colección «[nombre de tu pregunta]», ¿qué autores aparecen en más artículos? Dame los diez primeros con el número de artículos y sus temas."*

Elige de 3 a 5 personas cuyo trabajo quieras seguir. Un nombre por línea. Si sabes su perfil de Bluesky o su web, añádelos (así no hay confusiones con otra persona que se llame igual):

```
- Nombre Apellido — @usuario.bsky.social — tema: predicción de estructuras
- Nombre Apellido — github.com/usuario — tema: sitios de unión
```

### 2. Decide dónde guarda los artículos

Lo más sencillo: la subcolección «Novedades semanales» de la colección de tu pregunta, con una etiqueta propia (`seguimiento-autores`) para distinguirlos de los que añade la tarea de actualización.

### 3. Pídele a Claude que cree la tarea

En una conversación con Claude, pega el texto de la plantilla de abajo (con tu lista dentro) y dile, por ejemplo:

> *"Crea una tarea programada semanal, los lunes a las 8:40, con estas instrucciones."*

### 4. Revisa los permisos

La tarea se ejecuta cuando no estás delante: si cada paso pide permiso, se quedará parada. Permítele solo lo que necesita (buscar, añadir a Zotero y crear notas), no borrar ni enviar nada.

### 5. Haz una prueba

Pídele a Claude que **la ejecute una vez ahora**, con `[90]` días en vez de `[7]` para que haya algo que encontrar, y comprueba que aparece la nota en «Novedades semanales». Después vuelve a 7.

---

## Plantilla de instrucciones para la tarea

Copia esto, cambia lo que va entre `[corchetes]` y dáselo a Claude:

```
Eres mi asistente de vigilancia científica. Cada vez que se ejecute esta tarea:

1. REVISA lo publicado en los últimos [7] días por estos investigadores:
   [pega aquí tu lista]
   Fuentes: arXiv, OpenAlex, Semantic Scholar, Bluesky, Mastodon, GitHub y
   sus blogs. No uses X/Twitter ni LinkedIn.

2. FILTRA: quédate solo con lo relevante para mis temas:
   [tu pregunta y sus temas; p. ej., fiabilidad de AlphaFold en bolsillos de unión].
   Descarta opiniones sueltas, autopromoción y repeticiones.

3. GUARDA EN ZOTERO solo los artículos realmente interesantes (como mucho [5]):
   - Añádelos por DOI o por ID de arXiv.
   - Ponlos en «[colección de tu pregunta] › Novedades semanales».
   - Antes de añadir, comprueba que no esté ya en la biblioteca.
   - Solo añade: no borres, no muevas y no modifiques nada que ya exista.
   - Añade la etiqueta "seguimiento-autores".

4. DEJA UNA NOTA titulada "Seguimiento de autores – semana del [fecha]".
   El conector de Zotero solo crea notas dentro de un elemento. Si en esa
   subcolección no existe, crea uno de tipo "document" titulado
   "Registro de novedades" y añade ahí la nota; si ya existe, reutilízalo.
   Incluye:
   - Lo más destacado (máx. 5 puntos), con 2-3 frases de por qué importa.
   - El resto, agrupado por investigador, con enlace.
   - Lista de lo que has añadido a Zotero.
   - Qué fuentes no has podido consultar.
   Si no hay nada nuevo, dilo. No envíes correos ni mensajes.

5. Usa un lenguaje claro y directo. Nada de relleno.
```

---

## Mantenimiento

- **Añadir o quitar investigadores:** pídele a Claude que actualice la tarea con la nueva lista.
- **Demasiado ruido:** endurece el filtro del paso 2 o baja el máximo de artículos.
- **Revisar lo que ha guardado:** en Zotero, filtra por la etiqueta `seguimiento-autores`.
- **Pausar o borrar:** pídeselo a Claude o hazlo desde la lista de tareas programadas.

---

## Problemas típicos

| Síntoma | Causa probable | Solución |
|---|---|---|
| La tarea no termina | Está esperando una aprobación | Revisa los permisos de la tarea |
| No aparece nada en Zotero | Ordenador apagado, app de Claude cerrada o Zotero sin sincronizar | Cambia la hora, deja la app abierta o sincroniza Zotero |
| La nota dice que no hay nada nuevo | Es lo normal muchas semanas | Amplía los días o la lista de autores |
| Aparecen artículos de otra persona | Nombre ambiguo | Añade su perfil o su web a la lista |
| Artículos fuera de tema | Filtro del paso 2 demasiado amplio | Concreta los temas |
