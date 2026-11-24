# ¿Qué datos puedo usar con Claude?

Una regla para todo el curso: **lo que Claude lee sale de tu ordenador.** Da igual que lo pegues en el chat, que lo abra desde una carpeta en la pestaña Code o que lo lea de Zotero: ese contenido viaja a Anthropic para que el modelo lo procese. Lo que Claude no abre se queda en tu ordenador.

## El semáforo

| | Qué es | Qué haces |
|---|---|---|
| 🟢 **Adelante** | Datos públicos (GEO, PRIDE, repositorios de imágenes…), artículos publicados, tus propios textos, código, datos sintéticos o de ejemplo | Úsalos con normalidad |
| 🟡 **Con cuidado** | Tus resultados sin publicar | Usa lo mínimo, sin identificadores, y mejor aún: que Claude no abra los datos (ver abajo) |
| 🔴 **No** | Datos de pacientes o de salud, aunque estén seudonimizados; cualquier dato personal; lo que te han dado en confidencia: manuscritos que revisas, proyectos que evalúas, datos de una empresa o con acuerdo de confidencialidad, una patente sin presentar | No los subas. Si tu investigación los necesita, pregunta antes al comité de ética o al delegado de protección de datos de tu institución |

**Si dudas, trátalo como 🔴 y pregunta.**

## Tus datos sin publicar: que Claude escriba el código sin verlos

No hace falta que Claude lea tus datos para ayudarte a analizarlos:

1. **Describe la estructura, no el contenido.** Qué columnas hay, qué significa cada una y qué tipo de valores tienen. Si hace falta, inventa tres filas de ejemplo.
2. **Pídele el programa.** «No abras la carpeta `datos/`. Con esta descripción, escribe un programa que haga…»
3. **Ejecútalo tú y mira el resultado.** Comparte con Claude solo lo necesario: un error, una tabla resumen, una figura sin datos sensibles.

Si decides que sí puede leer un archivo, quita antes lo que no haga falta: columnas que no uses, nombres, códigos de muestra que identifiquen a alguien.

## Configura tu cuenta

- **Ajustes → Privacidad → «Ayudar a mejorar Claude», desactivado.** Así tus conversaciones no se usan para entrenar modelos y se borran a los 30 días. Con la opción activada, pueden guardarse hasta cinco años, sin datos que te identifiquen.
- **No uses el pulgar arriba o abajo** con contenido delicado: esa valoración se guarda cinco años con la conversación.
- Lo anterior es para los planes personales (Free, Pro y Max), también en la pestaña Code. Los planes de empresa (Team y Enterprise) tienen otras condiciones: no entrenan con tus datos por defecto.

Condiciones consultadas el 24/11/2026 en la [ayuda de privacidad de Anthropic](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data). Pueden cambiar: revísalas tú.

## Antes de usar IA con un proyecto

- ¿Tu financiador, tu revista o tu acuerdo con colaboradores dicen algo sobre IA?
- ¿Los datos son tuyos o de tu grupo, y puedes decidir sobre ellos?
- ¿Puedes explicar qué ha hecho la IA y qué has comprobado tú?
