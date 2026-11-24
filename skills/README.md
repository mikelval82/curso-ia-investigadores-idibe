# grill-me y grilling

Son de [Matt Pocock](https://github.com/mattpocock/skills), versión 1.2.3, sin modificar y con su licencia MIT. Sirven para poner a prueba un plan, una decisión o una idea: Claude te pregunta hasta que queda claro. `grill-me` solo llama a `grilling`, así que hacen falta las dos.

## Usarlas

- **En una práctica:** la sesión 2 trae solo grilling, en `skills/grilling/`, que se lee directamente. La sesión 3 y la [plantilla](../plantilla/README.md) traen las dos en `.claude/skills/`, para usar `/grill-me`.
- **En otro proyecto con Claude Code:** copia las dos carpetas en `.claude/skills/` y escribe `/grill-me`.
- **Con Codex:** `/grill-me` no aparece. Pídele: «Lee `.claude/skills/grilling/SKILL.md` y aplícalo a mi plan».

## Modificarlas

Una skill es un archivo de texto, `SKILL.md`. Ábrelo, cambia lo que quieras y prueba otra vez. Por ejemplo, en `grilling/SKILL.md`:

| Original | La tuya |
|---|---|
| «Ask the whole frontier in one round» | «Pregunta de una en una, cinco preguntas como mucho, en español» |

Cambia una cosa cada vez y comprueba si hace lo que esperabas. Si compartes tu versión, conserva `LICENSE.txt`.

**Lee siempre una skill antes de instalarla:** son instrucciones que Claude va a seguir.
