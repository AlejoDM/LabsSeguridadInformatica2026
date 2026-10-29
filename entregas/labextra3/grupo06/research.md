# Research — Lab Extra 3: Defendé PhantomCorp

**Grupo:** 06
**Fecha:** 2026-10-29
**Opción elegida:** A — Guías reales de hardening web

**Declaración de uso de IA:** (pendiente de completar por el grupo antes de entregar — ver indicación aparte)

## 1. Qué defensas del laboratorio aparecen en guías públicas, y con qué nombre

Las cinco defensas corregidas en `objetivo/server.py` tienen un equivalente directo en guías públicas de OWASP:

- **D4 (SQLi en `/login`):** la *SQL Injection Prevention Cheat Sheet* de OWASP ubica las **consultas parametrizadas / prepared statements con variables enlazadas** como su primera defensa primaria, por delante de procedimientos almacenados, validación por allowlist y escape de caracteres. Es exactamente el cambio aplicado en el parche: pasar de concatenar `user`/`pass` dentro del texto SQL a `db.execute("... WHERE user = ? AND password = ?", (user, pwd))`, donde el motor mantiene separados el código SQL y los datos sin importar qué contenga la entrada.
- **D1 (banner `Server`):** el *OWASP Secure Headers Project* recomienda eliminar o reemplazar por un valor genérico los encabezados que delatan producto y versión del servidor, como `Server`. En la guía esto se trata como reducción de *fingerprinting*, no como una vulnerabilidad explotable en sí misma.
- **D2 (`/api/status` con `debug:true`, rutas y PID) y D3 (backup sin autorización, anunciado en `robots.txt`):** ambas caen dentro de **A05:2021 — Security Misconfiguration** del OWASP Top 10, que define como síntoma típico dejar habilitadas funciones o cuentas innecesarias y mensajes de error/diagnóstico verbosos que no deberían llegar a producción; y dentro de **A01:2021 — Broken Access Control** en la parte de D3 referida a exponer un recurso sin control de autorización efectivo, more allá de que `robots.txt` lo anuncie o no.
- **D5 (path traversal en `/descargar`):** no tiene una cheat sheet dedicada tan citada como la de SQLi, pero la misma familia de causa raíz —construir una ruta de archivo a partir de entrada del usuario sin validar el destino resuelto— es la que describe A01:2021 como control de acceso roto sobre rutas de archivos, y es consistente con la corrección aplicada: resolver la ruta final (`os.path.realpath`) y verificar que quede dentro del directorio permitido, en vez de filtrar la cadena literal `..`.

## 2. Un control que las guías recomiendan y el laboratorio no cubre

Las guías de OWASP insisten en un control que **D1 no implementa por completo**: no alcanza con quitar el valor de `Server`, sino que conviene, además, **no revelar la pila tecnológica por otros canales** (mensajes de error por defecto, cabeceras adicionales como `X-Powered-By`, o páginas de error con traceback). El parche de D1 solo actúa sobre el header `Server`; el propio código del laboratorio (`BaseHTTPRequestHandler`) agrega otros encabezados por defecto que no se tocaron.

Con la biblioteca estándar, sin frameworks, esto se podría reforzar en `server.py`:

```python
class Handler(BaseHTTPRequestHandler):
    server_version = ""   # ya aplicado en D1
    sys_version = ""       # ya aplicado en D1: elimina "Python/3.x" del header Server

    def log_message(self, *a):
        pass  # ya presente: evita que errores internos impriman detalles en consola/stdout
```

Un control adicional, no cubierto por ninguna de las cinco defensas, sería envolver todo `do_GET` en un manejador de excepciones genérico que, ante cualquier error no previsto, devuelva un `500` con un cuerpo fijo (`"Error interno"`) en vez de dejar que una excepción no capturada propague un traceback de Python al cliente (comportamiento por defecto de `http.server` en modo debug). Ninguna de las D1–D5 prueba ese camino porque ninguna de las entradas de ataque provistas llega a disparar una excepción no manejada, pero es exactamente el tipo de "mensaje de error verbose" que A05:2021 señala como síntoma de mala configuración.

## 3. Defense in depth aplicado a D3

"Defensa en profundidad" significa no depender de un único control para proteger un recurso, sino superponer varias capas independientes, de modo que si una falla las demás sigan conteniendo el riesgo. D3 es el ejemplo más claro del laboratorio porque el código original fallaba en la única capa que tenía: ocultar la ruta en `robots.txt` (que ni siquiera es un control de seguridad, solo una preferencia para rastreadores) y nada más, por lo que `/backup` respondía `200` a cualquiera que la pidiera directamente.

El parche de D3 aplica dos capas, no una: deja de anunciar la ruta en `robots.txt` (reduce descubrimiento casual) **y** hace que `/backup` responda `404` sin importar si alguien la conoce o no (el control real). Una defensa en profundidad más completa agregaría una tercera capa independiente de la aplicación —por ejemplo, que el recurso de backup ni siquiera resida bajo el directorio que el servidor HTTP puede leer o servir— para que, aunque un futuro cambio de código reintroduzca el endpoint por error, el archivo ya no esté alcanzable desde ese proceso. Ninguna capa aislada (ocultar la ruta, bloquear la respuesta, o mover el archivo) sustituye a las otras: la combinación es lo que reduce el riesgo de que un solo error de configuración vuelva a exponer el recurso.

## 4. Pregunta de cierre — el verificador del lab frente a un escáner real (Nessus, OpenVAS, nuclei)

El `verificar-defensa.py` de este laboratorio y un escáner de vulnerabilidades real comparten el mismo principio: automatizan un conjunto de **ataques conocidos** contra la aplicación y reportan si la respuesta observada coincide con el patrón de "vulnerable" o con el de "corregido" (en el caso del verificador, literalmente invierte esa lógica: marca verde cuando el ataque *falla*). Nessus, OpenVAS y nuclei funcionan de manera equivalente: lanzan firmas/plantillas de ataques y vulnerabilidades conocidas (CVEs, configuraciones inseguras típicas, versiones de software vulnerables) y comparan la respuesta contra condiciones esperadas.

Lo que un escaneo automático de este tipo **puede** demostrar es exactamente lo que este laboratorio demostró para D5: que un payload concreto, conocido de antemano, ya no produce el resultado vulnerable esperado bajo las condiciones exactas de la prueba (puerto, timing, entorno de red).

Lo que **no** puede demostrar, y que este mismo laboratorio evidenció en carne propia:

1. **Un "verde" puede ser un falso positivo del entorno, no de la defensa.** El propio verificador, corriendo en Windows, marcó D5 como "bloqueada" en corridas donde en realidad la conexión al servidor de prueba había fallado (`connection refused`), y antes del parche había marcado D5 como "bloqueada" simplemente porque `/etc/passwd` no existe en ese sistema operativo —ninguno de los dos resultados decía nada sobre si la ruta estaba realmente confinada—. Un escáner automático tiene el mismo problema: una respuesta inesperada del entorno (timeout, proxy, balanceador, WAF) puede leerse como "no vulnerable" sin que el control real exista.
2. **Un escaneo solo cubre los patrones que conoce.** El verificador prueba cinco ataques puntuales y predefinidos; no agota variantes de encoding, de payload, ni la superficie completa de la aplicación. Un escáner real tiene el mismo límite estructural: detecta lo que sus firmas/plantillas contemplan, no cualquier debilidad posible del código.
3. **No reemplaza entender ni demostrar el mecanismo de la corrección.** Una salida "5/5" certifica que cinco pruebas puntuales pasaron, no que el código sea estructuralmente correcto; es la misma razón por la que este informe exige, además del resultado del verificador, el diff del parche y una prueba de regresión funcional explicada —igual que una auditoría de seguridad real no se conforma con "el escáner no encontró nada" como única evidencia de que una aplicación es segura.

## 5. Fuentes

1. OWASP Cheat Sheet Series. *SQL Injection Prevention Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
2. OWASP. *Secure Headers Project*. https://owasp.org/www-project-secure-headers-project/
3. OWASP. *A05:2021 – Security Misconfiguration* (OWASP Top 10 2021). https://owasp.org/Top10/2021/A05_2021-Security_Misconfiguration/
4. OWASP. *A01:2021 – Broken Access Control* (OWASP Top 10 2021, introducción y ranking). https://owasp.org/Top10/2021/0x00_2021-introduction/
