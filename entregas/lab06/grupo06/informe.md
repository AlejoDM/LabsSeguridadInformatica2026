# Informe — Laboratorio 06 · Enumeración

**Grupo:** 06
**Integrantes:**

| Nombre y apellido    | Usuario de GitHub |
| -------------------- | ----------------- |
| Martín Beccereca     | martinbeccereca   |
| Belén Benito         | belubenito603     |
| Alejo José De Miguel | AlejoDM           |
| Tomás Giudici        | TomasGiudici      |
| Carolina Suppo       | carosuppo         |

**Fecha:** 21/10/2026

## 0. Declaración de uso de IA

**Herramienta:** Codex.

- **Finalidad del uso:** apoyo para interpretar la consigna, planificar el reparto de tareas y elaborar el borrador inicial de este informe.
- **Partes asistidas:** planificación del Lab 06; bitácora y organización de sus evidencias.
- **Verificación:** la enumeración y la confirmación se ejecutaron contra el contenedor `phantomcorp` provisto por la cátedra. Las salidas originales de `dirb`, `curl`, el envío de la flag y el estado del motor se conservaron en `evidencias/`. El grupo debe revisar y poder explicar todo el contenido antes de entregar.

**Herramienta:** ChatGPT.

- **Finalidad del uso:** apoyo en la ejecución guiada de pruebas, interpretación de resultados, resolución de problemas técnicos y redacción de la documentación.
- **Partes asistidas:** fila R3 y R4 del inventario, respuestas P3 y P4, organización de la bitácora y validación del reto R4.
- **Verificación:** los comandos de R4 fueron ejecutados contra el contenedor autorizado `phantomcorp`. Se comprobó la respuesta HTTP, se conservaron las evidencias originales y se verificó la aceptación de la flag mediante una copia temporal del validador compatible con Linux.

**Herramienta:** Claude Code.

- **Finalidad del uso:** apoyo para ejecutar la enumeración de R2 contra `phantomcorp` y para redactar la fila correspondiente del inventario, la sección de evidencia, P2 y la bitácora.
- **Partes asistidas:** sección "Evidencia del R2" y comandos de R2 en la bitácora.
- **Verificación:** las peticiones HTTP se ejecutaron contra el contenedor `phantomcorp` desde la consola atacante; las salidas crudas se conservaron sin editar en `evidencias/`. Se revisó el contenido antes de incorporarlo.

## 1. Flags capturadas

| Reto                                 | Estado    | Evidencia                                                                                                |
| ------------------------------------ | --------- | -------------------------------------------------------------------------------------------------------- |
| R1 — Enumeración de directorios      | Resuelto  | [Envío de R1](evidencias/lab06-r1-submit.txt) y [estado posterior](evidencias/lab06-status-after-r1.txt) |
| R2 — Repositorio Git expuesto        | Resuelto  | [config filtrado](evidencias/lab06-r2-git-config.txt) y [envío de R2](evidencias/lab06-r2-submit.txt)    |
| R3 — Métodos HTTP peligrosos         | Resuelto  | [OPTIONS](evidencias/lab06-r3-options.txt) y [Nmap HTTP](evidencias/lab06-r3-nmap-http.txt)              |
| R4 — Enumeración de usuarios vía API | Resuelto | [Respuesta de la API](evidencias/lab06-r4-api-users.txt) y [estado del R4](evidencias/lab06-r4-status.txt) |
| R5 — Fingerprinting de tecnología    | Pendiente | —                                                                                                        |

La salida de estado posterior al R1 registra 1 de 5 retos resueltos. El archivo [progreso-06.done](evidencias/progreso-06.done) es una copia del estado local del motor y complementa, pero no reemplaza, la salida legible de `./ctf status 06`.

## 2. Inventario de enumeración

| Hallazgo                                            | Ruta/Método                | Técnica                                                                                                                                                          | Evidencia                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Riesgo                                                                                                                                                                                                                                                                                                                                                                                                                                          | ¿Qué habilita para el Lab 07?                                                                                                                                                                                                                                                                |
| --------------------------------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Directorio de respaldos accesible sin autenticación | `/backup`                  | Enumeración de directorios con `dirb`; confirmación manual con `curl`                                                                                            | `dirb` reportó `/backup` con `200`; la respuesta HTTP lista `respaldo-db-2024.sql.gz` y `config.old`. Ver [salida de dirb](evidencias/lab06-r1-dirb.txt) y [confirmación de `/backup`](evidencias/lab06-r1-backup.txt).                                                                                                                                                                                                                                                                            | Un tercero con acceso al servicio puede consultar el índice observado. Los nombres de archivos son indicios de datos y configuraciones potencialmente sensibles; no se descargó ni verificó el contenido de esos archivos.                                                                                                                                                                                                                      | Orienta el análisis posterior hacia respaldos y configuraciones expuestos. Si alguno fuera accesible y contuviera datos o credenciales, podría habilitar nuevas hipótesis de explotación; esa condición no fue verificada en R1.                                                             |
| Método HTTP `PUT` habilitado                        | `OPTIONS /` — método `PUT` | Enumeración de métodos HTTP con `curl`; corroboración con scripts NSE de Nmap                                                                                    | La respuesta a `OPTIONS` indicó que `PUT` está habilitado y la enumeración con Nmap corroboró el hallazgo. Ver [respuesta OPTIONS](evidencias/lab06-r3-options.txt) y [enumeración con Nmap](evidencias/lab06-r3-nmap-http.txt).                                                                                                                                                                                                                                                                   | La habilitación de `PUT` amplía la superficie de ataque porque puede permitir enviar contenido a recursos del servidor. En este lab no se comprobó que permita escritura arbitraria ni ejecución de archivos.                                                                                                                                                                                                                                   | Orienta el Lab 07 a verificar de forma controlada si `PUT` permite crear o reemplazar recursos y, solo si se cumplen las condiciones necesarias, evaluar una posible carga de archivos.                                                                                                      |
| Repositorio Git expuesto por HTTP                   | `/.git/config`             | Petición directa con `curl -i` al archivo de configuración del repositorio; verificación de otras rutas del `.git` (`HEAD`, `logs/HEAD`, listado del directorio) | `curl -sS -i http://phantomcorp/.git/config` devolvió `200` con el contenido del archivo, que incluye la URL del remoto `origin` (`https://git.internal.phantomcorp/intranet.git`). Las mismas pruebas contra `/.git/HEAD`, `/.git/logs/HEAD` y `/.git/` devolvieron `404`. Ver [config filtrado](evidencias/lab06-r2-git-config.txt), [HEAD](evidencias/lab06-r2-git-head.txt), [logs/HEAD](evidencias/lab06-r2-git-logs-head.txt) y [listado del directorio](evidencias/lab06-r2-git-index.txt). | Un `.git/config` accesible confirma que el servidor sirve archivos internos del control de versiones y filtra la URL del repositorio origen, información útil para orientar un ataque dirigido a esa infraestructura. En este caso puntual no se pudo acceder a `HEAD`, a los logs ni al listado del directorio, por lo que no está verificado que el repositorio completo (historia, objetos) sea descargable; solo el archivo `config` lo es. | Orienta el Lab 07 a intentar, de forma controlada, reconstruir el repositorio accesible (por ejemplo con herramientas de volcado de `.git` vía HTTP) solo si se confirma que más rutas del `.git` están expuestas, y a investigar el remoto `origin` filtrado como posible vector adicional. |
| Exposición de usuarios y roles mediante API interna | `GET /api/users` | Consulta HTTP con `curl -i` | El servidor respondió `200 OK` y devolvió tres usuarios: `admin` (`superuser`), `jperez` (`editor`) y `mgomez` (`viewer`). Ver [evidencia R4](evidencias/lab06-r4-api-users.txt). | La exposición de usuarios y roles sin autenticación facilita la identificación de cuentas privilegiadas y posibles ataques dirigidos. No se comprobó acceso a las cuentas. | Permite orientar el Lab 07 hacia la revisión de la autenticación, autorización y protección de cuentas privilegiadas. |

### Evidencia del R1

Extracto de la enumeración:

```text
+ http://phantomcorp/admin (CODE:403|SIZE:65)
+ http://phantomcorp/backup (CODE:200|SIZE:249)
```

La respuesta `403` de `/admin` indica que la ruta existe, pero no demuestra que su contenido sea accesible. La respuesta `200` de `/backup` permitió confirmar un directorio accesible y observar su listado. Las salidas completas se conservan en los enlaces de la tabla.

### Evidencia del R3

Para identificar los métodos HTTP habilitados se realizó una petición `OPTIONS` contra el servidor y se corroboró el resultado mediante scripts HTTP de Nmap.

Las salidas completas se conservan en [respuesta OPTIONS](evidencias/lab06-r3-options.txt) y [enumeración HTTP con Nmap](evidencias/lab06-r3-nmap-http.txt).

La evidencia permite afirmar que el método `PUT` está habilitado. No se realizaron cargas mediante este método, por lo que no se verificó si permite crear archivos arbitrarios ni si esos archivos podrían ser ejecutados por el servidor.

### Evidencia del R2

Para comprobar la exposición del repositorio se solicitó directamente el archivo de configuración del control de versiones:

```text
curl -sS -i http://phantomcorp/.git/config
HTTP/1.0 200 OK
...
[remote "origin"]
	url = https://git.internal.phantomcorp/intranet.git
```

El servidor respondió `200` y devolvió el contenido del archivo, incluida la URL del remoto `origin`. Para acotar el alcance de la exposición se probaron además otras rutas típicas de un `.git` servido por HTTP: `/.git/HEAD`, `/.git/logs/HEAD` y el listado del directorio `/.git/`. Las tres devolvieron `404`, lo que indica que, en este caso, no todo el repositorio quedó accesible por esta vía, solo el archivo `config`. Las salidas completas se conservan en [config filtrado](evidencias/lab06-r2-git-config.txt), [HEAD](evidencias/lab06-r2-git-head.txt), [logs/HEAD](evidencias/lab06-r2-git-logs-head.txt) y [listado del directorio](evidencias/lab06-r2-git-index.txt).

No se intentó reconstruir el repositorio con herramientas de volcado (por ejemplo `git-dumper`), porque las rutas necesarias para eso no estaban disponibles; esa validación queda fuera del alcance de este hallazgo y se señala como pendiente.

### Evidencia del R4

Para enumerar los usuarios expuestos por la API interna de PhantomCorp realizamos una petición HTTP al endpoint `/api/users` utilizando `curl -i`.

El servidor respondió con el código `200 OK` y devolvió un JSON que contiene tres usuarios con sus respectivos roles: `admin` (`superuser`), `jperez` (`editor`) y `mgomez` (`viewer`). Además, la respuesta incluye una nota que identifica al recurso como un endpoint interno de Recursos Humanos que no debería estar expuesto.

La consulta se realizó sin proporcionar credenciales, lo que permitió comprobar que la información se encontraba accesible desde la consola atacante del laboratorio.

La salida HTTP completa se conserva en [lab06-r4-api-users.txt](evidencias/lab06-r4-api-users.txt), mientras que la validación del reto se documenta en [lab06-r4-status.txt](evidencias/lab06-r4-status.txt).

No se intentó iniciar sesión con los usuarios encontrados ni acceder a funcionalidades restringidas. Por lo tanto, el hallazgo demuestra exposición de información, pero no una vulneración de las cuentas.

## 3. Preguntas de análisis

### P1 — Enumeración vs. recon

En el Lab 05 realizamos reconocimiento para construir un mapa amplio de la superficie de PhantomCorp. Con `nmap -Pn -sV -p- phantomcorp` identificamos cuatro servicios expuestos: FTP en 21, HTTP en 80, HTTP/API en 8080 y un servicio no identificado en 31337. También usamos headers HTTP y `robots.txt` para reunir indicios iniciales sobre el servicio web. El resultado fue conocer qué servicios estaban disponibles y cuáles requerían análisis posterior.

En el Lab 06 realizamos enumeración sobre el servicio web identificado. Ejecutamos `dirb http://phantomcorp/`, que encontró `/admin` con código `403` y `/backup` con código `200`. Luego confirmamos este último recurso con `curl -sS -i http://phantomcorp/backup`; la respuesta mostró un listado que incluye `respaldo-db-2024.sql.gz` y `config.old`. Estas observaciones están respaldadas por las salidas de R1 enlazadas en el inventario.

Por lo tanto, el reconocimiento respondió qué servicios existían y dónde estaban; la enumeración profundizó dentro de uno de esos servicios para identificar recursos no enlazados, su nivel de acceso y sus consecuencias potenciales. El Lab 05 produjo el mapa inicial y el Lab 06 comienza a construir el inventario detallado que orientará hipótesis para el Lab 07.

### P2 — El `.git` expuesto

El servidor web respondió `200` a una petición directa de `http://phantomcorp/.git/config` y devolvió el contenido del archivo, que incluye la URL del remoto `origin` (`https://git.internal.phantomcorp/intranet.git`). Esto confirma que el directorio `.git` del proyecto, pensado para uso local del control de versiones, quedó accesible por HTTP.

El riesgo no depende de que ese único archivo sea sensible en sí mismo, sino de lo que normalmente contiene un `.git` completo: historial de commits, objetos con el código fuente en versiones anteriores y, en proyectos donde no se cuidó qué se versiona, configuraciones o credenciales que luego se removieron del código pero no de la historia. Si todo el directorio fuera descargable, sería posible reconstruir el repositorio completo con herramientas conocidas para ese fin.

En este caso probamos otras rutas típicas (`/.git/HEAD`, `/.git/logs/HEAD`, el listado de `/.git/`) y las tres devolvieron `404`. Eso es una observación, no una garantía: solo demuestra que esas rutas puntuales no están servidas con la configuración actual del servidor, no que el resto del repositorio sea inaccesible por otras vías no probadas, ni que el `config` filtrado carezca de valor. El dato concreto y verificado es la URL del remoto interno, que por sí sola ya es información de infraestructura que normalmente no debería ser pública: le dice a un atacante dónde vive el repositorio real de PhantomCorp.

Como mitigación, el servidor web no debería servir ningún archivo dentro de `.git/` (se soluciona con una regla de bloqueo a nivel de configuración del servidor, no solo ocultando archivos puntuales), y el directorio de publicación del sitio no debería coincidir con la raíz del repositorio de código.

### P3 — El método `PUT`

Durante la enumeración de métodos HTTP observamos que el servidor anuncia PUT como método permitido. Este resultado se obtuvo mediante una petición OPTIONS y se corroboró con los scripts HTTP de Nmap.
PUT puede ser peligroso porque permite enviar contenido a un recurso del servidor. En un escenario vulnerable, un atacante podría intentar utilizarlo para subir un archivo propio y, si además el servidor permitiera almacenarlo en una ruta ejecutable, podría llegar a producirse ejecución de código.
En este laboratorio no realizamos ninguna carga mediante PUT, por lo que no podemos afirmar que PhantomCorp permita subir o ejecutar archivos arbitrarios. Lo comprobado es únicamente que el método está habilitado. Como mitigación, debería deshabilitarse si no es necesario o restringirse mediante autenticación, autorización y permisos adecuados.

### P4 — Enumeración de usuarios

Durante la enumeración del servicio web de PhantomCorp consultamos el endpoint `/api/users` mediante el comando `curl -i http://phantomcorp/api/users`. El servidor respondió con un código HTTP 200 OK y devolvió información de tres usuarios: `admin`, con rol `superuser`; `jperez`, con rol `editor`; y `mgomez`, con rol `viewer`.

Además, la respuesta incluía una nota que indicaba que se trataba de un endpoint interno de Recursos Humanos que no debería estar expuesto. Pudimos acceder a esta información sin proporcionar credenciales.

Este hallazgo representa un riesgo porque permite conocer usuarios existentes y distinguir cuáles tienen mayores privilegios. Un atacante podría utilizar esta información para dirigir futuros intentos de acceso no autorizado, especialmente contra cuentas administrativas.

Sin embargo, esto no significa que hayamos conseguido acceder a las cuentas ni vulnerar el sistema de autenticación. Lo que comprobamos fue únicamente la exposición de usuarios y roles.

Para reducir este riesgo, recomendamos implementar controles de autenticación y autorización en la API, restringir el acceso a los endpoints internos y limitar la información que se devuelve a los usuarios.

### P5 — Rol defensor (3 mitigaciones)

_Pendiente de completar una vez documentados al menos tres hallazgos._

## 4. Bitácora de comandos

Los siguientes comandos se ejecutaron contra el contenedor autorizado `phantomcorp`, desde `cyberlab-attacker`:

```bash
# R1 — Enumeración de directorios
dirb http://phantomcorp/ -S
curl -sS -i http://phantomcorp/backup

# R2 — Repositorio Git expuesto
curl -sS -i http://phantomcorp/.git/config
curl -sS -i http://phantomcorp/.git/HEAD
curl -sS -i http://phantomcorp/.git/logs/HEAD
curl -sS -i http://phantomcorp/.git/

# R3 — Enumeración de métodos HTTP
curl -X OPTIONS -i http://phantomcorp/
nmap --script http-methods,http-enum phantomcorp
```

	### Registro de validación del R4

	Desde PowerShell, utilizando Docker, registramos la flag mediante una copia temporal del validador compatible con Linux:
```powershell
docker exec cyberlab-attacker bash /tmp/lab06-ctf/ctf submit 06 R4 'FLAG{user_enumeration_api}'
docker exec cyberlab-attacker bash /tmp/lab06-ctf/ctf status 06

	Desde la raíz del repositorio se registraron las flags observadas y se verificó el estado:

	```bash
	# R1
	./ctf submit 06 R1 'FLAG{dir_enumeration_backup}'

	# R2
	./ctf submit 06 R2 'FLAG{git_repo_exposed}'

	# R3
	./ctf submit 06 R3 'FLAG{http_methods_put_enabled}'

	./ctf status 06
	```

	Las salidas completas se preservan en `evidencias/`. Las operaciones se limitaron al target del Lab 06 provisto por la cátedra.
