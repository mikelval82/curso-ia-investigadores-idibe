# Sesión 3 · Guía de la práctica

**Objetivo.** Dirigir un análisis por fases: Claude propone y programa; tú decides y lo dejas escrito.

La pregunta es la misma que en las sesiones 2 y 4: **¿la confianza de AlphaFold en el bolsillo avisa de si el docking va a funcionar?** Hoy trabajas sobre la primera mitad: ¿avisa al menos de si el bolsillo está bien predicho? Los datos son el resultado ya calculado del análisis del curso, y están en `datos/`; `datos/LEEME.md` los describe. Trabaja por parejas si puedes. Los tiempos son orientativos.

| Fase | Tiempo |
|---|---|
| Antes de empezar | 5 min |
| 1. Exploración | 8 min |
| 2. Preparar | 8 min |
| 3. Medir | 12 min |
| 4. Poner a prueba | 8 min |
| Cierre | 4 min |

> ⚠️ Son datos públicos y ya calculados: no se vuelve a ejecutar el análisis. Con los tuyos, mira antes la ficha [¿Qué datos puedo usar?](https://github.com/mikelval82/curso-ia-investigadores-idibe/blob/main/sesion1/QUE_DATOS_PUEDO_USAR.md).

---

## Antes de empezar

- [ ] [PREPARAR.md](PREPARAR.md) termina con «Todo listo para la sesión 3».
- [ ] Esta carpeta está abierta en Claude, pestaña **Code**. (Si usas Codex, copia `CLAUDE.md` como `AGENTS.md`.)
- [ ] Has leído [CLAUDE.md](CLAUDE.md): son seis reglas. Añade las que hemos visto en clase:

```
- Di cuántas filas quedan tras cada paso y por qué.
- Di siempre con cuántos complejos y cuántas proteínas se ha calculado.
- Da cada correlación con su p y su n.
- Antes de concluir, enséñame la figura con los puntos.
- No llames predicción a una correlación.
```

Empieza con esto:

```
Lee CLAUDE.md y datos/LEEME.md y dime en pocas líneas qué reglas vas a seguir
y qué datos hay. No hagas nada más.
```

✔ Las repite bien y sabe qué es un bolsillo, un pLDDT y un RMSD. Si no las menciona todas, pídele que vuelva a leer el archivo.

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

Preguntas para no olvidar: ¿cuántas filas tiene la tabla y cuántas sirven?, ¿qué dice la columna `estado` de las que no sirven?, ¿aparece alguna proteína (`uniprot`) más de una vez?, ¿hay bolsillos de confianza baja?

✔ Sabes cuántos complejos hay, cuántos se caen y por qué.

### 2. Preparar

¿Te quedas solo con las filas `ok`? ¿Filtras también por `identidad_bolsillo`? ¿Dejas una fila por proteína o todas? ¿Qué columna mide «lo bien hecho que está el bolsillo»: `rmsd_ca_bolsillo` o `rmsd_atomos_bolsillo`?

✔ Sabes con cuántos complejos y cuántas proteínas te has quedado, y por qué.

### 3. Medir

Si quieres poner a prueba tu plan antes de calcular, escribe `/grilling` y cuéntale qué vas a hacer. Es opcional.

¿Spearman o Pearson? ¿Una sola correlación, o además la figura y los grupos por tramos de confianza (menos de 90, 90 o más)?

✔ Tienes la correlación **con su p y su n**, y una figura con los puntos que entiendes.

### 4. Poner a prueba

¿Qué pasa si cambias una decisión de la fase 2? ¿Cuántos bolsillos de confianza alta salen mal de todas formas? ¿Hay alguna proteína que se repita y dé resultados muy distintos?

Y una comprobación final:

```
Cambia una sola decisión razonable de la fase 2 o la 3 y repite. Enséñame la
tabla con los dos resultados, uno al lado del otro.
```

✔ Has visto si la conclusión aguanta el cambio, y sabes a qué casos no se les aplica.

> Si te sobra tiempo: `docking_caja_ajustada.csv` tiene los 90 complejos en los que además se probó el docking, con `acierta_af` y `acierta_exp`. Es la segunda mitad de la pregunta, y la que cambia la respuesta.

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
| Da una correlación y nada más | «¿Con cuántos complejos? ¿Y la p? Enséñame la figura» |
| Usa las 428 filas sin mirar `estado` | Es una decisión que no ha contado: pídele que la anote en DECISIONES.md |
| Dice que la confianza «predice» el acierto | Recuérdale la regla: con estos datos solo hay una correlación |
| Dos parejas tienen resultados distintos | Comparad vuestros DECISIONES.md: ahí está la explicación |
