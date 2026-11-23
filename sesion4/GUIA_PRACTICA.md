# Sesión 4 · Guía de la práctica

**Objetivo.** Escribir una introducción de unas 300 palabras con los artículos de tu colección, comprobar que cada cita dice lo que dice el artículo y dejar un radar de convocatorias en marcha.

Trabaja con tu pregunta y tu colección de la sesión 2. Los textos en bloque son para copiar; cambia lo que va entre `[corchetes]`. Los tiempos son orientativos: lo que no termines, complétalo en casa.

> ⚠️ Solo literatura publicada. No subas datos de pacientes, resultados sin publicar ni manuscritos ajenos.

| Parte | Qué haces | Tiempo |
|---|---|---|
| A | Preparar | 15 min |
| B | Escribir | 20 min |
| C | Comprobar | 15 min |
| D | Radar de convocatorias | 10 min |

**Mientras Claude trabaja, adelanta la parte D.** Si vas con Codex o no has podido instalar el plugin, sigue [la otra vía](#si-usas-codex-o-no-tienes-el-plugin) y vuelve a la parte D: la entrega es la misma.

---

## Antes de empezar

- [ ] Has hecho la [preparación previa](INSTALAR_THEAIWRITER.md): plugin instalado e índice actualizado.
- [ ] Al menos **tres artículos** de tu colección tienen PDF con texto, y los has leído.
- [ ] Tienes a mano la entrega de la sesión 2 (`ENTREGA.md`): la pregunta y la hipótesis.

---

## Parte A · Preparar

### 1. Una carpeta vacía

Crea una carpeta, por ejemplo `mi-introduccion`, y ábrela en la pestaña **Code**, en una sesión local.

### 2. El documento

```text
/theaiwriter:nuevo Introducción sobre [tu pregunta]
```

Claude te propone un punto por cada cosa. Contesta:

| Te pregunta | Contesta |
|---|---|
| Título | El que te propone, u otro |
| Tipo | **Perspectiva**: es el tipo sin resultados propios |
| Idioma | Español |
| Colección | El nombre de **tu colección principal**; incluye sus subcolecciones |

✔ Aparece `proyecto.yaml` y te dice cuántas obras tienen PDF.

### 3. Tu resumen

Abre `materiales/abstract.md` y contesta **con tus palabras**, dos líneas por pregunta, debajo de cada una:

| Pregunta | De dónde sale |
|---|---|
| ¿Qué quieres defender? | Tu hipótesis de la sesión 2 |
| ¿Por qué importa ahora? | Tu pregunta revisada |
| ¿Qué argumentos la sostienen? | Tus artículos de lectura obligatoria |
| ¿Qué objeción esperas? | El resultado que la refutaría |

Si no ves cómo editarlo, dicta las respuestas y pide que las guarde **sin cambiarlas**.

```text
/theaiwriter:estado
```

✔ Ya no pide completar el resumen.

---

## Parte B · Escribir

### 4. Pide solo la introducción

```text
/theaiwriter:escribir solo la introducción, unas 300 palabras y entre 3 y 6 obras, con pausa
```

Consume tu plan: es lo que más gasta de la práctica.

### 5. Lee el plan y discútelo

Se para y te enseña el plan. **No lo apruebes sin leerlo.** Mira tres cosas:

1. ¿La primera frase del plan es lo que tú quieres defender?
2. ¿Avisa de algo que tus artículos no apoyan? Es lo más valioso del plan.
3. ¿Usa artículos que has leído? ¿Falta alguno que discuta tu idea?

Pide al menos **un cambio** y contesta `aprobado`.

✔ Existe `borrador/documento.md`, con citas como `[@apellido2020palabra]`. Una marca `[@?]` es una frase sin fuente: déjala a la vista.

**Mientras escribe, abre otra conversación y empieza la parte D.**

---

## Parte C · Comprobar

### 6. Mira el informe

Al terminar de escribir, el plugin comprueba el borrador y **lanza el juez solo**. No hace falta volver a pedirlo. Para ver cómo va:

```text
/theaiwriter:estado
```

Cuando termine, abre `informes/comprobacion.md`.

| El informe dice | Haz esto |
|---|---|
| Clave que no existe | Quita la cita o busca la obra |
| Cita literal que no coincide | Cópiala del PDF |
| Frase sin cita que habla de una obra | Pon la cita, o déjala si es tuya |
| Tergiversada, no apoyada o parcial | **Abre el artículo.** El juez también se equivoca |

Si el juez no termina a tiempo, sigue: las tres frases se comprueban igual.

### 7. Abre tres frases

Elige **las tres de las que más dudes**, también entre las que el juez da por buenas. Para encontrarlas en el PDF:

```
Para estas tres frases de borrador/documento.md, dime la obra, la página y
el pasaje en el que se apoya cada una, en su idioma original:
[frase 1] [frase 2] [frase 3]
No cambies el texto.
```

Abre el PDF en Zotero, busca el pasaje y **lee el párrafo entero**. Pregúntate:

- ¿Es la misma población, el mismo sistema, la misma magnitud?
- ¿Lo midieron ellos o citan a otros?
- ¿Mi frase dice más que el artículo?

Apunta en [ENTREGA.md](ENTREGA.md) la frase, la página y tu decisión: **la dejo, la cambio o la quito**.

### 8. Corrige

```text
/theaiwriter:corregir
```

Te enseña cada cambio, antes y después. **Acepta solo los que hayas mirado:** por ejemplo, `1, 3`. Lo que no arregle, cámbialo tú en el archivo.

```text
/theaiwriter:comprobar sin juez
```

✔ No quedan claves inventadas y tienes tres frases decididas por ti.

### 9. Tu declaración

Adapta este ejemplo a lo que de verdad has hecho:

```
Usé [herramienta y versión] para redactar un primer borrador y comprobar las
citas. Revisé el texto y respondo de su contenido.
```

Antes de usarla en una revista, mira sus normas.

---

## Parte D · Radar de convocatorias

Sigue la [ficha del radar](ficha-radar.md), en su **propia carpeta** (`radar-convocatorias`) y en **otra conversación**.

1. Rellena tu perfil y pega las instrucciones.
2. Cuando termine, abre **dos plazos** en la página oficial y lee las **descartadas**.
3. Crea la tarea semanal y ejecútala una vez. Si no da tiempo, en casa.

✔ Existe `convocatorias.csv` y los dos plazos coinciden.

Opcional, en casa y con permiso de la universidad: [el correo, solo borradores](ficha-correo.md).

---

## Si usas Codex o no tienes el plugin

Los mismos pasos, con tu asistente y comprobando a mano. Sustituye a las partes A, B y C.

**1. Prepara.** Crea la carpeta `mi-introduccion` y, dentro, `pdfs` con **entre tres y seis** artículos de tu colección. En Zotero: clic derecho sobre el PDF y **Mostrar archivo**; cópialo, no lo muevas. Escribe `resumen.md` con las cuatro respuestas del paso 3.

**2. Pide el plan.**

```
Lee resumen.md y los PDF de la carpeta pdfs. No uses internet ni tu memoria.
No escribas todavía la introducción.

Si algún PDF no se puede leer, dímelo y no lo cites.

Escribe plan.md: qué quiero defender, qué va a decir cada párrafo y qué
artículo lo apoya, con su página. Di qué partes de mi resumen no tienen apoyo
en estos artículos. Después, espera a que lo apruebe.
```

Lee el plan como en el paso 5 y pide al menos un cambio.

**3. Pide la introducción.**

```
Aprobado. Escribe introduccion.md: unas 300 palabras, en español.

- Cada frase que diga lo que dice un artículo lleva su cita en la misma frase:
  (Apellido, año, p. X). La página es la que se ve al abrir el PDF.
- Con el mismo alcance que el artículo. Si el artículo cita a otros, dilo.
- Lo que propongo yo va en otra frase y sin cita.
- Si falta una fuente, escribe [FALTA FUENTE]. No la inventes.

Escribe también pasajes.md: una fila por frase con cita, con el artículo, la
página y el pasaje literal en su idioma.
```

**4. Comprueba.** Abre una conversación **nueva** en la misma carpeta, para que no defienda su propio texto:

```
Compara cada frase con cita de introduccion.md con su PDF de la carpeta pdfs.
No te fíes de pasajes.md: abre el artículo.

Para cada una: apoyada, parcial, no apoyada o no lo puedo comprobar, con la
página, el pasaje literal y el motivo. No cambies ningún archivo.
```

Aquí no hay programa que confirme que las citas existen ni que los pasajes son literales: por eso **busca tú cada pasaje literal en el PDF**, al menos en tus tres frases. Sigue el paso 7 desde «Abre el PDF», corrige el texto a mano y escribe tu declaración (paso 9).

Si tienes la skill `bibliografia-con-evidencia`, en el paso 4 añade «lee y aplica su `SKILL.md`».

**5. El radar.** Las instrucciones de la [ficha](ficha-radar.md) se pueden pegar también en Codex. Su [documentación](https://learn.chatgpt.com/docs/automations) (22/11/2026) dice que admite tareas programadas y que, si usan archivos locales, la app y el ordenador tienen que estar encendidos. **No lo hemos probado:** si no te funciona, entrega la ejecución a mano.

---

## Qué entregas

Completa [ENTREGA.md](ENTREGA.md):

1. La introducción, de unas 300 palabras.
2. Tres frases abiertas: página y decisión.
3. La declaración de uso de IA.
4. El radar, creado y probado una vez.

## Si algo falla

| Síntoma | Qué hacer |
|---|---|
| No aparecen las órdenes `/theaiwriter:` | Cierra Claude del todo y ábrelo. Si sigue igual, usa la otra vía |
| Dice que la carpeta ya es un documento | Ya hiciste el paso 2: sigue con `/theaiwriter:estado` |
| Dice que el resumen está vacío | Escribe debajo de cada pregunta, no dentro de `<!-- -->`, y guarda |
| Casi no encuentra obras | Faltan PDF en Zotero. Añádelos y pide `/theaiwriter:diagnostico actualiza el índice` |
| Se ha puesto a escribir el artículo entero | Páralo y repite: «solo la introducción» |
| El informe dice «desactualizado» | El texto ha cambiado después del juez. Con tus tres frases abiertas, puedes seguir |
| Límite de uso alcanzado | Comprueba tus tres frases a mano; el juez sigue otro día con `/theaiwriter:comprobar` |
| Cita un artículo que no has leído | Léelo o quítalo: lo firmas tú |
