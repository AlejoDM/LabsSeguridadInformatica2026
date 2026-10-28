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

## 1. Resumen ejecutivo

Se evaluó el sistema ficticio «Clientes» de PhantomCorp dentro del alcance autorizado. Durante la evaluación se identificó un portal interno no enlazado y se demostró que su autenticación puede eludirse sin credenciales mediante una inyección SQL. La prueba obtuvo acceso al dashboard de RRHH presentado como `admin`.

El hallazgo confirmado es de severidad alta porque permite a un atacante remoto no autenticado eludir el control de acceso. No se demostró en esta etapa la extracción de datos de clientes, la modificación de información ni la afectación de disponibilidad. La prioridad inmediata es corregir la autenticación con consultas parametrizadas y revisar los privilegios de la cuenta de base de datos.

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

## 5. Conclusión

La evaluación confirmó que la visibilidad reducida de un portal no constituye un control de seguridad y que la autenticación es vulnerable a inyección SQL. La corrección prioritaria es eliminar la concatenación de entradas en consultas mediante parametrización y limitar los privilegios de la base de datos. Hasta este punto se demostró acceso no autorizado al área de RRHH; las etapas posteriores deben documentarse solo cuando cuenten con evidencia equivalente.

## 6. Anexo

- Bitácora: `evidencia/comandos.txt`.
- Salidas HTTP y validación: `evidencia/salidas/`.
- Estado comprobado: `evidencia/salidas/p2-validacion-ctf.txt`, R1 y R2 resueltos, 2/4.
- Análisis de reconocimiento: `evidencia/analisis/p1-recon-metodologia.md`.
- Análisis de acceso inicial: `evidencia/analisis/p2-acceso-hallazgo.md`.
- **Compatibilidad de validación:** el manifiesto de retos está en CRLF y el verificador no elimina ese carácter del hash. Se empleó una copia temporal normalizada exclusivamente para presentar las flags; el archivo original no fue modificado.
