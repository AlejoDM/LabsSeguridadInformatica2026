# P4 — R4: impacto en datos de clientes

## Procedimiento y evidencia

Se continuó desde el traspaso de P3: el token del laboratorio se obtuvo del recurso indicado en `../salidas/p3-r3-evidencia.txt` y se usó únicamente contra `http://phantomcorp/api/reporte`. No se copia el valor del token en este análisis ni en las nuevas salidas.

Las pruebas se ejecutaron desde `cyberlab-attacker`. La solicitud al endpoint sin el parámetro `cmd` devolvió el resultado de `id`: el proceso que atiende la API se ejecutó como `uid=0(root)` (`../salidas/p4-r4-identidad.txt`). Luego se enumeró solo el directorio `priv`, que contenía `clientes.db.txt` (`../salidas/p4-r4-recurso.txt`). Las solicitudes fueron:

```bash
TOKEN=$(curl -fsS --max-time 10 http://phantomcorp/backup/rrhh.conf |
  sed -n 's/^API_TOKEN=//p')
curl -sS -i --max-time 10 --get --data-urlencode "token=$TOKEN" \
  http://phantomcorp/api/reporte
curl -sS -i --max-time 10 --get --data-urlencode "token=$TOKEN" \
  --url "http://phantomcorp/api/reporte?cmd=ls+priv"
curl -sS -i --max-time 10 --get --data-urlencode "token=$TOKEN" \
  --url "http://phantomcorp/api/reporte?cmd=wc+-l+priv/clientes.db.txt"
```

El conteo devolvió una sola línea (`../salidas/p4-r4-conteo.txt`). Para limitar la lectura a ese contenido, se consultó únicamente la primera línea:

```bash
TOKEN=$(curl -fsS --max-time 10 http://phantomcorp/backup/rrhh.conf |
  sed -n 's/^API_TOKEN=//p')
curl -sS -i --max-time 10 --get --data-urlencode "token=$TOKEN" \
  --url "http://phantomcorp/api/reporte?cmd=head+-n+1+priv/clientes.db.txt"
```

La respuesta fue `200 OK` e informó que el recurso representa 48.210 registros y enumera los campos nombre, DNI y tarjeta; también devolvió `FLAG{final_crown_jewels}` (`../salidas/p4-r4-impacto.txt`). La línea consultada no contenía valores individuales de clientes. Por eso el resultado confirma acceso al recurso de datos y su estructura declarada, pero no se afirma que se hayan leído ni extraído los 48.210 registros.

La flag R4 fue aceptada por el motor CTF; el resultado está en `../salidas/p4-r4-submit.txt`. Para la validación se utilizó una copia temporal del manifiesto con los finales de línea normalizados, sin modificar el archivo original de `labs/`.

El `./ctf status final` de este workspace muestra R4 y 1/4: aquí no están registradas localmente las flags anteriores, aunque los aportes de P1–P3 conservan sus propias validaciones. P5 debe comprobar y guardar el estado consolidado al verificar el recorrido completo.

## H-04 — Ejecución de comandos del sistema mediante la API de reportes

- **Ubicación:** `GET /api/reporte`, parámetros `token` y `cmd`.
- **Condición observada:** con el token indicado por P3, el endpoint procesó comandos enviados en `cmd`. La solicitud sin `cmd` devolvió `id` con `uid=0(root)`; otras solicitudes de solo lectura localizaron y consultaron el recurso de clientes.
- **Impacto demostrado:** ejecución remota de comandos de lectura como root y acceso al archivo `priv/clientes.db.txt`. La respuesta observada expone el número declarado de registros y los nombres de campos, no valores individuales.
- **Severidad:** Alta — CVSS v3.1: `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` (8.8). El vector valora el endpoint con el requisito de presentar un token (PR:L), una solicitud remota de baja complejidad y sin interacción de usuario. Como P3 obtuvo ese token de un recurso servido sin autenticación, el encadenamiento reduce en la práctica la barrera de acceso; esto se considera en la prioridad propuesta. La ejecución como root permite impacto potencial alto sobre confidencialidad, integridad y disponibilidad dentro del mismo sistema; no se probaron escrituras, borrados ni interrupciones.
- **Remediación:** eliminar la ejecución de comandos del sistema desde la API. Si el reporte es necesario, implementar una operación fija que consulte únicamente los datos autorizados, con consultas parametrizadas y validación en el servidor. Ejecutar el servicio con una cuenta sin privilegios de root, limitar el acceso por autenticación y autorización, retirar el archivo de secretos del directorio web y rotar el token expuesto. Verificar que `cmd` no pueda seleccionar comandos del sistema y que el reporte solo devuelva los campos permitidos.
- **Limitación:** no se modificaron datos ni se intentaron acciones destructivas; tampoco se recuperaron registros individuales. El alcance de esta prueba fue el objetivo `phantomcorp` del laboratorio.

## Revisión de prioridades R1–R3

1. **H-04 (R4), Alta, CVSS 8.8:** retirar primero la capacidad de ejecución de comandos como root y reducir privilegios del servicio.
2. **H-03 (R3), Alta, CVSS 7.5:** sacar el archivo de configuración del directorio servido y rotar credenciales y token; su exposición facilita el acceso a la API de R4.
3. **H-02 (R2), Alta, CVSS 7.5:** corregir la consulta de autenticación con parametrización y limitar los privilegios de la cuenta de base de datos.
4. **R1:** P1 lo documenta como descubrimiento de superficie, no como vulnerabilidad independiente con CVSS. La ruta poco visible no sustituye controles de acceso.

H-02 y H-03 tienen el mismo puntaje informado; se prioriza H-03 antes por habilitar directamente el acceso usado en R4. Las remediaciones propuestas por P2 y P3 atacan la causa observada. Esta revisión es una propuesta para que P5 la integre y contraste con el informe completo.

## Declaración de uso de IA

**Herramienta:** Opencode.

- **Finalidad y partes asistidas:** apoyo para estructurar el análisis de R4, describir el impacto observado y revisar la priorización y las remediaciones.
- **Verificación:** revisé personalmente las respuestas HTTP de `/api/reporte`, el conteo, la línea consultada y la aceptación de R4 contra las salidas crudas de `phantomcorp`. El análisis se limitó a lo observado, sin afirmar extracción de registros individuales ni cambios en los datos.
