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

## 1. Flags capturadas

| Reto      | Estado   | Evidencia                                               |
| --------- | -------- | ------------------------------------------------------- |
| R1 — Recon | Obtenida | [Salida cruda de R1](evidencia/salidas/r1-recon-opt.txt) y [envío de R1](evidencia/salidas/r1-submit.txt) |
| R2 — Loot | Obtenida | [Salida cruda de R2](evidencia/salidas/r2-loot-env.txt) |

La captura final de `./ctf status 08` queda pendiente de integrar cuando el grupo presente los cinco retos.

## 2. Informe de post-explotación

| Fase      | Qué hicimos                                                                                                                                                                                            | Comando/técnica                                                                                                                | Evidencia                                                                                                                         | Defensa                                                                                                                                                                                                                                 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Recon (R1) | Como `operador`, recién caído en el host, enumeramos `/opt` buscando información de despliegue que no debería estar ahí. Encontramos un subdirectorio con una nota de deploy legible por el usuario limitado. | `ls -la /opt`, `ls -la /opt/phantom-deploy` y `cat /opt/phantom-deploy/DEPLOY_NOTES.txt`, ejecutados desde el host víctima mediante `make shell-victima` (en esta sesión, `docker exec -u operador`). | [Salida R1](evidencia/salidas/r1-recon-opt.txt): confirma la identidad `operador`, el hostname `phantomcorp` y el contenido de `DEPLOY_NOTES.txt` con el `deploy_token` que incluye la flag. | Retirar notas y archivos de despliegue de rutas accesibles a cuentas de aplicación; aplicar permisos mínimos sobre `/opt`, inventariar qué queda en el filesystem tras un deploy y revisar ese inventario antes de pasar a producción. |
| Loot (R2) | Como el usuario limitado `operador`, leímos el archivo de configuración de la aplicación. El archivo reveló el host de BD, el usuario de aplicación, una contraseña y el secreto que contiene la flag. | `cat /var/www/.env` ejecutado desde el host víctima mediante `make shell-victima` (en esta sesión, `docker exec -u operador`). | [Salida R2](evidencia/salidas/r2-loot-env.txt): confirma la identidad `operador`, la existencia de `/var/www/.env` y sus valores. | Retirar secretos de archivos legibles por usuarios no autorizados; usar un gestor de secretos, identidad de workload/credenciales de corta vida, permisos mínimos, auditoría, rotación y revocación inmediata de los valores expuestos. |

### Observación, inferencia y límite — R1

**Observación.** El proceso se ejecutó como `uid=1000(operador)` en el host `phantomcorp`. Dentro de `/opt` existe un único subdirectorio, `phantom-deploy`, propiedad de `root:root`, que contiene un archivo `DEPLOY_NOTES.txt` legible por `operador`. Su contenido es `PhantomCorp - notas de despliegue (NO borrar)` seguido de `deploy_token=FLAG{post_situational_awareness}`.

**Inferencia.** Una nota de despliegue dejada en un directorio legible por una cuenta de aplicación de bajo privilegio indica que el proceso de deploy no limpió artefactos operacionales del sistema en producción. El nombre del campo (`deploy_token`) sugiere que, en un escenario real, ese valor podría usarse para autenticar o identificar un despliegue ante algún sistema externo, aunque este paquete no permite comprobar contra qué servicio se validaría.

**No verificado.** Esta evidencia no demuestra que el `deploy_token` esté vigente, que habilite por sí solo alguna acción privilegiada, ni que existan otros archivos sensibles fuera de `/opt` accesibles a `operador`. Encontrar información operacional no equivale a tener privilegios elevados; eso se evalúa recién en R3.

### Observación, inferencia y límite — R2

**Observación.** El proceso se ejecutó como `uid=1000(operador)`. `/var/www/.env` era un archivo de propiedad `root:root`, con permisos `0644`, y su contenido resultó legible para ese usuario. Incluía `DB_HOST=phantomcorp-db`, `DB_USER=phantom_app`, `DB_PASS=…` y `APP_SECRET=FLAG{loot_credentials_found}`.

**Inferencia.** Una cuenta local de bajo privilegio que pueda leer este archivo puede obtener credenciales de la aplicación y secretos que deberían estar restringidos. Si la contraseña sigue vigente y el usuario conserva permisos de conexión, esto reduce el costo de acceder al servicio interno de base de datos.

**No verificado.** Esta evidencia no demuestra por sí sola qué permisos tiene `phantom_app` dentro de la base, que la contraseña se reutilice en otros sistemas, ni que puedan modificarse datos. Esos aspectos requieren pruebas adicionales y permanecen fuera de R2.

## 3. Automatización

Pendiente del responsable de R5: adjuntar `src/recolector.py` completado y su salida contra el host interno desde la víctima.

## 4. Preguntas de análisis

### P2 — ¿Por qué el atacante no alcanzaba `phantomcorp-db` y sí pudo hacerlo desde la víctima?

El atacante inicial opera desde la red `labnet`, donde solo está expuesto el host `phantomcorp`. La base `phantomcorp-db` pertenece a una red interna separada y no es alcanzable desde esa consola externa. En cambio, el host víctima participa también en la red interna; por eso, una vez obtenido acceso como `operador`, pudo resolver y consultar `http://phantomcorp-db/`. La salida de apoyo de [pivoting](evidencia/salidas/p2-pivot-apoyo.txt) identifica al servicio como una base interna con acceso restringido a la LAN.

Esto ilustra un pivote: el host comprometido funciona como punto de apoyo desde una zona visible por el atacante hacia una red que no estaba expuesta directamente. No se creó un túnel ni se desplegó un proxy en esta práctica; se demostró únicamente que la posición de red de la víctima permite la conexión. La mitigación no es solo ocultar el nombre del host: requiere segmentación con reglas de salida mínimas, autenticación y autorización del servicio de base de datos, credenciales de mínimo privilegio y monitoreo de conexiones este-oeste inusuales.

## 5. Bitácora de P2

Ver [comandos de P2](evidencia/comandos.txt). Todos se ejecutaron exclusivamente en los contenedores autorizados del Lab 08.
