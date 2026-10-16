# Informe — Laboratorio 05 · Reconocimiento

**Grupo:** 06
**Integrantes:**
**Fecha:** 16/10/2026
**Alcance de este aporte:** R3, R4, puerto 80 y P3.

## 0. Declaración de uso de IA

## 1. Parte práctica — flags capturadas

- **R3:** `FLAG{http_headers_leak_info}`, encontrada por el usuario en `X-Backend-Flag` al ejecutar `curl -I http://phantomcorp`. Se conservó su evidencia original sin sobrescribirla.
- **R4:** `FLAG{recon_hidden_path}`, encontrada en el cuerpo HTML de `/panel-interno-9x2f`, ruta publicada en `/robots.txt`.

Ambas fueron aceptadas por el mecanismo ctf. Evidencia cruda: [validación R3](evidencia/salidas/ctf-submit-r3.txt), [validación R4](evidencia/salidas/ctf-submit-r4.txt) y [salida completa de ctf status 05](evidencia/salidas/ctf-status-05.txt).

## 2. Mapa de superficie de ataque

| Puerto | Servicio | Versión (evidencia) | ¿Cómo lo identificaste? | CVE relevante | CVSS | Criticidad | Justificación (contra ESTE caso) |
|---|---|---|---|---|---|---|---|
| 21 | | | | | | | |
| 80/tcp | HTTP | Headers: `Server: PhantomServer/2.4.1` y `X-Powered-By: PhantomCMS 2.4.1`; respuesta `HTTP/1.0 200 OK`. Versiones anunciadas, sin verificación independiente del software. | HEAD a `http://phantomcorp` con curl; GET a `/robots.txt` y a `/panel-interno-9x2f`, todos sobre HTTP sin puerto explícito (80). | No determinado: las respuestas no permiten vincular estos nombres/versiones con un CVE verificable. No se atribuye un CVE por similitud de nombres. | No asignado; no se calculó un vector ni se verificó un CVE aplicable. | Media, valoración cualitativa para la exposición de información observada. | Los headers revelan producto, versión y una flag. robots.txt publica una ruta interna y un comentario de infraestructura; la ruta responde 200 y entrega el panel y otra flag sin credenciales. Esto facilita reconocimiento y expone contenido interno. No se demostró ejecución de comandos, modificación de datos ni acceso a funciones administrativas. |
| 8080 | | | | | | | |
| 31337 | | | | | | | |

Evidencia completa, sin editar:

- [Headers originales de R3](evidencia/salidas/http80-headers.txt).
- [Respuesta de robots.txt](evidencia/salidas/http80-robots.txt).
- [Respuesta del panel interno](evidencia/salidas/http80-panel-interno.txt).

La identificación de esta fila se basa en HTTP observado con curl, no en un escaneo nmap. `HTTP/1.0` es la versión del protocolo de respuesta, no la versión del producto. Las fechas de los headers están en GMT.

## 3. Preguntas de análisis

**P1 — El puerto que el escaneo default se perdió.**

**P2 — El servicio dev en producción.**

**P3 — La ironía de robots.txt.**

robots.txt permite comunicar a los rastreadores qué rutas se les pide que no rastreen. No implementa autenticación ni autorización: una directiva Disallow no impide que alguien solicite esa URL y tampoco garantiza que una dirección no aparezca indexada.

En este laboratorio, `curl -sS -i http://phantomcorp/robots.txt` devolvió `HTTP/1.0 200 OK` y el siguiente contenido:

```text
User-agent: *
Disallow: /admin
Disallow: /panel-interno-9x2f
# Recordatorio infra: /panel-interno-9x2f sigue accesible desde afuera. Migrar a VPN.
```

La ironía es que, al intentar apartar rutas de los rastreadores, el archivo público revela sus nombres exactos a quien está haciendo reconocimiento. El comentario además señala una exposición pendiente de corregir. Seguimos esa pista con `curl -sS -i http://phantomcorp/panel-interno-9x2f`: sin enviar credenciales ni cookies, recibimos `HTTP/1.0 200 OK`, el título «Panel interno PhantomCorp» y `FLAG{recon_hidden_path}`. El texto «Acceso restringido» del HTML no evitó que se entregara ese contenido.

La evidencia demuestra acceso desde el contenedor atacante al panel dentro de la red del laboratorio; el comentario dice «desde afuera», pero no comprobamos exposición a Internet. `/admin` solo se observó listado y no se consultó. La conclusión es que ocultar o desaconsejar el rastreo de una ruta no protege su contenido: el acceso debe controlarse en el servidor. La evidencia de este caso está en las respuestas completas de robots.txt y del panel enlazadas arriba.

**P4 — Pasivo vs. activo.**

**P5 — Ahora sos el defensor.**

## 4. Bitácora de comandos

Ver [evidencia/comandos.txt](evidencia/comandos.txt): separa las acciones previas informadas por el usuario de las ejecutadas en esta continuación e identifica dónde se ejecuta cada comando. Las salidas originales permanecen en `/loot`, montado como `.loot/` del repositorio, y se copiaron sin edición a `evidencia/salidas/` para versionarlas.

## Pendientes de integración del grupo
