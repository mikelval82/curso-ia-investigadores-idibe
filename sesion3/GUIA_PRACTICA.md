# Sesión 3 · Guía de la práctica

**Objetivo.** Dirigir un análisis por fases: Claude propone y programa; tú decides y lo dejas escrito.

La pregunta es la misma para todos: **¿se puede predecir la resistencia a ciprofloxacino de *E. coli* a partir de sus genes accesorios?** Trabaja por parejas si puedes. Los tiempos son orientativos.

| Fase | Tiempo |
|---|---|
| Antes de empezar | 5 min |
| 1. Exploración | 8 min |
| 2. Preprocesado | 8 min |
| 3. Entrenar y validar | 12 min |
| 4. Evaluar | 8 min |
| Cierre | 4 min |

> ⚠️ Son datos públicos. Con los tuyos, no subas datos de pacientes ni resultados sin publicar sin saber bajo qué condiciones.

---

## Antes de empezar

- [ ] [PREPARAR.md](PREPARAR.md) termina con «Todo listo para la sesión 3».
- [ ] Esta carpeta está abierta en Claude, pestaña **Code**. (Si usas Codex, copia `CLAUDE.md` como `AGENTS.md`.)
- [ ] Has leído [CLAUDE.md](CLAUDE.md): son seis reglas. Añade las que hemos visto en clase:

```
- Di cuántas filas quedan tras cada paso y por qué.
- Informa siempre de cuántos resistentes se detectan.
- Compara con usar solo el linaje.
- Trata igual a todos los modelos que compares.
- No llames causa a una asociación.
```

Empieza con esto:

```
Lee CLAUDE.md y dime en pocas líneas qué reglas vas a seguir. No hagas nada más.
```

✔ Las repite bien. Si no las menciona todas, pídele que vuelva a leer el archivo.

---

## En cada fase

Copia este texto y cambia la fase:

```
Estamos en la fase de [exploración]. No pases a la siguiente.

Mira los datos que necesites y propón dos opciones para cada decisión de esta
fase, tres decisiones como mucho. Para cada opción dime qué gano y qué pierdo,
en lenguaje sencillo. Espera a que elija antes de hacer nada.
```

Elige y, cuando termine:

```
Anota en DECISIONES.md qué opciones había, qué he elegido y por qué.
Después enséñame lo que ha cambiado en los números.
```

**Escribe tú el «por qué».** Si lo redacta Claude, léelo en voz alta: ¿lo dirías así?

### 1. Exploración

Preguntas para no olvidar: ¿qué falta y por qué?, ¿hay aislados raros o repetidos?, ¿los resistentes se reparten igual entre linajes y años? (En los datos, el linaje es la columna `MLST`.)

✔ Sabes cuántos aislados tienen resultado para ciprofloxacino y cuántos son resistentes.

### 2. Preprocesado

¿Qué genes descartas y con qué criterio? ¿Antes o después de separar los datos? ¿Qué haces con los aislados sin linaje?

✔ Sabes cuántas filas y cuántos genes quedan.

### 3. Entrenar y validar

Si quieres poner a prueba tu plan antes de entrenar, escribe `/grill-me` y cuéntale qué vas a hacer. Es opcional.

¿Con quién pruebas el modelo: con aislados al azar o con linajes que no ha visto? ¿Das más peso a los resistentes? ¿A todos los modelos igual?

✔ Tienes el resultado de **dos** formas de separar los datos.

### 4. Evaluar

¿Qué error te importa más: dejar escapar un resistente o dar por resistente uno que no lo es? ¿Con qué lo comparas?

✔ Tienes el acierto, los resistentes detectados y lo que se consigue sabiendo solo el linaje.

Y una comprobación final:

```
Cambia una sola decisión razonable de la fase 3 y repite. Enséñame la tabla
con los dos resultados, uno al lado del otro.
```

✔ Has visto si la conclusión aguanta el cambio.

---

## Cierre: qué entregas

1. Tu `CLAUDE.md`, con las reglas que has añadido.
2. [DECISIONES.md](DECISIONES.md) completo.
3. Un resultado que sepas explicar, con su límite.
4. Una duda que estos datos no permiten responder.

## Si algo falla

| Síntoma | Qué hacer |
|---|---|
| Claude sigue a la fase siguiente | «Para. Estamos en la fase de…» y apúntalo: también es información |
| No encuentra Python o una librería | Pídele que use `.venv`. Si no está, vuelve a PREPARAR.md |
| Tarda mucho | Pídele menos genes o menos árboles y anótalo como decisión |
| Da muchas cifras y no las entiendes | «Explícamelo con cien aislados: ¿cuántos resistentes encuentra y cuántos se le escapan?» |
| Dos parejas tienen resultados distintos | Comparad vuestros DECISIONES.md: ahí está la explicación |
