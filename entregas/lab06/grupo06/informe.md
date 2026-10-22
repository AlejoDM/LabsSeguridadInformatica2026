# Informe — Laboratorio 06 · Enumeración

**Grupo:** 06
**Integrantes:**

| Nombre y apellido    | Usuario de GitHub |
| -------------------- | ----------------- |
| Martín Beccereca     | martinbeccereca   |
| Belén Benito         | belubenito01      |
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

- **Finalidad del uso:** apoyo en la redacción y revisión de la documentación.
- **Partes asistidas:** fila R3 del inventario, respuesta P3 y organización de la bitácora.
- **Verificación:** los comandos y pruebas fueron ejecutados contra el contenedor `phantomcorp`; las afirmaciones se contrastaron con las salidas originales conservadas en `evidencias/`.

## 1. Flags capturadas

| Reto                                 | Estado    | Evidencia                                                                                                |
| ------------------------------------ | --------- | -------------------------------------------------------------------------------------------------------- |
| R1 — Enumeración de directorios      | Resuelto  | [Envío de R1](evidencias/lab06-r1-submit.txt) y [estado posterior](evidencias/lab06-status-after-r1.txt) |
| R2 — Repositorio Git expuesto        | Resuelto  | [config filtrado](evidencias/lab06-r2-git-config.txt) y [envío de R2](evidencias/lab06-r2-submit.txt)    |
| R3 — Métodos HTTP peligrosos         | Resuelto | [OPTIONS](evidencias/lab06-r3-options.txt) y [Nmap HTTP](evidencias/lab06-r3-nmap-http.txt)                                                                                                        |
| R4 — Enumeración de usuarios vía API | Pendiente | —                                                                                                        |
| R5 — Fingerprinting de tecnología    | Pendiente | —                                                                                                        |

La salida de estado posterior al R1 registra 1 de 5 retos resueltos. El archivo [progreso-06.done](evidencias/progreso-06.done) es una copia del estado local del motor y complementa, pero no reemplaza, la salida legible de `./ctf status 06`.

## 2. Inventario de enumeración

| Hallazgo                                            | Ruta/Método | Técnica                                                               | Evidencia                                                                                                                                                                                                               | Riesgo                                                                                                                                                                                                                     | ¿Qué habilita para el Lab 07?                                                                                                                                                                                                    |
| --------------------------------------------------- | ----------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Directorio de respaldos accesible sin autenticación | `/backup`   | Enumeración de directorios con `dirb`; confirmación manual con `curl` | `dirb` reportó `/backup` con `200`; la respuesta HTTP lista `respaldo-db-2024.sql.gz` y `config.old`. Ver [salida de dirb](evidencias/lab06-r1-dirb.txt) y [confirmación de `/backup`](evidencias/lab06-r1-backup.txt). | Un tercero con acceso al servicio puede consultar el índice observado. Los nombres de archivos son indicios de datos y configuraciones potencialmente sensibles; no se descargó ni verificó el contenido de esos archivos. | Orienta el análisis posterior hacia respaldos y configuraciones expuestos. Si alguno fuera accesible y contuviera datos o credenciales, podría habilitar nuevas hipótesis de explotación; esa condición no fue verificada en R1. |
| Método HTTP `PUT` habilitado | `OPTIONS /` — método `PUT` | Enumeración de métodos HTTP con `curl`; corroboración con scripts NSE de Nmap | La respuesta a `OPTIONS` indicó que `PUT` está habilitado y la enumeración con Nmap corroboró el hallazgo. Ver [respuesta OPTIONS](evidencias/lab06-r3-options.txt) y [enumeración con Nmap](evidencias/lab06-r3-nmap-http.txt). | La habilitación de `PUT` amplía la superficie de ataque porque puede permitir enviar contenido a recursos del servidor. En este lab no se comprobó que permita escritura arbitraria ni ejecución de archivos. | Orienta el Lab 07 a verificar de forma controlada si `PUT` permite crear o reemplazar recursos y, solo si se cumplen las condiciones necesarias, evaluar una posible carga de archivos. |

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

## 3. Preguntas de análisis

### P1 — Enumeración vs. recon

En el Lab 05 realizamos reconocimiento para construir un mapa amplio de la superficie de PhantomCorp. Con `nmap -Pn -sV -p- phantomcorp` identificamos cuatro servicios expuestos: FTP en 21, HTTP en 80, HTTP/API en 8080 y un servicio no identificado en 31337. También usamos headers HTTP y `robots.txt` para reunir indicios iniciales sobre el servicio web. El resultado fue conocer qué servicios estaban disponibles y cuáles requerían análisis posterior.

En el Lab 06 realizamos enumeración sobre el servicio web identificado. Ejecutamos `dirb http://phantomcorp/`, que encontró `/admin` con código `403` y `/backup` con código `200`. Luego confirmamos este último recurso con `curl -sS -i http://phantomcorp/backup`; la respuesta mostró un listado que incluye `respaldo-db-2024.sql.gz` y `config.old`. Estas observaciones están respaldadas por las salidas de R1 enlazadas en el inventario.

Por lo tanto, el reconocimiento respondió qué servicios existían y dónde estaban; la enumeración profundizó dentro de uno de esos servicios para identificar recursos no enlazados, su nivel de acceso y sus consecuencias potenciales. El Lab 05 produjo el mapa inicial y el Lab 06 comienza a construir el inventario detallado que orientará hipótesis para el Lab 07.

### P2 — El `.git` expuesto

_Pendiente de completar con la evidencia de R2._

### P3 — El método `PUT`

Durante la enumeración de métodos HTTP observamos que el servidor anuncia PUT como método permitido. Este resultado se obtuvo mediante una petición OPTIONS y se corroboró con los scripts HTTP de Nmap.
PUT puede ser peligroso porque permite enviar contenido a un recurso del servidor. En un escenario vulnerable, un atacante podría intentar utilizarlo para subir un archivo propio y, si además el servidor permitiera almacenarlo en una ruta ejecutable, podría llegar a producirse ejecución de código.
En este laboratorio no realizamos ninguna carga mediante PUT, por lo que no podemos afirmar que PhantomCorp permita subir o ejecutar archivos arbitrarios. Lo comprobado es únicamente que el método está habilitado. Como mitigación, debería deshabilitarse si no es necesario o restringirse mediante autenticación, autorización y permisos adecuados.

### P4 — Enumeración de usuarios

_Pendiente de completar con la evidencia de R4._

### P5 — Rol defensor (3 mitigaciones)

_Pendiente de completar una vez documentados al menos tres hallazgos._

## 4. Bitácora de comandos

Los siguientes comandos se ejecutaron contra el contenedor autorizado `phantomcorp`, desde `cyberlab-attacker`:

```bash
# R1 — Enumeración de directorios
dirb http://phantomcorp/ -S
curl -sS -i http://phantomcorp/backup

# R3 — Enumeración de métodos HTTP
curl -X OPTIONS -i http://phantomcorp/
nmap --script http-methods,http-enum phantomcorp
```

Desde la raíz del repositorio se registraron las flags observadas y se verificó el estado:

```bash
# R1
./ctf submit 06 R1 'FLAG{dir_enumeration_backup}'

# R3
./ctf submit 06 R3 'FLAG{http_methods_put_enabled}'

./ctf status 06
```

Las salidas completas se preservan en `evidencias/`. Las operaciones se limitaron al target del Lab 06 provisto por la cátedra.