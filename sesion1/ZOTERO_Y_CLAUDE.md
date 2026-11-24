# Conectar Zotero a Claude (MCP)

**Para qué sirve:** le pides a Claude que busque bibliografía sobre un tema y él mete los artículos directamente en tu Zotero (por DOI), en la colección que digas. También puede buscar en lo que ya tienes, sacarte el BibTeX, leer tus anotaciones o crear colecciones y etiquetas.

**Qué necesitas:**
- La app de escritorio de Claude (Windows, Mac o Linux)
- Una cuenta de Zotero con la **sincronización activada** (Zotero → Ajustes → Sincronización)
- 15 minutos

> **Cómo funciona por dentro:** Claude no toca tu Zotero de escritorio. Escribe en tu biblioteca *online* de zotero.org, y tu Zotero de escritorio lo recibe al sincronizar. Por eso hace falta la sincronización.

---

## Paso 1 · Crear tu llave de acceso a Zotero

1. Entra en **https://www.zotero.org/settings/keys** (con tu cuenta).
2. Arriba verás una frase como *"Your userID for use in API calls is **1234567**"*. **Apunta ese número**: es tu **Library ID**.
3. Pulsa **Create new private key**:
   - Nombre: `Claude`
   - Marca **Allow library access** y **Allow write access**
   - Guarda. Te mostrará una clave de 24 caracteres: **cópiala** (solo se ve una vez).

⚠️ Esa clave es como una contraseña de tu biblioteca. No la pegues en chats ni la mandes por correo. Si algún día quieres cortar el acceso, bórrala en esa misma página.

## Paso 2 · Instalar `uv` (el programa que arranca el conector)

Abre una terminal y pega:

| Sistema | Comando |
|---|---|
| **Mac / Linux** | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Windows** (PowerShell) | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |

Cierra y abre la terminal, y averigua **dónde se ha instalado**:

- Mac / Linux: `which uvx` → algo como `/Users/ana/.local/bin/uvx`
- Windows: `where.exe uvx` (con el `.exe`) → algo como `C:\Users\ana\.local\bin\uvx.exe`

**Apunta esa ruta.** Claude la necesita completa (no basta con poner `uvx`).

## Paso 3 · Decirle a Claude que use el conector

En la app de Claude: **Ajustes → Desarrollador → Editar configuración**. Se abre un fichero llamado `claude_desktop_config.json`.

Añade el bloque `mcpServers` **sustituyendo las tres partes en mayúsculas**:

```json
"mcpServers": {
  "zotero": {
    "command": "RUTA_DE_UVX",
    "args": ["--from", "zotero-library-mcp", "zotero-mcp"],
    "env": {
      "ZOTERO_LIBRARY_ID": "TU_NUMERO",
      "ZOTERO_API_KEY": "TU_CLAVE"
    }
  }
}
```

**Dónde ponerlo.** El fichero es *una sola* caja `{ ... }`. El bloque va **dentro** de esa caja, al mismo nivel que lo que ya haya, separado por una coma:

```json
{
  "preferences": { ...lo que ya había, sin tocar... },
  "mcpServers": {
    "zotero": { ... }
  }
}
```

En Windows, en la ruta escribe las barras dobles: `C:\\Users\\ana\\.local\\bin\\uvx.exe`

## Paso 4 · Reiniciar Claude *del todo*

Cerrar la ventana no basta: la app suele quedarse abierta en segundo plano.
- **Windows:** clic derecho en el icono de Claude junto al reloj → Salir
- **Mac:** `Cmd + Q`
- **Linux:** salir desde el icono de la bandeja, o `pkill -f -i claude`

Vuelve a abrirla.

## Paso 5 · Comprobar

Escríbele a Claude: *"Comprueba la conexión con mi Zotero y lista mis colecciones"*.

Si te devuelve tus colecciones, ya está. Prueba algo real:
> *"Busca 10 artículos recientes sobre X, comprueba que sus DOI existen y añádelos a una colección nueva llamada X-revisión."*

---

## Si no funciona: los 4 fallos típicos

| Síntoma | Causa probable | Solución |
|---|---|---|
| Claude no ve ninguna herramienta de Zotero | La app no se reinició de verdad | Paso 4 otra vez |
| Igual, tras reiniciar | El JSON está mal (falta una coma, sobra una llave, hay dos cajas `{ }`) | Pega el fichero en https://jsonlint.com **quitando antes la clave** |
| Error de credenciales | El *Library ID* no es el número del Paso 1 (p. ej. pusiste el nombre de una colección) | Es el número de *"Your userID…"* |
| No arranca | Se quedó un texto de ejemplo (`RUTA_DE_UVX`, `TU_NUMERO`…) o la ruta de `uvx` está mal | Revisa las tres partes en mayúsculas |

Si no lo ves claro, ve a **Ajustes → Desarrollador**: ahí aparece `zotero` con su estado y un enlace al log de errores.

---

## Buenas prácticas

- **Revisa lo que entra.** Pídele a Claude que compruebe los DOI y échale un ojo a la colección antes de citar nada.
- **Usa colecciones nuevas para cada búsqueda** (`tema-fecha`). Así, si algo no te convence, lo borras de golpe sin tocar el resto.
- **Una clave por herramienta.** Si conectas Zotero a otras apps, crea una clave para cada una. Así puedes revocar solo la que quieras.

*Conector: [zotero-library-mcp](https://github.com/RaulSimpetru/zotero-library-mcp) (código abierto, licencia MIT).*
