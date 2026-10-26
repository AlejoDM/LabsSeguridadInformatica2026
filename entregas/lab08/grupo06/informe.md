# Informe — Laboratorio 08 · Post-explotación y automatización

**Grupo:** 06 ·
**Integrantes:**
| Nombre y apellido | Legajo | Usuario de GitHub |
|---|---:|---|
| Martín Beccereca | 15154 | @martinbeccereca |
| María Belén Benito | 14625 | @belubenito603 |
| Alejo De Miguel | 15138 | @AlejoDM |
| Tomás Giudici | 14977 | @TomasGiudici |
| Carolina Suppo | 15057 | @carosuppo |
**Fecha:** 23/10/2026

## 0. Declaración de uso de IA

Se utilizó Codex (OpenAI) para asistir en la organización de la evidencia, la redacción inicial de la fila de Loot, la respuesta P2 y el mini-research. Las credenciales y flags consignadas se verificaron mediante comandos ejecutados por el equipo dentro del entorno autorizado del Lab 08; las fuentes del research fueron leídas y contrastadas antes de incorporarlas. El grupo debe revisar este texto, completar los datos de integrantes y declarar cualquier otra herramienta utilizada.

**Herramienta:** Claude Code.

- **Finalidad del uso:** apoyo para ejecutar el reconocimiento de R1 contra el host víctima (`/opt`) y la consolidación de `comandos.txt`.
- **Partes asistidas:** fila "R1 — Recon" en la tabla de flags, fila "Recon (R1)" y su análisis en la tabla de post-explotación y sección de comandos de R1 en `evidencia/comandos.txt`.
- **Verificación:** los comandos se ejecutaron como `operador` y la salida se guardó cruda y sin editar en `evidencia/salidas/`. Se revisó el contenido antes de incorporarlo.

**Herramienta:** ChatGPT (OpenAI).

- **Finalidad del uso:** asistencia en la implementación y prueba del script de automatización del Reto 5, interpretación de respuestas HTTP y redacción de la documentación.
- **Partes asistidas:** función `buscar_flag()` de `src/recolector.py`, sección 3 de Automatización, respuesta P4 y registro de comandos de R5.
- **Verificación:** el programa se ejecutó como `operador` dentro del contenedor víctima y se comprobó su funcionamiento contra `phantomcorp-db`. Se verificó el hallazgo en el legajo 187, el comportamiento con rangos sin resultados y la aceptación de la flag mediante una copia temporal del validador.

## 1. Flags capturadas

| Reto      | Estado   | Evidencia                                               |
| --------- | -------- | ------------------------------------------------------- |
| R1 — Recon | Obtenida | [Salida cruda de R1](evidencia/salidas/r1-recon-opt.txt) y [envío de R1](evidencia/salidas/r1-submit.txt) |
| R2 — Loot | Obtenida | [Salida cruda de R2](evidencia/salidas/r2-loot-env.txt) |
| R3 — Escalada de privilegios (SUID) | Obtenida | [Elevación a root](evidencia/salidas/r3-privesc-identidad.txt) y [lectura de la flag](evidencia/salidas/r3-privesc-flag.txt). Flag `FLAG{privesc_suid_root}`, aceptada mediante `./ctf submit 08 R3`. |

La captura final de `./ctf status 08` queda pendiente de integrar cuando el grupo presente los cinco retos.

## 2. Informe de post-explotación

| Fase      | Qué hicimos                                                                                                                                                                                            | Comando/técnica                                                                                                                | Evidencia                                                                                                                         | Defensa                                                                                                                                                                                                                                 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Recon (R1) | Como `operador`, recién caído en el host, enumeramos `/opt` buscando información de despliegue que no debería estar ahí. Encontramos un subdirectorio con una nota de deploy legible por el usuario limitado. | `ls -la /opt`, `ls -la /opt/phantom-deploy` y `cat /opt/phantom-deploy/DEPLOY_NOTES.txt`, ejecutados desde el host víctima mediante `make shell-victima` (en esta sesión, `docker exec -u operador`). | [Salida R1](evidencia/salidas/r1-recon-opt.txt): confirma la identidad `operador`, el hostname `phantomcorp` y el contenido de `DEPLOY_NOTES.txt` con el `deploy_token` que incluye la flag. | Retirar notas y archivos de despliegue de rutas accesibles a cuentas de aplicación; aplicar permisos mínimos sobre `/opt`, inventariar qué queda en el filesystem tras un deploy y revisar ese inventario antes de pasar a producción. |
| Loot (R2) | Como el usuario limitado `operador`, leímos el archivo de configuración de la aplicación. El archivo reveló el host de BD, el usuario de aplicación, una contraseña y el secreto que contiene la flag. | `cat /var/www/.env` ejecutado desde el host víctima mediante `make shell-victima` (en esta sesión, `docker exec -u operador`). | [Salida R2](evidencia/salidas/r2-loot-env.txt): confirma la identidad `operador`, la existencia de `/var/www/.env` y sus valores. | Retirar secretos de archivos legibles por usuarios no autorizados; usar un gestor de secretos, identidad de workload/credenciales de corta vida, permisos mínimos, auditoría, rotación y revocación inmediata de los valores expuestos. |
| Privesc (R3) | Desde la cuenta limitada `operador`, identificamos un ejecutable no estándar con permisos SUID perteneciente a `root`. Comprobamos que permitía ejecutar comandos conservando privilegios efectivos de administrador y leer el archivo protegido indicado por la consigna. | `find / -type f -perm -4000 2>/dev/null` permitió localizar `/usr/local/bin/system-check`. Comprobamos sus permisos con `ls -l` y verificamos mediante SHA-256 que era una copia de Bash. Luego ejecutamos `/usr/local/bin/system-check -p -c 'id'` y `/usr/local/bin/system-check -p -c 'cat /root/flag.txt'`. | [Enumeración SUID](evidencia/salidas/r3-suid-enumeracion.txt), [identidad inicial](evidencia/salidas/r3-identidad.txt), [privilegios efectivos](evidencia/salidas/r3-privesc-identidad.txt) y [lectura del archivo protegido](evidencia/salidas/r3-privesc-flag.txt). Se observó `euid=0(root)` y se obtuvo la flag `FLAG{privesc_suid_root}`. No se comprobó persistencia ni acceso a otros sistemas. | Eliminar el permiso SUID de intérpretes y ejecutables que no lo necesiten, evitar utilizar herramientas de propósito general con privilegios de `root`, revisar periódicamente los archivos SUID/SGID y aplicar el principio de mínimo privilegio. |

### Observación, inferencia y límite — R1

**Observación.** El proceso se ejecutó como `uid=1000(operador)` en el host `phantomcorp`. Dentro de `/opt` existe un único subdirectorio, `phantom-deploy`, propiedad de `root:root`, que contiene un archivo `DEPLOY_NOTES.txt` legible por `operador`. Su contenido es `PhantomCorp - notas de despliegue (NO borrar)` seguido de `deploy_token=FLAG{post_situational_awareness}`.

**Inferencia.** Una nota de despliegue dejada en un directorio legible por una cuenta de aplicación de bajo privilegio indica que el proceso de deploy no limpió artefactos operacionales del sistema en producción. El nombre del campo (`deploy_token`) sugiere que, en un escenario real, ese valor podría usarse para autenticar o identificar un despliegue ante algún sistema externo, aunque este paquete no permite comprobar contra qué servicio se validaría.

**No verificado.** Esta evidencia no demuestra que el `deploy_token` esté vigente, que habilite por sí solo alguna acción privilegiada, ni que existan otros archivos sensibles fuera de `/opt` accesibles a `operador`. Encontrar información operacional no equivale a tener privilegios elevados; eso se evalúa recién en R3.

### Observación, inferencia y límite — R2

**Observación.** El proceso se ejecutó como `uid=1000(operador)`. `/var/www/.env` era un archivo de propiedad `root:root`, con permisos `0644`, y su contenido resultó legible para ese usuario. Incluía `DB_HOST=phantomcorp-db`, `DB_USER=phantom_app`, `DB_PASS=…` y `APP_SECRET=FLAG{loot_credentials_found}`.

**Inferencia.** Una cuenta local de bajo privilegio que pueda leer este archivo puede obtener credenciales de la aplicación y secretos que deberían estar restringidos. Si la contraseña sigue vigente y el usuario conserva permisos de conexión, esto reduce el costo de acceder al servicio interno de base de datos.

**No verificado.** Esta evidencia no demuestra por sí sola qué permisos tiene `phantom_app` dentro de la base, que la contraseña se reutilice en otros sistemas, ni que puedan modificarse datos. Esos aspectos requieren pruebas adicionales y permanecen fuera de R2.

## 3. Automatización

Para el Reto 5 desarrollamos un script en Python que automatiza la consulta de legajos de empleados a través del endpoint `/empleado?id=N`, perteneciente al servidor interno `phantomcorp-db`.

Partimos del archivo proporcionado por la cátedra, conservando la función `consultar_legajo()` y completando la función `buscar_flag()`. Esta última recorre los identificadores dentro del rango indicado, consulta cada legajo y analiza la respuesta JSON para detectar el campo especial `legajo_oculto`, que contiene la flag.

El programa utiliza únicamente bibliotecas estándar de Python. Además, contempla respuestas fallidas, como los errores HTTP 404, y se detiene inmediatamente cuando encuentra el registro buscado, evitando realizar consultas innecesarias.

**Ejecución:** El script se ejecutó desde el contenedor víctima `phantomcorp`, utilizando el usuario limitado `operador`, ya que el servidor `phantomcorp-db` solo es accesible desde la red interna del laboratorio.

**Resultado obtenido:** Al recorrer los legajos del 1 al 250, el programa identificó el legajo **187**, correspondiente a `cuenta-servicio`, y recuperó la flag `FLAG{automation_pays_off}`. Posteriormente, la flag fue aceptada por el validador del laboratorio.

También realizamos pruebas con el rango del 1 al 5 y con el identificador 251. En ambos casos, el programa finalizó correctamente informando que no encontró la flag, sin producir errores de ejecución.

**Evidencias:** [Código del recolector](src/recolector.py) y [salida de la ejecución](evidencia/salidas/r5-recolector.txt).

**Alcance:** Las consultas se limitaron al servicio interno del entorno autorizado. El script no modifica datos ni realiza solicitudes fuera del rango requerido para la prueba principal.

## 4. Preguntas de análisis

### P1 — ¿Por qué un binario SUID es peligroso? ¿Qué hace el flag `-p`?

El bit SUID (`set-user-ID`) hace que, al ejecutar el binario, el proceso corra con los permisos del **dueño del archivo**, no con los del usuario que lo invocó. Esto existe para casos legítimos y acotados: por ejemplo, `passwd` necesita escribir en `/etc/shadow`, que un usuario común no puede tocar directamente, así que `passwd` es SUID de `root` para esa única operación controlada. El problema aparece cuando el binario con SUID es una herramienta de propósito general (un intérprete, un editor, una utilidad de archivos, etc.) que además permite ejecutar comandos arbitrarios o leer/escribir rutas arbitrarias. Si ese binario pertenece a `root` y tiene SUID activo, cualquier usuario que pueda invocarlo hereda, para esa invocación, los privilegios de `root` — y si la herramienta permite lanzar un shell o leer cualquier archivo, el usuario limitado termina con acceso de administrador. GTFOBins documenta, para decenas de binarios comunes, la invocación exacta que logra ese efecto.

El flag `-p` aparece en varias de esas invocaciones (por ejemplo en intérpretes o editores que de otro modo *bajarían* sus propios privilegios al detectar que corren con un UID efectivo distinto del real, como medida de seguridad del propio binario). `-p` le indica al programa que **preserve** los privilegios efectivos en vez de resignarlos automáticamente; sin esa opción, el binario podría "notar" que fue invocado vía SUID y renunciar por su cuenta a los privilegios elevados antes de ejecutar nada, frustrando el intento de escalada. Con `-p`, el proceso que arranca —por ejemplo un shell— conserva el UID efectivo de `root` en lugar de caer al UID real del usuario que lo invocó.

Esta respuesta describe el mecanismo general de SUID y de `-p`. La identificación del binario SUID no estándar presente en PhantomCorp, la invocación concreta usada contra él y la evidencia de la escalada lograda corresponden a R3 y quedan a cargo de ese responsable; esta sección no reemplaza esa evidencia.

### P2 — ¿Por qué el atacante no alcanzaba `phantomcorp-db` y sí pudo hacerlo desde la víctima?

El atacante inicial opera desde la red `labnet`, donde solo está expuesto el host `phantomcorp`. La base `phantomcorp-db` pertenece a una red interna separada y no es alcanzable desde esa consola externa. En cambio, el host víctima participa también en la red interna; por eso, una vez obtenido acceso como `operador`, pudo resolver y consultar `http://phantomcorp-db/`. La salida de apoyo de [pivoting](evidencia/salidas/p2-pivot-apoyo.txt) identifica al servicio como una base interna con acceso restringido a la LAN.

Esto ilustra un pivote: el host comprometido funciona como punto de apoyo desde una zona visible por el atacante hacia una red que no estaba expuesta directamente. No se creó un túnel ni se desplegó un proxy en esta práctica; se demostró únicamente que la posición de red de la víctima permite la conexión. La mitigación no es solo ocultar el nombre del host: requiere segmentación con reglas de salida mínimas, autenticación y autorización del servicio de base de datos, credenciales de mínimo privilegio y monitoreo de conexiones este-oeste inusuales.

### P3 — ¿Cómo evitar que los secretos queden expuestos en archivos `.env` e historiales de comandos?

La exposición de credenciales y secretos en archivos de configuración o historiales de comandos representa un riesgo importante, ya que un usuario con acceso limitado al sistema podría obtener información que le permita acceder a otros servicios.

Para prevenirlo, una medida fundamental es utilizar un gestor de secretos, evitando almacenar contraseñas y tokens directamente en archivos `.env`. Cuando estos archivos sean necesarios, deben tener permisos restrictivos y ser accesibles únicamente para los usuarios o procesos autorizados. También se deben excluir del control de versiones y revisar que no contengan credenciales innecesarias.

En cuanto al historial de comandos, se debe evitar introducir contraseñas o tokens directamente en la terminal, especialmente como argumentos que puedan quedar registrados. Es preferible utilizar mecanismos seguros de autenticación y suministro de credenciales que no las expongan en el historial.

Finalmente, si una credencial queda expuesta, debe revocarse o rotarse. Estas medidas, junto con el principio de mínimo privilegio, reducen tanto la posibilidad de obtener secretos como el impacto de una eventual filtración.

En PhantomCorp, el hallazgo de R2 demuestra la importancia de proteger los archivos de configuración, ya que `/var/www/.env` era legible por el usuario `operador`. Sin embargo, esa observación no demuestra que las credenciales hayan sido utilizadas para comprometer otros sistemas.

### P4 — ¿Qué decisiones humanas no toma el script y debería evaluar un agente?

El script desarrollado para el Reto 5 automatiza una tarea repetitiva: consultar legajos, analizar las respuestas y detenerse cuando encuentra una flag. Sin embargo, no toma decisiones sobre el contexto, la autorización ni las consecuencias de las acciones que realiza.

Por ejemplo, una persona debe definir previamente qué sistema está autorizado a consultar, qué rango de identificadores corresponde utilizar y cuál es el objetivo de la búsqueda. El script solamente ejecuta esas instrucciones; no puede determinar por sí mismo si una consulta está permitida o si sus resultados deberían utilizarse para realizar otras acciones.

Un agente podría incorporar decisiones adicionales, como interpretar respuestas inesperadas, adaptar el procedimiento ante errores o seleccionar entre distintas herramientas. Sin embargo, esas capacidades también requieren límites y supervisión humana, especialmente cuando podrían implicar acceder a información sensible o ampliar el alcance de una prueba.

En nuestro laboratorio, el programa se limitó a recorrer los legajos del 1 al 250, identificar el registro que contenía la flag y detenerse inmediatamente. Esto demuestra cómo la automatización permite ahorrar tiempo en tareas repetitivas, pero **no reemplaza el criterio humano para definir objetivos, permisos y límites de seguridad**.

## 5. Bitácora de P2

Ver [comandos de P2](evidencia/comandos.txt). Todos se ejecutaron exclusivamente en los contenedores autorizados del Lab 08.
