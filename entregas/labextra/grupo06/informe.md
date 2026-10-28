# Informe — Laboratorio Extra SSRF

**Grupo:** 06
**Fecha:** 2026-10-28

| Nombre y apellido | Usuario de GitHub |
|---|---|
| Martín Beccereca | martinbeccereca |
| Belén Benito | belubenito603 |
| Alejo José De Miguel | AlejoDM |
| Tomás Giudici | TomasGiudici |
| Carolina Suppo | carosuppo |

## 0. Declaración de uso de IA

**Herramienta:** Codex (OpenAI).

**Finalidad y partes asistidas:** apoyo para la ejecución de R3.
**Verificación realizada:** Se ejecutaron los comandos en el entorno autorizado del laboratorio y se analizaron las respuestas obtenidas para comprobar que el acceso al recurso interno se realizó mediante la vulnerabilidad SSRF. Se verificó la presencia de la información expuesta y se validó la flag mediante el sistema oficial de retos.

**Herramienta:** Opencode.

**Finalidad y partes asistidas:** apoyo para documentar R2 y redactar la respuesta P2 sobre el oráculo de escaneo.
**Verificación realizada:** Se contrastaron las solicitudes con las salidas crudas del contenedor del Lab Extra. La cadena mostrada por la intranet se presentó al verificador y fue rechazada; la comparación literal de los errores de R1 queda pendiente de las salidas de P1.

## 1. Cadena de explotación

### R1 — Panel interno en localhost

Pendiente del responsable P1. No se sondearon puertos para este aporte.

### R2 — Intranet en la red interna

Desde `cyberlab-attacker`, la solicitud directa a `http://phantomcorp-intra/` devolvió `curl: (6) Could not resolve host: phantomcorp-intra`; esto confirma que el nombre no se resolvió desde la consola, no que se haya observado un timeout o una conexión bloqueada por IP. En la topología del Compose del laboratorio, la consola atacante está en `labnet` y la intranet solo en `internalnet`, por lo que no hay acceso directo desde la consola. [Salida original](evidencia/salidas/08-p2-directo.txt).

Luego se envió `http://phantomcorp-intra/` como destino de `/preview` en `phantomcorp`. La respuesta HTTP 200 incluyó la página «Intranet PhantomCorp» y el contenido `FLAG{ssrf_intranet_descubierta}`, prueba de acceso indirecto a través del servidor web conectado a ambas redes. [Salida original](evidencia/salidas/09-p2-intranet-preview.txt).

La cadena observada se presentó al verificador con `./ctf submit extra R2 'FLAG{ssrf_intranet_descubierta}'`, pero respondió `[FAIL] Flag incorrecta para el reto R2`. Por lo tanto, queda comprobado el acceso indirecto y documentado el contenido recibido, pero R2 no se declara resuelto ni se afirma que esa cadena sea la flag válida. El estado consultado en esta sesión mostró 0/3; la captura 07 corresponde al estado documentado durante la ejecución anterior de P3. Se conservan el intento fallido y el estado observado después del intento. [Presentación](evidencia/salidas/11-p2-submit.txt) · [Estado](evidencia/salidas/12-p2-status.txt).

Para buscar más pistas sin adivinar rutas, se siguieron los dos enlaces publicados en la home. `/salud` devolvió únicamente el estado del servicio; `backups/clientes.json` devolvió la flag de R3 ya documentada, no otra flag para R2. [Home](evidencia/salidas/13-p2-intranet-home-recheck.txt) · [Salud](evidencia/salidas/14-p2-salud-recheck.txt) · [Backup enlazado](evidencia/salidas/15-p2-backup-link.txt). No se observó otra cadena de R2 en los recursos publicados ni se presentó una respuesta de R3 como si correspondiera a R2; la aceptación de R2 sigue pendiente.

### R3 — Exfiltración del backup

Las pruebas se ejecutaron desde `cyberlab-attacker`, mediante `docker exec ... bash -c`, equivalente no interactivo a la consola de `make shell`. El host utilizó PowerShell y Git Bash para el verificador. Se comprobó el comando Compose contra el Makefile porque `make` no estaba disponible. Los comandos exactos y sus redirecciones se encuentran en [evidencia/comandos.txt](evidencia/comandos.txt).

1. **Descubrimiento de la interfaz.** `curl -sS -i --max-time 10 http://phantomcorp/` mostró un formulario GET con `action="/preview"` e `input name="url"`. La propia página indica que el servidor genera la previsualización. [Salida original](evidencia/salidas/01-home.txt).
2. **Contraste directo.** `curl -sS -i --max-time 3 http://phantomcorp-intra/` devolvió `curl: (6) Could not resolve host: phantomcorp-intra`. Esto acredita que el acceso por ese nombre falló desde el atacante; no demuestra por sí solo un timeout ni un bloqueo de conexiones por IP. La segmentación se conoce además por la topología y Compose oficiales. [Salida original](evidencia/salidas/02-directo.txt).
3. **Línea base de preview.** Se suministró `http://phantomcorp/` al formulario. La respuesta HTTP 200 incluyó la home dentro de la previsualización, sin visitar destinos externos. [Salida original](evidencia/salidas/03-preview-base.txt).
4. **Punto de partida interno.** Se consultó `http://phantomcorp-intra/` por preview; el nombre proviene del enunciado. La respuesta HTTP 200 incluyó la página «Intranet PhantomCorp» y el enlace literal `<a href="/backups/clientes.json">backup de clientes (temporal, borrar!)</a>`. Esta pista justifica la siguiente consulta; no se adivinó la ruta. [Salida original](evidencia/salidas/04-intranet.txt).
5. **Lectura del backup.** Se resolvió el enlace relativo respecto del host de intranet y se consultó mediante la misma función:

```bash
curl -sS -i --max-time 10 --get --data-urlencode url=http://phantomcorp-intra/backups/clientes.json http://phantomcorp/preview
```

La respuesta exterior fue `HTTP/1.0 200 OK` y `Content-Type: text/html; charset=utf-8`: preview envolvió el JSON con un encabezado HTML. No se atribuyen esas cabeceras al servicio interno. El contenido incluyó un aviso de backup temporal previo a migración, dos objetos en `clientes` con campos `id`, `empresa` y `cuit`, y `"integridad": "FLAG{ssrf_backup_clientes}"`. Los registros completos se conservan en la [salida original del backup](evidencia/salidas/05-backup.txt), sin duplicar innecesariamente sus identificadores aquí.

6. **Verificación.** Desde la raíz del repositorio, Git Bash ejecutó `./ctf submit extra R3 'FLAG{ssrf_backup_clientes}'`. El verificador respondió `[ OK ] Reto R3 resuelto: Exfiltrar datos sensibles a traves del SSRF`. [Salida original](evidencia/salidas/06-submit.txt).

El recorrido observado fue: home pública → formulario `/preview?url=...` → home de intranet → enlace publicado al backup → lectura del backup mediante preview. No fue necesario consultar `/salud`, otra ruta enlazada, para localizar ni verificar R3.

## 2. Evidencia de progreso

Estado real posterior al aporte P3 (no es el estado final grupal):

```text
·  R1     El server fetchea por vos: panel interno en localhost
·  R2     Descubrir la intranet en la red interna
✓  R3     Exfiltrar datos sensibles a traves del SSRF
1/3 (33%)
```

La [salida íntegra de ./ctf status extra](evidencia/salidas/07-status.txt) conserva el formato original. P5 deberá integrar el estado final cuando P1 y P2 presenten sus retos.

## 3. Preguntas de análisis

### P1 — Modelo de confianza por red

Pendiente de P1.

### P2 — Oráculo de escaneo

El transcript de los sondeos de localhost de R1 todavía no está en la entrega, así que no se atribuyen mensajes literales a puertos concretos. En la evidencia de P2 sí se observa el contraste de R2: desde la consola atacante, `curl` informa que no puede resolver `phantomcorp-intra`; al pedirle ese mismo destino a `/preview`, el servidor responde HTTP 200 con la página interna. Es un ejemplo de cómo el punto de observación del servidor permite conocer recursos que no están disponibles directamente desde el atacante.

Para R1, la comparación literal solicitada debe completarse con las salidas de P1. En general, un rechazo de conexión indica que no hay un servicio aceptando TCP en ese puerto, mientras que una respuesta HTTP demuestra que algo aceptó la conexión y habló HTTP. La aplicación SSRF puede revelar esa diferencia aunque el atacante no tenga conectividad directa, convirtiéndose en un oráculo de escaneo. La señal no es concluyente por sí sola: filtros, timeouts, protocolos distintos y errores de la aplicación pueden producir respuestas ambiguas.

### P3 — Hallazgo profesional

**Título:** exposición de un backup de clientes de intranet mediante SSRF en la previsualización pública.

**Activo afectado:** la confidencialidad del recurso `http://phantomcorp-intra/backups/clientes.json`. El punto de entrada es el parámetro `url` de `http://phantomcorp/preview`, en el portal PhantomCorp del laboratorio.

**Vector y condiciones:** un usuario con acceso HTTP al portal suministra una URL del host interno al formulario GET. En las solicitudes registradas no se enviaron credenciales ni cookies. La aplicación consulta el destino y devuelve su contenido. La conectividad del portal a ambas redes, definida en el entorno oficial, permite usarlo como intermediario hacia la intranet. La exposición combina la aceptación del destino interno por preview y la disponibilidad del backup para esa consulta.

**Evidencia reproducible:** la home pública revela la interfaz ([01](evidencia/salidas/01-home.txt)); el acceso directo por nombre falla ([02](evidencia/salidas/02-directo.txt)); preview devuelve la home interna con la ruta del backup ([04](evidencia/salidas/04-intranet.txt)); la consulta del enlace devuelve los datos y la flag R3 ([05](evidencia/salidas/05-backup.txt)); el verificador acepta la flag ([06](evidencia/salidas/06-submit.txt)). Los comandos se conservan en orden en el registro común.

**Impacto observado:** información de dos clientes ficticios —identificadores, razones sociales y CUIT— cruza desde un recurso interno hasta la respuesta recibida por el atacante. Se demuestra lectura no autenticada mediante el portal y pérdida de confidencialidad de ese backup. El campo llamado `integridad` contiene la flag didáctica; no demuestra alteración de datos ni una verificación criptográfica del backup. No se observaron contraseñas, tokens, acceso a una base de datos completa, escritura, shell, ejecución de código ni compromiso cloud.

**Prioridad propuesta:** alta para corregir la exposición, por la lectura de datos internos desde una función pública sin credenciales en las pruebas. Es una valoración cualitativa del escenario, no una puntuación CVSS calculada ni una afirmación de compromiso total. El alcance observado se limita a dos registros de laboratorio.

**Recomendaciones:** restringir los destinos de preview a los necesarios para su función y aplicar una política de egreso que impida acceder a la intranet desde el componente que realiza las consultas. Validar el destino efectivo al resolver y conectar, y también ante redirecciones; el bloqueo literal de `localhost` no aborda el host usado aquí. Retirar backups del servicio HTTP y exigir autorización en los recursos internos como control independiente. En producción, revisar registros de acceso para determinar el alcance de lecturas previas; no se realizó esa investigación en este laboratorio.

**Criterio de corrección:** repetir la petición de la evidencia 05 debe resultar en rechazo del destino por preview, sin devolver datos internos, mientras que una URL legítima autorizada conserva su comportamiento. No se modificó el target para probar estas defensas, porque los enunciados y el entorno son de solo lectura para las entregas.

### P4 — Mitigaciones

Respuesta completa pendiente de P4. **Revisión de P3 de la propuesta del plan:** restringir destinos por diseño y por red sí aborda el recorrido observado, siempre que el proceso que hace preview no pueda alcanzar `phantomcorp-intra`. La evidencia 05 proporciona una prueba concreta de regresión. Bloquear únicamente `localhost` o `127.0.0.1` no impediría esta cadena, cuyo destino usa el nombre de intranet. Si el portal necesita conectividad interna para otras funciones, conviene separar el componente de previsualización y restringir su egreso. Una allowlist debe verificar el destino efectivo, no solamente una cadena de hostname. Esta revisión evalúa la propuesta escrita del plan; no una implementación ni un aporte terminado de P4, inexistente en esta rama al comenzar.

### P5 — Metadata service

Pendiente de P5.

## 4. Conclusión

Pendiente de integración por P5. Aporte comprobado para el resumen ejecutivo: la previsualización pública permitió recuperar un backup interno con dos registros ficticios de clientes. Priorizar la restricción del destino y egreso de preview y retirar/proteger los backups internos. El resultado demuestra exposición de datos, no control de toda la red.
