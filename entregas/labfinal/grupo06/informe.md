# Informe de Penetration Test — PhantomCorp «Clientes»

**Grupo:** 06
**Fecha:** 2026-10-28
**Cliente:** PhantomCorp S.A. · **Tipo:** Caja negra · **Alcance:** host `phantomcorp` del laboratorio

| Nombre y apellido    | Usuario de GitHub |
| -------------------- | ----------------- |
| Martín Beccereca     | martinbeccereca   |
| Belén Benito         | belubenito603     |
| Alejo José De Miguel | AlejoDM           |
| Tomás Giudici        | TomasGiudici      |
| Carolina Suppo       | carosuppo         |

## 0. Declaración de uso de IA

**Herramienta:** Codex (OpenAI).

- **Finalidad y partes asistidas:** apoyo en el reconocimiento, las pruebas controladas de autenticación, el registro de evidencias y la redacción del informe.
- **Verificación:** las respuestas HTTP, el cambio de comportamiento ante las solicitudes y las flags fueron contrastados manualmente en el entorno autorizado.

- **Herramienta:** Claude (Anthropic), vía Claude Code.
- **Finalidad y partes asistidas:** apoyo en la post-explotación de R3, estructurar el hallazgo H-03 (CVSS, remediación, limitaciones).
- **Verificación:** la solicitud a `/backup/rrhh.conf`, la respuesta `200 OK` con el secreto y la flag, el control negativo (404) y la validación de R3 ante `./ctf status final` fueron ejecutados y contrastados manualmente contra el entorno autorizado (`phantomcorp`); el texto del hallazgo se revisó contra la evidencia cruda antes de incorporarlo.

### Persona 4 — Carolina Suppo

**Herramienta:** Opencode.

- **Finalidad y partes asistidas:** apoyo para estructurar el análisis de R4, describir el impacto observado y revisar la priorización de hallazgos y remediaciones.
- **Verificación:** se contrastaron las respuestas HTTP de `/api/reporte`, el conteo, el contenido limitado del recurso de clientes y la aceptación de R4 con las evidencias originales. No se afirma extracción de registros individuales.

### Persona 5 — Integración y control de calidad

**Herramienta:** ChatGPT (OpenAI).

- **Finalidad y partes asistidas:** apoyo para integrar los análisis de P1–P4, actualizar el resumen ejecutivo, completar la narrativa del ataque, incorporar los hallazgos técnicos, redactar la conclusión y organizar el anexo.
- **Verificación realizada:** revisión de los aportes individuales, comprobación de la estructura del informe y control de formato mediante `git diff --check`.
- **Verificación completada:** Persona 5 reprodujo independientemente R1–R4 en el entorno autorizado y confirmó el progreso oficial del CTF: 4/4 (100 %). Evidencias: `evidencia/salidas/p5-verificacion-final.txt` y `evidencia/salidas/p5-status-final-4de4.txt`.

## 1. Resumen ejecutivo

Se realizó una evaluación de seguridad de caja negra sobre el sistema ficticio «Clientes» de PhantomCorp, exclusivamente dentro del entorno autorizado de la cátedra. El trabajo permitió reconstruir una cadena de cuatro etapas que comenzó con el descubrimiento de un portal interno y terminó demostrando acceso a un recurso de información de clientes.

Durante la evaluación se identificaron tres vulnerabilidades relevantes: una inyección SQL que permite ingresar al portal de RRHH sin credenciales válidas, la exposición pública de un archivo de configuración con credenciales y un token de API, y una API que permite ejecutar comandos del sistema utilizando dicho token. Las pruebas demostraron que esta última funcionalidad se ejecuta con privilegios de root.

El equipo alcanzó el archivo `priv/clientes.db.txt`, cuya respuesta informa la existencia de 48.210 registros y los campos nombre, DNI y tarjeta. No se extrajeron registros individuales ni se realizaron modificaciones sobre los datos.

Se recomienda priorizar la eliminación de la ejecución de comandos desde la API, reducir los privilegios del servicio, retirar los secretos del directorio público y rotar las credenciales expuestas. También debe corregirse la autenticación mediante consultas parametrizadas. Estas acciones buscan interrumpir la cadena de ataque y reducir la exposición de información sensible.

## 2. Alcance y metodología

Se evaluó únicamente el servicio HTTP de `phantomcorp` del integrador desde `cyberlab-attacker`, conectado a `cyberlab_labnet`. Se inició el entorno oficial con Docker Compose, equivalente a `make lab N=final`, sin modificar el target ni consultar su código, soluciones o manifiesto para descubrir rutas o flags. Las solicitudes de reconocimiento ocurrieron el 28/10/2026 entre 17:10:20 y 17:10:31 UTC (14:10:20–14:10:31 en Argentina), según las cabeceras del servidor.

El trabajo comprendió reconocimiento y enumeración dirigida (página inicial, `robots.txt`, ruta anunciada y una ruta inexistente de control), seguidos de dos solicitudes POST controladas al formulario descubierto: una con credenciales deliberadamente inválidas y otra con una condición booleana para comprobar la hipótesis de inyección SQL. Todas las solicitudes tuvieron un tiempo máximo de diez segundos. No se escanearon otros hosts, no se realizaron acciones destructivas, extracción masiva ni denegación de servicio. La ventana autorizada es la fijada por la cátedra; no consta un horario adicional en los materiales revisados.

| Recurso observado         | Resultado                                | Evidencia                            |
| ------------------------- | ---------------------------------------- | ------------------------------------ |
| `http://phantomcorp/`     | 200, portal público sin enlaces visibles | `evidencia/salidas/p1-inicio.txt`    |
| `/robots.txt`             | 200; anuncia `/portal-rrhh`              | `evidencia/salidas/p1-robots.txt`    |
| `/portal-rrhh`            | 200; portal interno y formulario         | `evidencia/salidas/p1-r1-portal.txt` |
| `/p1-control-inexistente` | 404, Not Found                           | `evidencia/salidas/p1-control.txt`   |

Las cabeceras declaran `PhantomClientes/2.0`; esto es un banner observado, no una identificación independiente del software instalado. La comparación con el 404 respalda que el portal no es simplemente una respuesta genérica para cualquier ruta. No se pretende un inventario exhaustivo de servicios.

## 3. Narrativa del ataque

### Reconocimiento y enumeración

La página inicial respondió con el portal público, sin enlaces al portal interno. Se consultó `robots.txt` como recurso habitual de enumeración: su línea `Disallow: /portal-rrhh` proporcionó una ruta concreta. Al solicitarla directamente, el servidor devolvió el título «Portal RRHH PhantomCorp», un formulario POST hacia `/portal/login`, los campos `user` y `pass`, y la flag `FLAG{final_recon_portal}` en un comentario HTML.

### Acceso inicial sin credenciales válidas

Se estableció una línea base enviando credenciales deliberadamente inválidas a `POST /portal/login`; el servidor respondió `401 Unauthorized`. Luego, una solicitud con `user=' OR '1'='1' -- ` y `pass=x` devolvió `200 OK`, el mensaje «Bienvenido admin. Dashboard RRHH.» y la flag `FLAG{final_sqli_foothold}`. El cambio de resultado con una contraseña sin valor confirma el bypass de autenticación. La respuesta también indicó un recurso posterior para investigar, que no fue consultado en este hito.

### Post-explotación: exposición del secreto (R3)

Después de demostrar el acceso no autorizado al portal de RRHH, la respuesta obtenida en R2 señaló el recurso `/backup/rrhh.conf`. El equipo consultó ese archivo desde el entorno autorizado y recibió HTTP 200, sin necesidad de presentar credenciales ni una cookie de sesión adicional.

El archivo de configuración exponía credenciales de base de datos y un token de API. Una solicitud de control a una ruta inexistente dentro de `/backup/` respondió HTTP 404, respaldando que el recurso consultado existía realmente.

Esta exposición permitió identificar el secreto necesario para continuar hacia la API de reportes. La evidencia está registrada en `evidencia/salidas/p3-r3-evidencia.txt` y `evidencia/salidas/p3-control.txt`.

### Impacto sobre el recurso de clientes (R4)

Con el token obtenido en R3, se accedió a `/api/reporte` desde la consola atacante del laboratorio. Las respuestas demostraron que la API permitía ejecutar comandos del sistema y que el proceso utilizaba privilegios de root.

Mediante solicitudes limitadas de solo lectura, el equipo identificó el archivo `priv/clientes.db.txt`. La respuesta de la consulta informó que el recurso representa 48.210 registros y contiene los campos nombre, DNI y tarjeta.

No se extrajeron registros individuales ni se realizaron modificaciones sobre los datos. El impacto confirmado es la ejecución de comandos con privilegios elevados y el acceso al recurso que contiene información de clientes.

Las evidencias se encuentran en `evidencia/salidas/p4-r4-identidad.txt`, `p4-r4-recurso.txt`, `p4-r4-conteo.txt` y `p4-r4-impacto.txt`.
## 4. Hallazgos (detalle técnico)

- **Reproducción del hallazgo:**

  Los siguientes comandos se ejecutaron desde el host mediante el contenedor atacante:

  ```bash
  docker exec cyberlab-attacker curl -sS -i --max-time 10 http://phantomcorp/robots.txt
  docker exec cyberlab-attacker curl -sS -i --max-time 10 http://phantomcorp/portal-rrhh
  ```

  **Resultados observados:**
  - `robots.txt` respondió `200 OK` y contenía `Disallow: /portal-rrhh`.
  - `/portal-rrhh` respondió `200 OK` y mostró un formulario `POST /portal/login` con los campos `user` y `pass`.
  - La respuesta HTML incluyó la flag `FLAG{final_recon_portal}`.

  Las respuestas originales se conservan en `evidencia/salidas/p1-robots.txt` y `evidencia/salidas/p1-r1-portal.txt`.

### Portal interno descubrible mediante robots.txt

- **Ubicación:** `/robots.txt` y `/portal-rrhh`.
- **Descripción:** un recurso público anuncia la ruta de un portal interno no enlazado desde la portada observada. El acceso no autenticado permite visualizar su formulario.
- **Evidencia:** respuestas completas en `p1-robots.txt` y `p1-r1-portal.txt`.
- **Impacto demostrado:** descubrimiento de la superficie de autenticación y de sus parámetros. No se demostró acceso a sesiones, secretos ni datos de clientes.
- **Clasificación:** observación informativa; sin CVSS asignado. Encontrar una página de login no demuestra por sí solo una vulnerabilidad explotable ni permite justificar un score.
- **Recomendación:** no tratar robots.txt ni una URL poco visible como control de acceso. Revisar si el portal debe ser accesible desde esta red y aplicar restricciones y autorización efectivas según su finalidad. Retirar referencias innecesarias reduce pistas, pero no sustituye esos controles.

### H-02 — Inyección SQL que permite el bypass de autenticación

- **Ubicación:** `POST /portal/login`, parámetro `user`.
- **Descripción:** el portal aceptó una condición SQL booleana en el nombre de usuario y creó una sesión presentada como `admin` pese a recibir una contraseña sin valor.
- **Evidencia reproducible:** la solicitud con credenciales inválidas y su respuesta `401` están en `evidencia/salidas/p2-r2-base.txt`; la solicitud de prueba y su respuesta `200` están en `evidencia/salidas/p2-r2-acceso.txt`.
- **Impacto demostrado:** un usuario remoto sin credenciales válidas accedió al dashboard de RRHH como `admin`.
- **Severidad:** Alta. CVSS v3.1: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` (7.5). La prueba fue remota, no requirió privilegios ni interacción y consiguió acceso no autorizado a un área administrativa. No se demostró modificación, afectación de disponibilidad ni acceso a datos de clientes.
- **Remediación:** reemplazar cualquier construcción dinámica de consultas de autenticación por consultas parametrizadas/prepared statements. Aplicar privilegios mínimos a la cuenta de base de datos y registrar/rechazar sintaxis anómala como control complementario. Verificar el arreglo comprobando que la misma solicitud booleana recibe el mismo rechazo que las credenciales inválidas y no crea sesión.
- **Limitación:** no se realizaron consultas de enumeración, extracción de tablas, modificaciones de datos ni acciones fuera del portal.

### H-03 — Exposición de archivo de configuración con credenciales y token de API

- **Ubicación:** `GET /backup/rrhh.conf`.
- **Descripción:** el servidor permitió acceder mediante HTTP a un archivo de configuración en texto plano, sin requerir autenticación ni sesión. El recurso contenía credenciales de base de datos y un token de API.
- **Evidencia:** `evidencia/salidas/p3-r3-evidencia.txt`. Una solicitud de control a una ruta inexistente devolvió HTTP 404 (`evidencia/salidas/p3-control.txt`).
- **Impacto demostrado:** divulgación de credenciales y del token a quien conozca o descubra la ruta. El token permitió continuar hacia el hito R4.
- **Severidad:** Alta — CVSS v3.1: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` (7.5).
- **Remediación:** retirar el archivo de configuración del directorio público, impedir su acceso mediante HTTP y rotar inmediatamente las credenciales y el token expuestos. Utilizar almacenamiento seguro de secretos y controles de acceso efectivos.
- **Limitación:** no se exploraron otros archivos de backup ni se verificó la utilización de las credenciales de base de datos.

### H-04 — Ejecución de comandos del sistema mediante la API de reportes

- **Ubicación:** `GET /api/reporte`, parámetros `token` y `cmd`.
- **Descripción:** utilizando el token obtenido en R3, la API aceptó comandos del sistema. Las respuestas confirmaron que el proceso se ejecutaba como `root`.
- **Evidencia:** `evidencia/salidas/p4-r4-identidad.txt`, `p4-r4-recurso.txt`, `p4-r4-conteo.txt` y `p4-r4-impacto.txt`.
- **Impacto demostrado:** ejecución de comandos de lectura con privilegios elevados y acceso al recurso `priv/clientes.db.txt`, cuya respuesta describe 48.210 registros y campos de nombre, DNI y tarjeta. No se extrajeron registros individuales.
- **Severidad:** Alta — CVSS v3.1: `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` (8.8). La API requiere un token, pero este se obtuvo de un archivo expuesto públicamente. Los impactos altos en integridad y disponibilidad representan capacidades potenciales de la ejecución como root; no se probaron acciones destructivas.
- **Remediación:** eliminar la ejecución arbitraria de comandos del sistema desde la API. Implementar operaciones de reporte predefinidas y autorizadas, ejecutar el servicio con privilegios mínimos, controlar el acceso al endpoint y rotar el token expuesto.
- **Limitación:** no se modificaron datos, no se realizaron acciones destructivas ni se recuperaron registros individuales de clientes.
## 5. Conclusión

La evaluación permitió demostrar una cadena de ataque que comenzó con el descubrimiento de un portal interno y continuó con la elusión de su autenticación mediante una inyección SQL. A partir de ese acceso se identificó un archivo de configuración expuesto que contenía credenciales y un token de API. Finalmente, el token permitió utilizar una API que ejecutaba comandos con privilegios de root y acceder al recurso asociado con los datos de clientes.

Se confirmaron tres vulnerabilidades de severidad alta: H-02 (CVSS 7.5), H-03 (CVSS 7.5) y H-04 (CVSS 8.8), según la evaluación documentada. La combinación de estas debilidades evidencia que una falla inicial puede facilitar el descubrimiento y aprovechamiento de otras superficies inseguras.

El impacto observado incluye acceso no autorizado al dashboard de RRHH, exposición de secretos, ejecución de comandos de lectura como root y acceso al archivo de clientes. La respuesta del recurso indica 48.210 registros y campos de nombre, DNI y tarjeta; sin embargo, no se extrajeron registros individuales ni se alteró información.

Las acciones correctivas se priorizan de la siguiente manera:

1. **H-04 — API de reportes:** eliminar la ejecución arbitraria de comandos, implementar operaciones permitidas y ejecutar el servicio con privilegios mínimos.
2. **H-03 — Secretos expuestos:** retirar el archivo del directorio público, impedir su acceso por HTTP y rotar las credenciales y el token comprometidos.
3. **H-02 — Autenticación:** implementar consultas parametrizadas, reforzar los controles de acceso y limitar los privilegios de la base de datos.

Como conclusión general, la seguridad del sistema no puede depender de que un portal permanezca oculto ni de que un token sea difícil de descubrir. La corrección de las causas raíz y la aplicación de controles de acceso efectivos son fundamentales para impedir que vulnerabilidades independientes se encadenen y comprometan recursos sensibles.
## 6. Anexo

### Registro de evidencias

- **Bitácora general:** `evidencia/comandos.txt`.
- **R1 — Reconocimiento:** `evidencia/salidas/p1-robots.txt`, `p1-r1-portal.txt` y `p1-submit-compatibilidad.txt`.
- **R2 — Explotación:** `evidencia/salidas/p2-r2-base.txt`, `p2-r2-acceso.txt` y `p2-validacion-ctf.txt`.
- **R3 — Post-explotación:** `evidencia/salidas/p3-r3-evidencia.txt`, `p3-control.txt` y `p3-validacion-ctf.txt`.
- **R4 — Impacto:** `evidencia/salidas/p4-r4-identidad.txt`, `p4-r4-recurso.txt`, `p4-r4-conteo.txt`, `p4-r4-impacto.txt` y `p4-r4-submit.txt`.

### Análisis individuales

- P1: `evidencia/analisis/p1-recon-metodologia.md`.
- P2: `evidencia/analisis/p2-acceso-hallazgo.md`.
- P3: `evidencia/analisis/p3-postexplotacion.md`.
- P4: `evidencia/analisis/p4-impacto-remediacion.md`.

### Estado de validación

Las evidencias individuales registran la aceptación de R1, R2, R3 y R4 por el motor CTF. Los estados fueron obtenidos en entornos locales de distintos integrantes.

**Completado:** Persona 5 verificó el recorrido R1–R4 y registró el estado consolidado del CTF: **4/4 (100 %)**, el 30/10/2026. El resultado oficial está documentado en `evidencia/salidas/p5-status-final-4de4.txt`.

### Compatibilidad de validación

Para las validaciones que lo requirieron se utilizó una copia temporal del manifiesto con finales de línea normalizados de CRLF a LF. No se modificó el manifiesto original.
