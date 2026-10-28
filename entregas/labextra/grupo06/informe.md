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

**Finalidad y partes asistidas:** apoyo para la ejecución de R1 y R3, el ordenamiento de evidencias y la redacción técnica inicial.
**Verificación realizada:** Se ejecutaron los comandos en el entorno autorizado del laboratorio y se analizaron las respuestas obtenidas para comprobar que el acceso al recurso interno se realizó mediante la vulnerabilidad SSRF. Se verificó la presencia de la información expuesta y se validó la flag mediante el sistema oficial de retos.

**Herramienta:** ChatGPT (OpenAI), aporte de la Persona 5.

- **Finalidad del uso:** asistencia para comprender los riesgos de SSRF en entornos cloud, redactar la pregunta P5 y revisar la integración de la entrega grupal.
- **Partes asistidas:** respuesta P5 sobre servicios de metadatos y revisión preliminar del informe.
- **Verificación:** se contrastó la respuesta con el alcance del laboratorio, diferenciando los accesos internos efectivamente observados de los riesgos teóricos de SSRF en servicios cloud. No se realizaron consultas contra servicios de metadatos reales.

## 1. Cadena de explotación

### R1 — Panel interno en localhost

La home pública de `http://phantomcorp/` expuso una herramienta con formulario GET hacia `/preview` e input `url`; el texto de la propia página aclara que la previsualización la genera el servidor. Esto justificó comprobar que el destino indicado se consulta desde PhantomCorp y no desde la consola atacante. La home y el formulario constan en la [salida original](evidencia/salidas/01-home.txt).

Se probaron por `/preview` destinos `127.0.0.1` limitados a una lista breve de puertos HTTP y de administración habituales. El contraste inicial contra el puerto 1 devolvió `HTTP/1.0 502 Bad Gateway` y `Connection refused`, por lo que la aplicación reveló que intentó abrir una conexión local pero no obtuvo listener. La [salida original](evidencia/salidas/08-r1-oraculo-puertos.txt) conserva ese caso. Los puertos 8080, 8000, 3000, 5000, 8888, 8008, 8081 y 9090 presentaron el mismo resultado; el registro de comandos detalla la secuencia completa.

El puerto 9000 produjo una respuesta diferente: el portal devolvió `HTTP/1.0 200 OK` y envolvió el contenido de «PhantomCorp — Panel interno (solo localhost)», que incluía la flag. La consulta reproducible fue:

```bash
curl -sS -i --max-time 10 --get --data-urlencode 'url=http://127.0.0.1:9000/' http://phantomcorp/preview
```

La respuesta completa está en la [evidencia del panel local](evidencia/salidas/09-r1-panel-local.txt). Desde la raíz del repositorio se presentó `FLAG{ssrf_localhost_panel_interno}` mediante `./ctf submit extra R1 'FLAG{ssrf_localhost_panel_interno}'`; el verificador la aceptó, como acredita la [salida de presentación](evidencia/salidas/10-r1-submit.txt).

### R2 — Intranet en la red interna

Pendiente del responsable P2. Para obtener el punto de partida de R3 se consultó la home de la intranet mediante preview y se conservó el contraste de acceso directo. No se presentó la flag R2 ni se reemplaza el análisis asignado a P2.

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

Estado real posterior a la presentación de R1 y R3 (no es el estado final grupal):

```text
✓  R1     El server fetchea por vos: panel interno en localhost
·  R2     Descubrir la intranet en la red interna
✓  R3     Exfiltrar datos sensibles a traves del SSRF
2/3 (66%)
```

La [salida íntegra de ./ctf status extra](evidencia/salidas/13-status-r1-r3.txt) conserva el formato original. Al integrar la entrega se debe volver a ejecutar el verificador y reemplazar este bloque por el estado final con los tres retos aceptados.

## 3. Preguntas de análisis

### Acceso indirecto y modelo de confianza por red

La topología del laboratorio separa la consola atacante y la intranet: el atacante solo pertenece a `labnet`, mientras que `phantomcorp-intra` solo pertenece a `internalnet`. El portal `phantomcorp` está conectado a ambas redes. Por eso, una petición directa desde la consola hacia la intranet no dispone de una ruta o resolución utilizable, pero la misma petición introducida en `/preview` puede ser emitida por el portal, que sí tiene conectividad hacia la red interna.

```text
Consola atacante --labnet--> phantomcorp (/preview) --internalnet--> phantomcorp-intra
        |                         |
        |                         +-- localhost:9000 (panel interno)
        +---- sin acceso directo a la intranet ----X
```

El componente que vuelve alcanzable indirectamente a la intranet es el servidor web `phantomcorp`, en particular su función `/preview`: acepta una URL elegida por quien consulta, realiza el request con la identidad y conectividad del servidor, y devuelve el contenido. R1 también demuestra la misma pérdida de la confianza basada solo en ubicación: `127.0.0.1` significa el propio portal para la solicitud generada por el servidor, no la consola atacante. La segmentación limita el acceso directo, pero no protege por sí sola cuando un host conectado a ambas redes puede ser inducido a solicitar destinos arbitrarios.

### P2 — Oráculo de escaneo

Pendiente de P2.

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

El servicio de metadatos (*metadata service*) es un mecanismo que utilizan las plataformas de computación en la nube para proporcionar información a las máquinas virtuales sobre su entorno de ejecución. En algunas plataformas, estos servicios también permiten obtener credenciales temporales asociadas a los permisos de la instancia.

Una dirección conocida es `169.254.169.254`, utilizada por servicios de metadatos como el de Amazon EC2. Se trata de una dirección especial accesible desde determinados entornos de nube, no de un servidor público convencional.

El problema aparece cuando una aplicación tiene una vulnerabilidad SSRF, como la que analizamos en PhantomCorp. Si el servidor acepta una URL proporcionada por un usuario y realiza la consulta sin validar correctamente el destino, un atacante podría intentar utilizar esa funcionalidad para acceder al servicio de metadatos desde el propio servidor.

En un entorno cloud mal protegido, esto podría exponer información de configuración o credenciales temporales. Si esas credenciales tienen permisos importantes, el impacto puede extenderse a otros recursos de la nube, según los permisos asignados. Por eso, las consecuencias pueden ser mayores que la simple lectura de una página interna.

Para reducir este riesgo es necesario restringir los destinos que puede consultar la aplicación, bloquear accesos innecesarios a direcciones internas y servicios de metadatos, aplicar permisos mínimos y utilizar mecanismos de protección específicos de cada plataforma, como IMDSv2 en AWS.

En nuestro laboratorio comprobamos que `/preview` permitía consultar recursos internos mediante SSRF, incluyendo un panel local y un backup de clientes. Sin embargo, no intentamos acceder a un servicio de metadatos real ni obtuvimos credenciales cloud.

Como conclusión, entendimos que una vulnerabilidad SSRF puede ser especialmente peligrosa en la nube porque el servidor podría tener acceso a recursos y permisos que el usuario externo no posee. El impacto depende de la configuración, las protecciones implementadas y los privilegios disponibles.

## 4. Conclusión

Pendiente de integración por P5. Aporte comprobado para el resumen ejecutivo: la previsualización pública permitió recuperar un backup interno con dos registros ficticios de clientes. Priorizar la restricción del destino y egreso de preview y retirar/proteger los backups internos. El resultado demuestra exposición de datos, no control de toda la red.
