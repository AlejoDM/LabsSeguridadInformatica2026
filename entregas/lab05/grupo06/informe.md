# Informe — Laboratorio 05 · Reconocimiento

**Grupo:** 06
**Integrantes:**

| Nombre y apellido    | Usuario de GitHub |
| -------------------- | ----------------- |
| Martín Beccereca     | martinbeccereca   |
| Belén Benito         | belubenito01      |
| Alejo José De Miguel | AlejoDM           |
| Tomás Giudici        | TomasGiudici      |
| Carolina Suppo       | carosuppo         |

## 0. Declaración de uso de IA

**Herramienta: Claude Code**

- **Finalidad del uso:** Apoyo en la ejecución del recon y en la redacción de las filas del mapa y de P1.
- **Partes generadas o asistidas:** Sección 2, P1 y carpeta `evidencia/`.
- **Verificación:** Las salidas se guardaron crudas con redirección desde la consola del atacante.

**Herramienta: ChatGPT**

- **Finalidad del uso:** Apoyo en la investigación sobre OSINT y reconocimiento pasivo, interpretación de los comandos `whois` y `dig`, y redacción de la respuesta P4.
- **Partes asistidas:** Archivo `research.md` y pregunta P4 de `informe.md`.
- **Verificación:** Se ejecutaron los comandos en el entorno Docker del laboratorio y se guardaron sus resultados en `evidencia/salidas/`.

**Herramienta: Opencode**

- **Finalidad del uso:** Apoyo puntual para ejecutar y ordenar los comandos del recon del puerto 8080, y para revisar la redacción de la fila del mapa, P2 y la bitácora.
- **Partes asistidas:** R5, sección 2 (fila 8080), P2 y sección 4 de `informe.md`; el análisis de los hallazgos, las decisiones y la validación final fueron del grupo.
- **Verificación:** El grupo revisó y validó los comandos y sus salidas; se corrieron en `cyberlab-attacker` y se guardaron crudas con `tee` en `/loot`, copiadas sin edición a `evidencia/salidas/`.

## 1. Parte práctica — flags capturadas

- **R3:** `FLAG{http_headers_leak_info}`, encontrada por el usuario en `X-Backend-Flag` al ejecutar `curl -I http://phantomcorp`. Se conservó su evidencia original sin sobrescribirla.
- **R4:** `FLAG{recon_hidden_path}`, encontrada en el cuerpo HTML de `/panel-interno-9x2f`, ruta publicada en `/robots.txt`.
- **R5:** `FLAG{dev_service_exposed}`, devuelta por el endpoint `/status` del servicio de desarrollo del puerto 8080. Evidencia: [respuesta de /status](evidencia/salidas/http8080-status.txt) y [validación R5](evidencia/salidas/ctf-submit-r5.txt).

R3, R4 y R5 fueron aceptadas por el mecanismo ctf. Evidencia cruda: [validación R3](evidencia/salidas/ctf-submit-r3.txt), [validación R4](evidencia/salidas/ctf-submit-r4.txt), [validación R5](evidencia/salidas/ctf-submit-r5.txt) y [salida completa de ctf status 05](evidencia/salidas/ctf-status-05.txt). Esta captura corresponde al registro histórico de R3/R4 (2/5) y no al progreso consolidado del grupo.

Confirmación de R3, R4 y R5 (extractos de las validaciones):

```text
[ OK ] Reto R3 resuelto: Fuga de informacion en headers HTTP
[ OK ] Reto R4 resuelto: Enumeracion de rutas via robots.txt
[ OK ] Reto R5 resuelto: Servicio dev expuesto en produccion
```

Salida de `./ctf status 05` del registro histórico de R3/R4 (2/5; la captura consolidada con las 5 flags queda para la integración final):

```text

  ╭────────────────────────────────────────────────────────────╮
  │                     PROGRESO · LAB 05                      │
  ╰────────────────────────────────────────────────────────────╯

   ·  R1     Puerto oculto en rango alto (barrido completo)
   ·  R2     Banner grabbing del servicio FTP
   ✓  R3     Fuga de informacion en headers HTTP
   ✓  R4     Enumeracion de rutas via robots.txt
   ·  R5     Servicio dev expuesto en produccion

  ████████████░░░░░░░░░░░░░░░░░░  2/5 (40%)
```

## 2. Mapa de superficie de ataque

| Puerto | Servicio                                                           | Versión (evidencia)                                                                                                                                                        | ¿Cómo lo identificaste?                                                                                                                                                 | CVE relevante                                                                                                                                       | CVSS                                                                  | Criticidad                                                                 | Justificación (contra ESTE caso)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ------ | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 21     | FTP                                                                | ProFTPD 1.3.5 — banner `220 ProFTPD 1.3.5 Server (PhantomCorp FTP)`; nmap `-sV`: `21/tcp open ftp ProFTPD 1.3.5`                                                           | Banner grabbing con `ncat -w2 phantomcorp 21` y confirmado con `nmap -Pn -sV -p-`                                                                                       | CVE-2015-3306 (`mod_copy`, comandos `SITE CPFR`/`SITE CPTO`)                                                                                        | 9.8 (CVSS v3.x, NVD)                                                  | Crítica                                                                    | El banner confirma la versión 1.3.5, que es la afectada por el CVE. Permite leer y escribir archivos arbitrarios sin autenticarse **si** `mod_copy` está cargado; en este recon no lo probamos, queda para el lab de explotación. Además el banner filtra el nombre de la empresa y una línea `214` que no debería estar.                                                                                                                                                                                                                                                                                                                               |
| 80/tcp | HTTP                                                               | Headers: `Server: PhantomServer/2.4.1` y `X-Powered-By: PhantomCMS 2.4.1`; respuesta `HTTP/1.0 200 OK`. Versiones anunciadas, sin verificación independiente del software. | HEAD a `http://phantomcorp` con curl; GET a `/robots.txt` y a `/panel-interno-9x2f`, todos sobre HTTP sin puerto explícito (80).                                        | No determinado: las respuestas no permiten vincular estos nombres/versiones con un CVE verificable. No se atribuye un CVE por similitud de nombres. | No asignado; no se calculó un vector ni se verificó un CVE aplicable. | Media, valoración cualitativa para la exposición de información observada. | Los headers revelan producto, versión y una flag. robots.txt publica una ruta interna y un comentario de infraestructura; la ruta responde 200 y entrega el panel y otra flag sin credenciales. Esto facilita reconocimiento y expone contenido interno. No se demostró ejecución de comandos, modificación de datos ni acceso a funciones administrativas.                                                                                                                                                                                                                                                                                             |
| 8080   | HTTP / API de desarrollo (`phantom-dev-api`)                       | `Werkzeug/2.0.1 Python/3.9.2` — header `Server:` y nmap `8080/tcp open http Werkzeug httpd 2.0.1 (Python 3.9.2)`; el cuerpo de `/status` agrega `"version":"0.9.3-DEV"`    | `nmap -Pn -sV -p 8080 phantomcorp` para producto/versión; `curl -sS -i http://phantomcorp:8080/` (raíz) y `curl -sS -i http://phantomcorp:8080/status` para el endpoint | No determinado: no se vinculó la versión anunciada a un CVE verificado y no se atribuye un CVE por similitud de nombres.                            | N/A (sin CVE verificado)                                              | Alta                                                                       | El servicio se identifica como API de desarrollo (`phantom-dev-api`, versión `0.9.3-DEV`) y expone `/status` sin autenticación con `"debug":true`, la versión interna y la flag. Corre sobre el servidor de desarrollo de Werkzeug, no sobre un WSGI de producción, en un puerto no estándar (8080) que queda fuera del portal corporativo del 80. Aunque no se haya verificado un CVE, el problema es concreto: entrega información de configuración y de versión, confirma que hay código de desarrollo en producción y facilita el reconocimiento. No se probó ejecución de comandos ni acceso al debugger; solo se comprobó la fuga de información. |
| 31337  | Desconocido (nmap lo adivina como `Elite` por el número de puerto) | "PhantomCorp maintenance shell v0.1" — banner de `ncat -w2 phantomcorp 31337`; nmap `-sV`: `31337/tcp open Elite?`                                                         | `nmap -sV -p-` no lo reconoció; lo identificamos conectando con `ncat` y leyendo el banner                                                                              | Ninguno identificado. No pude asociar este banner a un producto con CVE público                                                                     | N/A                                                                   | Alta                                                                       | Es un shell de mantenimiento propio, expuesto a la red y en un puerto clásico de backdoors. Responde sin pedir credenciales y su banner dice "acceso no autorizado prohibido", lo que confirma que no debería estar expuesto. No determiné qué comandos acepta, así que no afirmo más que eso.                                                                                                                                                                                                                                                                                                                                                          |

Headers relevantes del puerto 80 (extracto):

```text
HTTP/1.0 200 OK
Server: PhantomServer/2.4.1
X-Powered-By: PhantomCMS 2.4.1
X-Backend-Flag: FLAG{http_headers_leak_info}
```

Evidencia completa, sin editar:

- [Escaneo de puertos predeterminado](evidencia/salidas/nmap-default.txt).
- [Escaneo completo con detección de versiones](evidencia/salidas/nmap-sV-all.txt).
- [Banner del puerto 31337](evidencia/salidas/r1-banner-31337.txt).
- [Banner FTP del puerto 21](evidencia/salidas/r2-banner-ftp21.txt).
- [Detección de versión del puerto 8080](evidencia/salidas/nmap-8080.txt).
- [Respuesta de la raíz del 8080](evidencia/salidas/http8080-root.txt).
- [Respuesta del endpoint /status del 8080](evidencia/salidas/http8080-status.txt).

- [Headers originales de R3](evidencia/salidas/http80-headers.txt).
- [Respuesta de robots.txt](evidencia/salidas/http80-robots.txt).
- [Respuesta del panel interno](evidencia/salidas/http80-panel-interno.txt).

La identificación de la fila del puerto 80 se basa en HTTP observado con curl, no en un escaneo nmap. `HTTP/1.0` es la versión del protocolo de respuesta, no la versión del producto. Las fechas de los headers están en GMT.

## 3. Preguntas de análisis

**P1 — El puerto que el escaneo default se perdió.**
En nuestra corrida el escaneo default (`nmap -Pn phantomcorp`, 1000 puertos) y el
completo (`nmap -Pn -sV -p- phantomcorp`) encontraron los mismos cuatro puertos:
21, 80, 8080 y 31337. El 31337 aparece en el default porque nmap incluye en su
lista de los 1000 más frecuentes a ese puerto histórico de backdoors. Lo que el
default sí se perdió fue la **identificación**: sin `-sV` el puerto figuró como
`Elite` (un nombre que nmap deduce solo del número de puerto) y recién con `-sV`
vimos que ahí responde un "maintenance shell" de PhantomCorp. Entonces `-p-` no
nos sumó un puerto nuevo en este caso, pero la lección operativa es la misma:
el default cubre 1000 de 65535 puertos, así que cualquier servicio fuera de esa
lista pasa desapercibido, y un puerto abierto sin versión no es un hallazgo.
Para los próximos recon hacemos siempre `-p-` con `-sV`, y confiamos en la
columna VERSION y en el banner, no en la columna SERVICE.

**P2 — El servicio dev en producción.**

La evidencia concreta está en lo que devuelve el propio servicio. `nmap -Pn -sV -p 8080 phantomcorp` lo identifica como `Werkzeug httpd 2.0.1 (Python 3.9.2)`, que es el servidor de desarrollo de Flask/Werkzeug, no un servidor WSGI de producción como Gunicorn o uWSGI. El header confirma lo mismo: `Server: Werkzeug/2.0.1 Python/3.9.2`. Al pedir la raíz, `curl -sS -i http://phantomcorp:8080/` responde `phantom-dev-api. Proba /status`, y `/status` devuelve JSON con `"version":"0.9.3-DEV"` y `"debug":true`.

Esos tres indicios —prefijo `dev`, sufijo `-DEV` y `debug:true`— dicen que es una API de desarrollo. Además corre en el puerto 8080, fuera del 80 del portal corporativo, lo que sugiere que se levantó como excepción y no pasó por los controles del sitio principal.

Es un problema aunque no tenga un CVE conocido porque el riesgo no depende de una vulnerabilidad concreta: el servicio no pide credenciales, expone su estado interno y anuncia producto y versión. Un atacante puede usarlo como punto de entrada para probar el modo debug o para buscar fallas en una versión de desarrollo que nunca fue endurecida. Además, un servicio dev en producción suele quedar fuera de los parches, del monitoreo y de los logs del portal principal. La respuesta `/status` ya incluye `"debug":true` y la flag, así que la fuga de información es real y verificada; no afirmamos ejecución de comandos porque no la probamos.

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

Extracto del cuerpo HTML recibido del panel:

```html
<h1>Panel interno PhantomCorp</h1>
<p>
  Acceso restringido. Si llegaste aca por robots.txt, felicitaciones: acabas de
  hacer enumeracion de rutas. Esa es exactamente la tecnica.
</p>
<pre>FLAG{recon_hidden_path}</pre>
```

La evidencia demuestra acceso desde el contenedor atacante al panel dentro de la red del laboratorio; el comentario dice «desde afuera», pero no comprobamos exposición a Internet. `/admin` solo se observó listado y no se consultó. La conclusión es que ocultar o desaconsejar el rastreo de una ruta no protege su contenido: el acceso debe controlarse en el servidor. La evidencia de este caso está en las respuestas completas de robots.txt y del panel enlazadas arriba.

**P4 — Pasivo vs. activo.**

El reconocimiento pasivo consiste en recopilar información de un objetivo sin interactuar directamente con sus sistemas. En este laboratorio lo practicamos utilizando `whois nmap.org`, con el que obtuvimos datos del registro del dominio, como su fecha de creación y servidores DNS. También utilizamos `dig scanme.nmap.org A`, que nos permitió identificar su dirección IP mediante una consulta DNS.

En cambio, el reconocimiento activo implica comunicarse directamente con el objetivo para obtener información. Un ejemplo de esto fue el uso de `nmap` contra PhantomCorp para identificar puertos abiertos y servicios, y de `curl` para consultar las cabeceras HTTP y el archivo `robots.txt`.

La principal diferencia es la huella que dejamos. Las consultas de WHOIS y DNS se realizaron a servicios externos y no directamente a PhantomCorp, mientras que los escaneos de `nmap`, las conexiones con `ncat` y las solicitudes de `curl` generaron tráfico hacia sus servicios. Estas últimas acciones podrían haber quedado registradas en los logs de PhantomCorp, dependiendo de la configuración del servidor.

Esto nos permitió entender que el reconocimiento pasivo sirve para reunir información inicial con menor interacción directa, mientras que el activo permite conocer con más detalle los servicios expuestos, pero genera tráfico que puede ser detectado.

**Evidencias del reconocimiento pasivo:**

- [Consulta WHOIS de nmap.org](evidencia/salidas/p4-whois.txt).
- [Consulta DNS de scanme.nmap.org](evidencia/salidas/p4-dig.txt).

**P5 — Ahora sos el defensor.**

## 4. Bitácora de comandos

Dentro de `cyberlab-attacker`:

```bash
nmap -Pn phantomcorp > /loot/nmap-default.txt
nmap -Pn -sV -p- phantomcorp > /loot/nmap-sV-all.txt
ncat -w2 phantomcorp 31337 </dev/null > /loot/r1-banner-31337.txt
ncat -w2 phantomcorp 21 </dev/null > /loot/r2-banner-ftp21.txt
curl -I http://phantomcorp | tee /loot/http80-headers.txt
curl -sS -i http://phantomcorp/robots.txt | tee /loot/http80-robots.txt
curl -sS -i http://phantomcorp/panel-interno-9x2f | tee /loot/http80-panel-interno.txt
nmap -Pn -sV -p 8080 phantomcorp | tee /loot/nmap-8080.txt
curl -sS -i http://phantomcorp:8080/ | tee /loot/http8080-root.txt
curl -sS -i http://phantomcorp:8080/status | tee /loot/http8080-status.txt
```

Desde Bash de Git, en la raíz del repositorio:

```bash
./ctf submit 05 R3 'FLAG{http_headers_leak_info}'
./ctf submit 05 R4 'FLAG{recon_hidden_path}'
./ctf submit 05 R5 'FLAG{dev_service_exposed}'
./ctf status 05
```

Ver [evidencia/comandos.txt](evidencia/comandos.txt): separa las acciones previas informadas por el usuario de las ejecutadas en esta continuación e identifica dónde se ejecuta cada comando. Las salidas originales permanecen en `/loot`, montado como `.loot/` del repositorio, y se copiaron sin edición a `evidencia/salidas/` para versionarlas.

## Pendientes de integración del grupo
