# Informe de Penetration Test — PhantomCorp «Clientes»

**Grupo:** 06
**Fecha:** 2026-10-28
**Cliente:** PhantomCorp S.A. · **Tipo:** Caja negra · **Alcance:** host `phantomcorp` del laboratorio

| Nombre y apellido | Usuario de GitHub |
|---|---|
| Martín Beccereca | martinbeccereca |
| Belén Benito | belubenito603 |
| Alejo José De Miguel | AlejoDM |
| Tomás Giudici | TomasGiudici |
| Carolina Suppo | carosuppo |

## 0. Declaración de uso de IA

**Herramienta:** Codex (OpenAI).

- **Finalidad y partes asistidas:** apoyo en ejecución de reconocimiento R1, registro de evidencias y redacción de metodología.
- **Verificación:** respuestas HTTP y flag contrastadas manualmente.

## 1. Resumen ejecutivo

## 2. Alcance y metodología

Se evaluó únicamente el servicio HTTP de `phantomcorp` del integrador desde `cyberlab-attacker`, conectado a `cyberlab_labnet`. Se inició el entorno oficial con Docker Compose, equivalente a `make lab N=final`, sin modificar el target ni consultar su código, soluciones o manifiesto para descubrir rutas o flags. Las solicitudes de P1 ocurrieron el 28/10/2026 entre 17:10:20 y 17:10:31 UTC (14:10:20–14:10:31 en Argentina), según las cabeceras del servidor.

El trabajo de P1 se limitó a reconocimiento y enumeración dirigida: página inicial, robots.txt, ruta anunciada y una ruta inexistente de control. Las cuatro solicitudes fueron GET, con tiempo máximo de diez segundos. No se enviaron credenciales, payloads de explotación ni solicitudes de modificación. No se escanearon otros hosts, no se realizaron acciones destructivas ni se intentó denegación de servicio. La ventana autorizada es la fijada por la cátedra; no consta un horario adicional en los materiales revisados.

| Recurso observado | Resultado | Evidencia |
|---|---|---|
| `http://phantomcorp/` | 200, portal público sin enlaces visibles | `evidencia/salidas/p1-inicio.txt` |
| `/robots.txt` | 200; anuncia `/portal-rrhh` | `evidencia/salidas/p1-robots.txt` |
| `/portal-rrhh` | 200; portal interno y formulario | `evidencia/salidas/p1-r1-portal.txt` |
| `/p1-control-inexistente` | 404, Not Found | `evidencia/salidas/p1-control.txt` |

Las cabeceras declaran `PhantomClientes/2.0`; esto es un banner observado, no una identificación independiente del software instalado. La comparación con el 404 respalda que el portal no es simplemente una respuesta genérica para cualquier ruta. No se pretende un inventario exhaustivo de servicios.

## 3. Narrativa del ataque

### Aporte P1 — Reconocimiento y enumeración

La página inicial respondió con el portal público, sin enlaces al portal interno. Se consultó `robots.txt` como recurso habitual de enumeración: su línea `Disallow: /portal-rrhh` proporcionó una ruta concreta. Al solicitarla directamente, el servidor devolvió el título «Portal RRHH PhantomCorp», un formulario POST hacia `/portal/login`, los campos `user` y `pass`, y la flag `FLAG{final_recon_portal}` en un comentario HTML. Se detuvo la investigación en R1 para entregar a P2 la superficie de autenticación observada.

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
  
### Observación P1 — Portal interno descubrible mediante robots.txt

- **Ubicación:** `/robots.txt` y `/portal-rrhh`.
- **Descripción:** un recurso público anuncia la ruta de un portal interno no enlazado desde la portada observada. El acceso no autenticado permite visualizar su formulario.
- **Evidencia:** respuestas completas en `p1-robots.txt` y `p1-r1-portal.txt`.
- **Impacto demostrado:** descubrimiento de la superficie de autenticación y de sus parámetros. No se demostró acceso a sesiones, secretos ni datos de clientes.
- **Clasificación:** observación informativa; sin CVSS asignado. Encontrar una página de login no demuestra por sí solo una vulnerabilidad explotable ni permite justificar un score.
- **Recomendación:** no tratar robots.txt ni una URL poco visible como control de acceso. Revisar si el portal debe ser accesible desde esta red y aplicar restricciones y autorización efectivas según su finalidad. Retirar referencias innecesarias reduce pistas, pero no sustituye esos controles. P2 deberá verificar el mecanismo de autenticación antes de diagnosticar una falla concreta.

## 5. Conclusión

## 6. Anexo

- Bitácora: `evidencia/comandos.txt`.
- Salidas HTTP y validación: `evidencia/salidas/`.
- Estado comprobado: `evidencia/salidas/status-final.txt`, R1 resuelto, 1/4.
- Traspaso reproducible: `evidencia/analisis/p1-recon-metodologia.md`.
- **Incidencia durante la validación de R1:** El primer intento de presentar la flag mediante `./ctf submit final R1` fue rechazado. Se utilizó posteriormente un procedimiento de compatibilidad que leía una copia temporal del manifiesto sin caracteres CRLF, sin modificar el archivo original. Este procedimiento registró R1 como resuelto. Luego, al ejecutar nuevamente el comando oficial `./ctf submit final R1 'FLAG{final_recon_portal}'`, se obtuvo `[ OK ] Correcta (ya la tenías). Reto R1 ✓`. El estado del CTF confirma un progreso de 1/4. Se conservan las salidas del intento fallido y de la validación alternativa como evidencia.
