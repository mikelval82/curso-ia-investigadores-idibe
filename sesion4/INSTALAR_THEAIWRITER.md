# Sesión 4 · Preparación previa: TheAIWriter

**Objetivo.** Llegar al 18 de diciembre con el plugin instalado, los PDF en Zotero y la comprobación en verde.

TheAIWriter es un plugin de Claude Code. Sirve para escribir documentos científicos con los PDF de tu Zotero y comprobar que cada cita dice lo que dice el artículo. El plugin no escribe en Zotero.

- Manual: [PDF](manual-theaiwriter.pdf) · [HTML](manual-theaiwriter.html) (descárgalo y ábrelo en el navegador; sin internet se ve con otra letra) · [en GitHub](https://github.com/mikelval82/TheAiWriter/blob/master/docs/manual.md)
- [Cómo pasar el texto a Word o LibreOffice](https://github.com/mikelval82/TheAiWriter/blob/master/docs/exportar.md)
- [Repositorio](https://github.com/mikelval82/TheAiWriter). Versión de este manual: 0.5.3, candidata.

> **Probado solo en Linux.** Windows y Mac están pendientes. Prueba la instalación con tiempo y, si falla, sigue con la alternativa del final: la entrega es la misma.

---

## Antes de empezar

De la [receta de la sesión 1](https://github.com/mikelval82/curso-ia-investigadores-idibe/blob/main/sesion1/RECETA_ENTORNO.md) ya tienes:

- [ ] La app de Claude con la pestaña **Code** y tu plan de pago.
- [ ] **Zotero de escritorio** en este mismo ordenador.
- [ ] **uv**.

Necesitas además internet y espacio para el modelo de búsqueda, que ocupa unos cientos de MB.

## 1. Pon los PDF en Zotero

Importar un archivo RIS puede dejar los artículos sin su PDF, y sin PDF no se pueden citar.

1. En tu colección, selecciona los artículos de **lectura obligatoria**.
2. Clic derecho y **Buscar texto completo** (*Find Full Text*). Lo que no encuentre, descárgalo con tu acceso institucional y arrástralo sobre su ficha.
3. Abre uno y comprueba que puedes seleccionar el texto. Los PDF escaneados no sirven.

✔ Al menos tres artículos de tu colección tienen PDF con texto.

## 2. Instala el plugin

En la pestaña **Code**, en una sesión local, escribe estas dos órdenes, una cada vez:

```text
/plugin marketplace add mikelval82/TheAiWriter
```

```text
/plugin install theaiwriter@theaiwriter
```

Si la app no las reconoce y tienes Claude Code en la terminal, prueba allí:

```text
claude plugin marketplace add mikelval82/TheAiWriter
```

```text
claude plugin install theaiwriter@theaiwriter
```

Cierra Claude del todo y vuelve a abrirlo.

## 3. Comprueba

```text
/theaiwriter:diagnostico
```

✔ Encuentra tu carpeta de Zotero y te dice cuántas obras tienen PDF.

## 4. Prepara el índice en casa

La primera vez descarga el modelo de búsqueda y lee tus PDF. Hazlo **antes de clase**, con buena conexión:

```text
/theaiwriter:diagnostico actualiza el índice
```

✔ Termina sin errores.

---

## Lo que conviene saber

| Tema | Qué pasa |
|---|---|
| **Gasto** | Consume tu plan de Claude: la conversación, una llamada por cada párrafo con citas cuando actúa el juez y una por cada revisión. «Comprobar sin juez» no hace llamadas aparte |
| **Tus datos** | El índice se guarda en tu ordenador, pero lo que Claude lee de los PDF y de tu borrador se envía a Anthropic. No pongas datos de pacientes, resultados sin publicar ni manuscritos ajenos |
| **Errores** | El juez y el revisor se equivocan a veces. Mira lo que señalan; no lo borres sin más |
| **PDF** | No lee los escaneados y solo cita obras con PDF en Zotero |
| **Citas vivas** | Con Better BibTeX, probadas en LibreOffice. En Word, sin probar |
| **Licencia** | El código es MIT, pero usa PyMuPDF, que es AGPL |

## Si usas Codex o no puedes instalarlo

TheAIWriter solo funciona en Claude Code. Trae a clase tu colección y los PDF: harás la misma entrega con tu asistente y comprobarás a mano tres frases contra los artículos. Las instrucciones están en la [guía de la práctica](GUIA_PRACTICA.md#si-usas-codex-o-no-tienes-el-plugin).

## Si algo falla

| Síntoma | Qué hacer |
|---|---|
| No aparecen las órdenes `/theaiwriter:` | Cierra Claude del todo y ábrelo. Comprueba que es una sesión local |
| Falla al añadir el repositorio | Comprueba que Git está instalado: `git --version` |
| No encuentra Zotero | Abre Zotero de escritorio una vez y repite el diagnóstico |
| Un artículo no aparece | Mira que tenga el PDF y actualiza el índice |
