# Sesión 1 · Receta para preparar tu entorno

Objetivo: dejar listo tu ordenador para todo el curso. Sigue los pasos en orden. Cada paso termina con una comprobación ✔; no pases al siguiente hasta verla. Tiempo aproximado: 60–75 minutos (menos si traes las cuentas creadas).

## Ingredientes

- **Portátil** con Windows 10/11, macOS o Linux, cargador y unos 5 GB libres.
- **Permiso para instalar programas** en el portátil. Si es un equipo de la UMH gestionado por el servicio informático, pídelo antes del curso.
- **Correo institucional** (@umh.es) y acceso a tu gestor de contraseñas o a una libreta para apuntar claves.
- **Plan de pago de Claude** (Pro o superior). Cada participante usa el suyo. El curso se enseña con Claude; con Codex (plan de ChatGPT) puedes seguirlo, pero algunos pasos cambian.
- **Navegador** Chrome, Firefox, Edge o Safari actualizado.
- **El móvil**, por si alguna cuenta pide un código de verificación.

---

## Parte A · Cuentas (15 min)

Crea las cuentas con tu correo institucional, salvo la de Claude si ya tienes una. Apunta qué correo usas en cada una.

1. **Claude**: [claude.ai](https://claude.ai). Contrata el plan Pro si no lo tienes.
2. **Zotero**: [zotero.org/user/register](https://www.zotero.org/user/register). Gratuita.
3. **Research Rabbit**: [researchrabbit.ai](https://www.researchrabbit.ai). Gratuita.
4. **Consensus**: [consensus.app](https://consensus.app). Gratuita, con búsquedas limitadas.
5. **SciSpace**: [scispace.com](https://scispace.com). Gratuita, con funciones limitadas.

✔ Puedes entrar en las cinco con tu correo y contraseña.

## Parte B · Privacidad de Claude (2 min)

6. En claude.ai: **Ajustes → Privacidad**. Desactiva **«Ayudar a mejorar Claude»** si no quieres que tus conversaciones se usen para entrenar modelos.
7. Recuerda la regla de la sesión: no subas datos de pacientes, datos personales ni manuscritos ajenos en evaluación.

✔ La opción aparece desactivada.

## Parte C · Instalar las aplicaciones (20 min)

Instálalas en este orden:

8. **Claude** para escritorio: [claude.com/download](https://claude.com/download). Ábrela e inicia sesión con tu cuenta. Incluye el chat y la pestaña **Code** (Claude Code), que usaremos desde la sesión 2.
   - Si usas Codex: instala la app de Codex desde [chatgpt.com/codex](https://chatgpt.com/codex) e inicia sesión con tu cuenta de ChatGPT.
9. **Zotero** para escritorio: [zotero.org/download](https://www.zotero.org/download). Instala también el **Zotero Connector** para tu navegador desde la misma página.
10. **VS Code** (opcional): [code.visualstudio.com](https://code.visualstudio.com). Solo hace falta para el bonus de la sesión 3, donde se ven y editan los archivos del proyecto.
11. **uv**, el programa que arranca el conector de Zotero. Abre una terminal (en Windows, PowerShell) y pega:
    - Mac / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
    - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

    Cierra la terminal, ábrela de nuevo y escribe `which uvx` (Mac / Linux) o `where.exe uvx` (Windows, con el `.exe`). **Apunta la ruta completa** que aparece.

✔ Claude y Zotero se abren; la terminal te devuelve la ruta de `uvx`.

## Parte D · Preparar Zotero (5 min)

12. En Zotero de escritorio: **Editar (o Zotero) → Ajustes → Sincronización**. Entra con tu cuenta de Zotero y deja activada la sincronización.
13. Crea una colección de prueba llamada `Curso IDiBE` y guarda en ella un artículo cualquiera con el Zotero Connector del navegador.

✔ El artículo aparece en tu biblioteca de [zotero.org](https://www.zotero.org) tras sincronizar.

## Parte E · Conectar Zotero con Claude (15 min)

Claude no toca tu Zotero de escritorio: trabaja sobre tu biblioteca en línea y Zotero la recibe al sincronizar.

14. **Crea tu llave de acceso** en [zotero.org/settings/keys](https://www.zotero.org/settings/keys):
    - Apunta el número de «Your userID for use in API calls is …»: es tu **Library ID**.
    - Pulsa **Create new private key**, nombre `Claude`, marca **Allow library access** y **Allow write access**, y guarda.
    - Copia la clave en tu gestor de contraseñas. Solo se ve una vez. **No la pegues en ningún chat.**
15. **Dile a Claude que use el conector.** En la app de Claude: **Ajustes → Desarrollador → Editar configuración**. Se abre `claude_desktop_config.json`. Añade este bloque dentro de las llaves principales, separado por una coma de lo que ya hubiera, y sustituye las tres partes en mayúsculas:

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

    **Si el archivo está vacío o solo tiene `{}`**, borra lo que haya y pega esto entero:

    ```json
    {
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
    }
    ```

    En Windows, escribe la ruta con barras dobles: `C:\\Users\\ana\\.local\\bin\\uvx.exe`.

    **Si usas Codex**, en lugar de este paso abre `config.toml`, en la carpeta `.codex` de tu usuario, y añade al final:

    ```toml
    [mcp_servers.zotero]
    command = "RUTA_DE_UVX"
    args = ["--from", "zotero-library-mcp", "zotero-mcp"]

    [mcp_servers.zotero.env]
    ZOTERO_LIBRARY_ID = "TU_NUMERO"
    ZOTERO_API_KEY = "TU_CLAVE"
    ```

    En Windows, aquí también van barras dobles en la ruta. Esta parte está sin probar en clase: si falla, levanta la mano.
16. **Cierra Claude del todo**, no solo la ventana: en Windows, clic derecho en el icono junto al reloj → Salir; en Mac, `Cmd + Q`; en Linux, salir desde el icono de la bandeja. Vuelve a abrirla.
17. **Comprueba.** Escribe en un chat nuevo: *«Comprueba la conexión con mi Zotero y lista mis colecciones»*.

✔ Claude te devuelve tu colección `Curso IDiBE`.

Si no funciona, consulta la tabla de fallos típicos de la [guía completa de Zotero y Claude](ZOTERO_Y_CLAUDE.md) o levanta la mano.

## Parte F · Conectar las herramientas de búsqueda (10 min)

18. **Consensus en Claude**: en la app de Claude, **Ajustes → Conectores → Explorar conectores**, busca **Consensus**, pulsa **Conectar** e inicia sesión con tu cuenta de Consensus. Comprueba que el proveedor es Consensus, no una herramienta de demostraciones de ventas con el mismo nombre.
19. **PubMed y bioRxiv en Claude**: en el mismo sitio, busca y conecta los dos. Si te piden iniciar sesión y no tienes cuenta, avisa.
20. **Research Rabbit con Zotero**: en Research Rabbit, entra en tu biblioteca y usa **Import from Zotero** para traer la colección `Curso IDiBE`. La importación es gratuita; la sincronización en ambos sentidos requiere el plan de pago RR+.
21. **SciSpace**: solo comprueba que puedes entrar. Lo mencionaremos en la sesión 2.

✔ Claude responde a *«Busca en Consensus dos artículos sobre [tu tema]»* y tu colección aparece en Research Rabbit.

## Parte G · Lista final

Marca cada casilla antes de irte:

- [ ] Entro en Claude, Zotero, Research Rabbit, Consensus y SciSpace.
- [ ] He revisado la privacidad de mi cuenta de Claude.
- [ ] Claude y Zotero se abren en mi portátil.
- [ ] Zotero sincroniza con mi cuenta.
- [ ] Claude lista mis colecciones de Zotero.
- [ ] Claude busca en Consensus, PubMed y bioRxiv.
- [ ] Abro la pestaña **Code** de Claude y veo una carpeta de mi ordenador.
- [ ] Mi colección de prueba está en Research Rabbit.

Lo que no termines en clase, complétalo en casa con esta receta. **Para el 4 de diciembre** trae una pregunta científica de tu investigación y dos o tres artículos que conozcas sobre ella, guardados en Zotero.
