# P3 — R3: post-explotación y secreto looteado

## Procedimiento y evidencia

Partiendo del acceso demostrado por P2 (bypass de autenticación en `POST
/portal/login`), la respuesta de ese hito ya indicaba un recurso posterior:
`/backup/rrhh.conf`. Se solicitó ese recurso sin ninguna credencial ni cookie
de sesión adicional, desde `cyberlab-attacker`:

```bash
docker exec cyberlab-attacker curl -sS -i --max-time 10 http://phantomcorp/backup/rrhh.conf
```

La respuesta fue `200 OK` y expuso texto plano con credenciales de base de
datos y un token de API, además de la flag `FLAG{final_token_looted}`
(`../salidas/p3-r3-evidencia.txt`).

Como control negativo, se solicitó una ruta inexistente bajo el mismo prefijo:

```bash
docker exec cyberlab-attacker curl -sS -i --max-time 10 http://phantomcorp/backup/p3-control-inexistente.conf
```

La respuesta fue `404 Not Found` (`../salidas/p3-control.txt`), lo que
descarta que `/backup/` responda igual para cualquier ruta y respalda que el
archivo de configuración existe realmente en el servidor.

No se solicitó `/api/reporte` ni se usó el token contra ningún endpoint: ese
uso corresponde al hito de impacto (R4) y queda fuera del alcance de este
hito.

## H-03 — Exposición de archivo de configuración con credenciales y token de API

- **Ubicación:** `GET /backup/rrhh.conf`.
- **Condición observada:** el servidor sirve un archivo de configuración en
  texto plano sin requerir autenticación ni sesión; la única barrera previa
  fue no conocer la ruta, que la propia respuesta del hallazgo de R2 reveló.
- **Impacto demostrado:** divulgación de credenciales de base de datos
  (`DB_USER`/`DB_PASS`) y de un token de API (`API_TOKEN`) a cualquiera que
  conozca o adivine la ruta, sin necesidad de autenticarse en el portal.
- **Severidad:** Alta. CVSS v3.1:
  `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` (7.5). El acceso es remoto,
  sin privilegios ni interacción de usuario, y el resultado confirmado es la
  divulgación de secretos con alto impacto en confidencialidad. No se
  modificó información ni se afectó disponibilidad, y no se demostró en este
  hito el alcance de lo que el token habilita.
- **Remediación:** retirar archivos de configuración y backups del
  directorio servido por el aplicativo web; si deben persistir, ubicarlos
  fuera del `document root` y con control de acceso autenticado. Rotar de
  inmediato las credenciales y el token expuestos. No incluir secretos en
  archivos de texto plano accesibles por HTTP; usar un gestor de secretos o
  variables de entorno fuera del árbol web.
- **Limitación:** no se verificó si el mismo archivo es alcanzable sin pasar
  por el hallazgo de R2 (por ejemplo, listando `/backup/` directamente) ni se
  probaron otras rutas de backup; tampoco se usó el token contra `/api/reporte`.
  La vigencia del token y su alcance real no están demostrados en este hito.

## Traspaso P3 → P4

El secreto del caso es el `API_TOKEN` obtenido en `/backup/rrhh.conf`
(`../salidas/p3-r3-evidencia.txt`). El mismo archivo indica su uso esperado:
`/api/reporte?token=...&cmd=...`. P4 puede partir de ese dato para reproducir
el acceso de impacto (R4) sin necesidad de repetir R1–R3. P3 no ejecutó
ninguna solicitud contra `/api/reporte` ni determinó qué datos de clientes
quedan expuestos: eso corresponde al hito de impacto.
