# Plantilla para tu proyecto

Una carpeta básica para trabajar con un asistente en tu propia investigación. Es un punto de partida: cámbiala a tu gusto.

## Qué trae

```text
mi-proyecto/
├── AGENTS.md        Instrucciones para el asistente
├── CLAUDE.md        Le dice a Claude que lea AGENTS.md
├── contexto/
│   ├── PROYECTO.md      Qué quieres saber, con qué datos y cómo trabajas
│   ├── HIPOTESIS.md     Tu hipótesis (de la sesión 2)
│   ├── PARADIGMA.md     Tu esquema de estudio (de la sesión 2)
│   └── DECISIONES.md    Qué se ha hecho y qué has decidido
├── datos/           Tus datos originales
├── analisis/        El código y sus resultados
└── .claude/skills/  grill-me y grilling
```

`.claude` es una carpeta oculta. Si no la ves, en VS Code aparece en la lista de archivos.

## Empezar

1. Extrae el ZIP y cambia el nombre de la carpeta por el de tu proyecto.
2. Rellena `contexto/`. Si hiciste la entrega de la sesión 2, copia de allí la hipótesis y el paradigma.
3. Copia tus datos en `datos/`.
4. Abre la carpeta en VS Code y, dentro, Claude Code. También puedes abrirla en la pestaña **Code** de la app de Claude.
5. Escribe:

   ```
   Lee AGENTS.md y el contexto. Dime qué has entendido y qué falta.
   ```

6. Comprueba que lo que dice coincide con lo que escribiste.

## Poner a prueba tu plan

Escribe `/grill-me` y cuéntale qué quieres hacer. Te preguntará hasta que quede claro.

Las dos skills son de [Matt Pocock](https://github.com/mattpocock/skills), sin modificar. Son archivos de texto: ábrelos y cámbialos si quieres que pregunten de otra forma. Conserva su `LICENSE.txt`.

## Retomar otro día

Abre una conversación nueva y escribe:

```
Lee AGENTS.md y contexto/DECISIONES.md. ¿Dónde lo dejamos?
```

Así no dependes de recordar el chat anterior.

## Cambiar la plantilla

`AGENTS.md` es tuyo. Si el asistente hace algo que no quieres, añade una línea. Si una línea no sirve, bórrala. Cambia una cosa cada vez y comprueba qué pasa.

## Guardar versiones

Si usas Git, `.gitignore` deja fuera `datos/` para que no subas tus datos por error. Haz una copia de seguridad de esa carpeta por tu cuenta.
