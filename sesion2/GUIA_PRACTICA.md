# Sesión 2 · Guía de la práctica

**Objetivo.** Partir de tu pregunta científica y terminar con una colección de Zotero, los artículos que tienes que leer tú, una hipótesis refinada y un esquema de estudio.

Trabaja con tu propia pregunta. Los textos en bloque son para copiar, cambiar lo que va entre `[corchetes]` y dárselos a Claude. Los tiempos son orientativos: lo que no termines, complétalo en casa.

> ⚠️ No subas datos de pacientes, resultados sin publicar ni manuscritos ajenos. Para esta práctica no hacen falta.

| Parte | Qué haces | Tiempo |
|---|---|---|
| A | Buscar y guardar | 20 min |
| B | Automatizar | 8 min |
| C | Explorar | 17 min |
| D | Afinar la pregunta | 15 min |

---

## Antes de empezar

- [ ] La app de escritorio de Claude está abierta en la pestaña **Code**, con esta carpeta abierta.
- [ ] Claude lista tus colecciones de Zotero (receta de la sesión 1).
- [ ] En **Ajustes → Conectores** tienes activados **PubMed**, **bioRxiv** y **Consensus**.
- [ ] Entras en Research Rabbit y en Consensus.
- [ ] Tienes tu pregunta y dos o tres artículos que conozcas.

Si algo falla, sigue con lo que funcione y pide ayuda. Si usas Codex, necesitas tener Zotero y los conectores configurados allí; algunos pasos pueden cambiar.

---

## Parte A · Buscar y guardar

### 1. Tu colección

En Zotero, crea una colección con el nombre corto de tu pregunta y, dentro, estas subcolecciones: **Europe PMC**, **Claude**, **Research Rabbit**, **Consensus** y **Novedades semanales**.

✔ Las ves en Zotero tras sincronizar.

### 2. Búsqueda clásica en Europe PMC

1. Entra en [europepmc.org](https://europepmc.org) y escribe tu consulta **solo en título y resumen**:

   ```
   TITLE_ABS:([término] OR "[sinónimo]") AND TITLE_ABS:([concepto] OR "[sinónimo]")
   ```

2. Si salen cientos de resultados, añade un concepto. Si salen menos de diez, añade sinónimos. **Apunta la consulta y el número en `ENTREGA.md`.**
3. Pulsa **Export citations**, elige **RIS** y descarga.
4. En Zotero, selecciona la subcolección **Europe PMC**. Después, **Archivo › Importar…**, elige el archivo y **desmarca** la casilla de colocarlo en una nueva colección.
5. Revisa **Elementos duplicados** y fusiona solo los que sean la misma publicación. El preprint y su artículo publicado no lo son.

✔ La subcolección tiene tantos elementos como resultados exportaste.

### 3. La misma pregunta, desde Claude

```
Busca en PubMed, bioRxiv y Europe PMC artículos de [2021] a [2026] sobre
[tu pregunta].

Añade los relevantes a Zotero, en «[tu colección] › Claude». No borres ni
cambies nada que ya exista, y no dupliques los artículos que ya estén.

Para cada uno, dime dónde lo encontraste, con qué consulta literal y por qué
lo incluyes. Si una base no te deja buscar por palabras clave, dímelo.
```

Puede tardar más de diez minutos. **Déjalo trabajando y pasa a la parte B.**

### 4. Comparar (cuando Claude termine)

```
Compara en Zotero las subcolecciones «Europe PMC» y «Claude» de «[tu colección]».
Dime cuáles coinciden, contando como el mismo trabajo el preprint y su versión
publicada, y cuáles salen solo en una. No cambies nada.
```

✔ Has apuntado cuántos coinciden y has abierto **dos** de los que solo encontró Claude para ver si de verdad tienen que ver con tu pregunta.

---

## Parte B · Automatizar

Crea las dos tareas con sus fichas. Copia la plantilla, cambia lo que va entre corchetes y dásela a Claude.

1. [Actualización semanal de Zotero](ficha-actualizacion-zotero.md)
2. [Seguimiento de autores](ficha-seguimiento-autores.md)

Para probarlas, usa 90 días en vez de 7 y pide que se ejecuten una vez. Puedes hacer la prueba en casa.

✔ Las dos tareas aparecen en tu lista de tareas programadas.

---

## Parte C · Explorar

### 5. Research Rabbit

1. Empieza una búsqueda nueva y elige como semilla un artículo que conozcas bien.
2. En **Grow**, mira los similares, sus referencias y los que lo citan.
3. Elige unos pocos que no tuvieras, expórtalos en **RIS** e impórtalos en la subcolección **Research Rabbit**, como en el paso 2.

La sincronización automática con Zotero es de pago; no hace falta.

### 6. Consensus

1. Haz tu pregunta en inglés y en forma de sí o no.
2. Mira el **medidor** y cuántos estudios hay detrás (la N).
3. **Abre un estudio** y comprueba que dice lo que pone el resumen.
4. Exporta en **RIS** e impórtalo en la subcolección **Consensus**, o guarda con Zotero Connector.

La cuenta gratuita tiene un número limitado de mensajes Pro: haz solo las búsquedas que necesites.

### 7. Toda la biblioteca en Claude

```
Mi pregunta: [tu pregunta]

En «[tu colección]», agrupa los artículos por enfoque y señala los que
responden directamente a mi pregunta.

Propón como mucho cinco para leer enteros y explica por qué. Dime también
cuáles has dejado fuera que discutan la conclusión y qué has leído de cada
uno: texto completo, fragmentos o solo el resumen.

No etiquetes nada sin mi visto bueno.
```

**Decide tú** y, cuando lo tengas claro:

```
Etiqueta como «lectura obligatoria» solo estos: [lista]
```

✔ Entre uno y cinco artículos llevan la etiqueta.

---

## Parte D · Afinar la pregunta

Sigue los cinco pasos de la ficha [refinar tu pregunta](ficha-refinar-pregunta.md). El paso 4 usa la skill que está en `skills/grilling/`.

Si no te da tiempo, haz en clase los pasos 1 y 2 y termina en casa, **después de leer** tus artículos obligatorios.

---

## Qué entregas

Completa [ENTREGA.md](ENTREGA.md):

1. Tu colección, con una subcolección por fuente.
2. Los artículos de lectura obligatoria.
3. La hipótesis refinada y qué la cambió.
4. El paradigma experimental.

Además, las dos tareas programadas creadas y probadas una vez.

## Para el 16 de diciembre

Lee los artículos con la etiqueta «lectura obligatoria», anótalos en Zotero y corrige lo que Claude resumió mal. Comprueba que tienen su **PDF en Zotero**: el RIS puede no traerlo y la sesión 4 los necesita. Mira si la tarea semanal ha dejado algo: muchas semanas no habrá nada nuevo, y es normal.

## Si algo falla

| Síntoma | Qué hacer |
|---|---|
| Europe PMC dice que no hay resultados, pero los filtros muestran números | La web falla a ratos: espera unos minutos y recarga |
| Claude no ve tu Zotero | Cierra la app del todo, ábrela de nuevo y pide «lista mis colecciones» |
| Claude guarda en otra colección | Escribe el nombre exacto y pídele que te lo repita antes de guardar |
| No aparecen los artículos en Zotero | Sincroniza Zotero |
| Claude cita un artículo que no existe | Pide el DOI y ábrelo; si no existe, bórralo |
