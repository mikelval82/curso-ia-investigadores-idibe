# Sesión 3 · Guía de la práctica

**Objetivo.** Dirigir un análisis por fases: Claude propone y programa; tú decides y lo dejas escrito.

La pregunta es la misma para todos: **¿qué genes de los islotes pancreáticos se asocian con la HbA1c, y siguen asociados cuando se tienen en cuenta la edad, el IMC y el sexo?** Los datos son públicos: la expresión génica de los islotes de 63 donantes, con y sin diabetes tipo 2. Tras la preparación, `datos/LEEME.md` los describe. Trabaja por parejas si puedes. Los tiempos son orientativos.

| Fase | Tiempo |
|---|---|
| Antes de empezar | 5 min |
| 1. Exploración | 8 min |
| 2. Preprocesado | 8 min |
| 3. Comparar y ajustar | 12 min |
| 4. Evaluar | 8 min |
| Cierre | 4 min |

> ⚠️ Son datos públicos. Con los tuyos, mira antes la ficha [¿Qué datos puedo usar?](https://github.com/mikelval82/curso-ia-investigadores-idibe/blob/main/sesion1/QUE_DATOS_PUEDO_USAR.md).

---

## Antes de empezar

- [ ] [PREPARAR.md](PREPARAR.md) termina con «Todo listo para la sesión 3».
- [ ] Esta carpeta está abierta en Claude, pestaña **Code**. (Si usas Codex, copia `CLAUDE.md` como `AGENTS.md`.)
- [ ] Has leído [CLAUDE.md](CLAUDE.md): son seis reglas. Añade las que hemos visto en clase:

```
- Di cuántos donantes y cuántas sondas quedan tras cada paso y por qué.
- Con cada umbral, di cuántos genes saldrían solo por azar.
- Da siempre el resultado con y sin tener en cuenta edad, IMC y sexo.
- Comprueba un gen conocido de las células beta antes de dar un resultado.
- No llames causa a una asociación.
```

Empieza con esto:

```
Lee CLAUDE.md y datos/LEEME.md y dime en pocas líneas qué reglas vas a seguir
y qué datos hay. No hagas nada más.
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

Preguntas para no olvidar: ¿a quién le falta la HbA1c?, ¿hay donantes «sin diabetes» con una HbA1c de diabetes (6,5 % o más)?, ¿se parecen los dos grupos en edad, IMC y sexo?

✔ Sabes cuántos donantes tienen HbA1c y cuántos tienen diabetes.

### 2. Preprocesado

¿Qué haces con los donantes sin HbA1c? ¿Quitas las sondas que apenas se expresan? ¿Y las que no tienen gen o tienen varios?

✔ Sabes cuántos donantes y cuántas sondas quedan.

### 3. Comparar y ajustar

Si quieres poner a prueba tu plan antes de calcular, escribe `/grilling` y cuéntale qué vas a hacer. Es opcional.

¿Comparas «con diabetes» frente a «sin diabetes», o usas la HbA1c como un número? ¿Tienes en cuenta la edad, el IMC y el sexo?

✔ Tienes el resultado de **dos** formas: comparando los dos grupos y usando la HbA1c.

### 4. Evaluar

¿Qué umbral usas para decir que un gen «sale»? ¿Cuántos saldrían por azar? ¿Va en la dirección esperada un gen conocido de las células beta, como `PDX1` o `SLC2A2`? ¿Se parece a lo publicado?

✔ Sabes cuántos genes salen, cuántos esperarías por azar y si el gen conocido se comporta como se espera.

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
| Tarda mucho | Pídele que pruebe primero con 1.000 sondas y anótalo como decisión |
| Da muchas cifras y no las entiendes | «Explícamelo con un solo gen: ¿sube o baja con la HbA1c, y cuánto?» |
| Dice que un gen «causa» la diabetes | Recuérdale la regla: con estos datos solo se ve una asociación |
| Dos parejas tienen resultados distintos | Comparad vuestros DECISIONES.md: ahí está la explicación |
