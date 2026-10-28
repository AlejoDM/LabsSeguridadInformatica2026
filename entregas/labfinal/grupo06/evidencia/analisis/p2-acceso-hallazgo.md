# P2 — R2: bypass de autenticación por inyección SQL

## Resultado y evidencia

Se trabajó exclusivamente contra `http://phantomcorp/portal/login`, la acción del formulario entregada por P1. Desde `cyberlab-attacker` se estableció primero una línea base con credenciales deliberadamente inválidas:

```bash
docker exec cyberlab-attacker curl -sS -i --max-time 10 -X POST http://phantomcorp/portal/login --data-urlencode "user=p2-prueba-invalida" --data-urlencode "pass=credencial-invalida"
```

La respuesta fue `401 Unauthorized` y el cuerpo `Credenciales invalidas` (`../salidas/p2-r2-base.txt`).

Como prueba mínima de la hipótesis de inyección SQL, se sustituyó el campo `user` por una condición booleana y se mantuvo una contraseña sin valor:

```bash
docker exec cyberlab-attacker curl -sS -i --max-time 10 -X POST http://phantomcorp/portal/login --data-urlencode "user=' OR '1'='1' -- " --data-urlencode "pass=x"
```

La respuesta fue `200 OK`, identificó la sesión como `admin` y mostró `Dashboard RRHH` (`../salidas/p2-r2-acceso.txt`). Este cambio de 401 a 200 con una contraseña inválida demuestra un bypass de autenticación. La flag `FLAG{final_sqli_foothold}` se validó con el motor CTF mediante la normalización temporal de CRLF del manifiesto de validación, ya que el comando oficial directo no interpreta los hashes terminados en CRLF. El progreso registrado es R1 y R2, 2/4.

## H-02 — Inyección SQL que permite el bypass de autenticación

- **Ubicación:** `POST /portal/login`, parámetro `user`.
- **Condición observada:** una entrada SQL booleana en `user` fue aceptada con `pass=x` y cambió la respuesta de rechazo a una sesión mostrada como `admin`.
- **Impacto demostrado:** un usuario remoto sin credenciales válidas accedió al dashboard RRHH bajo la identidad presentada como `admin`.
- **Severidad:** Alta — CVSS v3.1: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` (7.5). La explotación fue remota, sin privilegios ni interacción, y el resultado demostrado fue acceso no autorizado a un área administrativa. No se afirma modificación, disponibilidad afectada ni acceso a datos de clientes en este hito.
- **Remediación:** reemplazar toda construcción dinámica de consultas de autenticación por consultas parametrizadas/prepared statements; validar el flujo de autenticación con comparaciones de credenciales seguras y permisos del lado servidor. Aplicar cuentas de base de datos con privilegios mínimos y registrar/rechazar sintaxis anómala como control complementario. Verificar la corrección repitiendo ambas solicitudes: la solicitud booleana debe devolver el mismo rechazo que las credenciales inválidas, sin crear sesión.
- **Limitación:** no se ejecutaron consultas de enumeración, extracción de tablas, modificación de datos ni acciones fuera del portal. El hecho de que la respuesta muestre `admin` no prueba por sí solo persistencia, control total del host ni acceso a los datos de clientes.

## Traspaso P2 → P3

El acceso se reproduce con la segunda solicitud anterior. Tras el bypass, la respuesta indica el recurso `/backup/rrhh.conf`. Esa referencia, obtenida desde el acceso R2, es el punto de partida mínimo para que P3 investigue el secreto del caso. P2 no solicitó ese recurso ni utilizó ningún secreto posterior.
