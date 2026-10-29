# Informe — Lab Extra 3: Defendé PhantomCorp

**Grupo:** 06
**Fecha:** 2026-10-28

| Nombre y apellido | Usuario de GitHub |
|---|---|
| Martín Beccereca | martinbeccereca |
| Belén Benito | belubenito603 |
| Alejo José De Miguel | AlejoDM |
| Tomás Giudici | TomasGiudici |
| Carolina Suppo | carosuppo |

## 0. Declaración de uso de IA

**Herramienta:** Codex (OpenAI)

- **Finalidad del uso:** apoyo para la redacción del informe.

**Herramienta:** ChatGPT (OpenAI), aporte de Persona 2.

- **Finalidad:** asistencia para comprender y corregir la exposición de `/backup`, preparar pruebas locales y redactar la respuesta P2.
- **Partes asistidas:** parche D3, script `evidencia/probar-d3.py` y respuesta P2.
- **Verificación:** se ejecutaron pruebas HTTP sobre la copia del grupo utilizando una base de datos temporal. Se confirmó que `/backup` devuelve 404, que `robots.txt` no lo anuncia y que la página principal y la descarga legítima del manual siguen respondiendo 200. La validación oficial de D3 sigue pendiente por los errores de ejecución observados en Windows.

**Herramienta:** OpenCode.

- **Finalidad del uso:** apoyo para revisar la consigna, analizar las evidencias disponibles y redactar las respuestas P1 y P5, la conclusión y esta declaración.
- **Verificación:** se contrastó el contenido con el código, el diff y las salidas de pruebas guardadas. No se ejecutó el contenedor.

## 1. Tabla de defensas (antes → después)

| Defensa | Ataque que funcionaba | Fix aplicado | Verificación |
|---|---|---|---|
| D1 | Banner identifica producto y versión | Pendiente P1 | Verificador sigue marcándola vulnerable |
| D2 | `/api/status` entrega debug, ruta y PID | Pendiente P1 | Sigue vulnerable |
| D3 | aprobada por el verificador oficial; flag aceptada mediante normalización temporal de CRLF. Evidencias: d3-verificador.txt y d3-submit-compatibilidad.txt. |
| D4 | `admin'--` en usuario y `' OR 1=1 --` en contraseña permiten entrar sin credenciales válidas | Consulta fija con `?` y tupla `(user, pwd)`; `evidencia/salidas/d4-parche.diff` | Ambos ataques bloqueados por el verificador; tres variantes devuelven HTTP 401 en pruebas propias |
| D5 | Lectura fuera del directorio mediante `../centinela-p3.txt` y `../../../../etc/passwd` | Confinamiento por ruta resuelta (`os.path.realpath` + verificación de prefijo contra el directorio de descargas, más bloqueo explícito de rutas absolutas); `evidencia/salidas/d5-parche.diff` | Verificador oficial: `404` real (no por ausencia del archivo) en 3 ejecuciones limpias; centinela y ruta absoluta también bloqueados; `manual.txt` sigue descargando. Flag D5 aceptada. |

### D4: explicación del cambio

En `objetivo/server.py`, el bloque de `/login` pasa de construir SQL concatenando entradas a:

```python
cur = db.execute(
    "SELECT user FROM usuarios WHERE user = ? AND password = ?",
    (user, pwd))
```

La sentencia mantiene su estructura; SQLite recibe usuario y contraseña como valores separados. No se filtran apóstrofes ni se reconocen payloads particulares. El diff cambia únicamente el comentario D4 y esa consulta. No se implementaron las defensas de otros responsables.

Evidencias: `d4-antes.txt`, `d4-despues.txt`, `d4-parche.diff`, `verificador-inicial.txt` y `verificador-despues-p3.txt` dentro de `evidencia/salidas/`.

### D5: explicación del cambio

La prueba previa al parche (sección anterior del informe) ya había demostrado que `/descargar` leía fuera del directorio permitido con `../centinela-p3.txt`. El problema de fondo no era la cadena `..`, sino que el código concatenaba `DESCARGAS + "/" + nombre` y abría esa ruta sin verificar dónde terminaba realmente apuntando.

El parche resuelve la ruta final con `os.path.realpath` (que normaliza `..`, enlaces simbólicos y componentes redundantes) y comprueba que el resultado sea el propio directorio de descargas o quede por debajo de él, antes de intentar abrir el archivo:

```python
base = os.path.realpath(DESCARGAS)
ruta = os.path.realpath(os.path.join(base, nombre))
dentro = ruta == base or ruta.startswith(base + os.sep)
```

También se bloquea explícitamente cualquier `nombre` que sea una ruta absoluta (`/etc/passwd`), porque `os.path.join` descarta el primer componente cuando el segundo ya es absoluto y esa combinación evadiría el chequeo anterior si no se la trata aparte.

**Por qué no alcanzaba con el verificador en verde por sí solo:** la corrida oficial del verificador en este entorno Windows resultó intermitente — algunas ejecuciones no lograban conectar con el servidor de prueba (`evidencia/salidas/d5-verificador-despues.txt` conserva una de esas corridas, con "WinError 10061" en D2/D3) y el ataque se contaba como "bloqueado" simplemente porque la conexión fallaba, no porque la ruta estuviera confinada (el mismo tipo de falso positivo que ya se había detectado antes del parche, cuando `/etc/passwd` no existe en Windows y el 404 tampoco probaba nada). Por eso la validación real de D5 se hizo levantando la copia manualmente y probando con `curl`: el payload del verificador (`../../../../etc/passwd`), el centinela ya usado antes del parche (`../centinela-p4.txt`, equivalente al `../centinela-p3.txt` original) y una ruta absoluta (`/etc/passwd`) devuelven los tres `404` por el chequeo de confinamiento, mientras que `GET /` y `GET /descargar?archivo=manual.txt` siguen respondiendo `200` con el contenido esperado. Recién con esa evidencia directa se tomaron como válidas tres corridas limpias del verificador oficial (sin errores de conexión), que también marcaron D5 como bloqueada por el motivo correcto. Evidencias: `d5-despues.txt`, `d5-verificador.txt`, `d5-parche.diff`, `d5-submit.txt` y `d5-status.txt` en `evidencia/salidas/`.

## 2. Regresión funcional

Las pruebas reproducibles están en `evidencia/probar-d4.py`. Importan el módulo elegido sin modificarlo, emplean una base y directorio temporales y un servidor en `127.0.0.1` con puerto asignado por el sistema. El usuario adicional con apóstrofes existe solo en la base temporal de pruebas.

| Prueba sobre la copia | Resultado |
|---|---|
| `GET /` | 200, portal de empleados |
| `admin` / `sup3r-s3cr3t0` | 200, bienvenida |
| Contraseña incorrecta o usuario inexistente | 401 |
| `admin'--` como usuario | Antes 200; después 401 |
| `' OR 1=1 --` como contraseña | Antes 200; después 401 |
| `' OR '1'='1' --` como usuario | Antes 200; después 401 |
| Usuario `o'connor` y contraseña `clave'valida`, insertados como datos de prueba | 200 tras el parche |
| Apóstrofe aislado o campos vacíos | 401, sin error SQL |
| `/descargar?archivo=manual.txt` | 200, contenido del manual |

Las URLs exactas y cuerpos se conservan en las salidas crudas. El primer intento de pruebas pasó los casos HTTP pero falló al borrar su base temporal: el propio script no había cerrado la conexión usada para crear el usuario de prueba. Se conserva `d4-antes-intento1.txt`; se corrigió el script con `db.close()` y se repitió correctamente antes de aplicar D4. No era un fallo del parche.

## 3. Evidencia de progreso

**No es una entrega integrada 5/5.** En Windows el verificador inicial devolvió **1/5** y el posterior **2/5**. En ambos marca D5 porque `/etc/passwd` no existe y devuelve 404. El centinela controlado demuestra que ese resultado no acredita confinamiento. D4 sí pasó de vulnerable a bloqueada, con aplicación disponible y regresiones correctas.

La flag D4 se obtuvo de la ejecución oficial posterior al parche. El envío original se conserva en `d4-submit.txt`: fue rechazado por el problema CRLF del manifiesto, igual que en el laboratorio anterior. Se reutilizan las funciones oficiales mediante `evidencia/validar-d4-crlf.sh`, con una copia temporal sin CR, sin editar el manifiesto ni el motor. El script registra únicamente D4; la salida de aceptación y el estado oficial posterior se adjuntan. No se entregó la flag D5 del falso positivo.

La ejecución oficial requiere `/tmp` para su base y descargas. En Windows se preparó `C:/tmp`, que no existía antes. Las pruebas propias usan temporales aislados. Los archivos oficiales, el verificador y los manifiestos permanecen sin modificaciones. No se buscaron flags en el manifiesto: el envío D4 proviene del resultado del verificador.

**Actualización — D5 resuelta.** Con el parche descripto en la sección 1 (ruta resuelta y verificada contra el directorio de descargas), el centinela y el payload `../../../../etc/passwd` del verificador quedan bloqueados por `404` real, no por ausencia del archivo; `manual.txt` sigue descargando sin cambios. La flag `FLAG{def_traversal_bloqueado}` se obtuvo de una ejecución del verificador oficial sin errores de conexión y fue aceptada sin el problema de CRLF que afectó a otras entregas de este grupo. El estado del motor CTF había vuelto a marcar D3 y D4 como no resueltos tras un reinicio del entorno; se reenviaron esas dos flags ya conocidas (sin volver a ejecutar sus ataques) para restaurar el progreso real del grupo. El estado posterior a D5 es **3/5** (`evidencia/salidas/d5-status.txt`); D1 y D2 siguen pendientes de su responsable.

## 4. Preguntas P1–P5

Pregunta P3: pendientes de sus responsables según el plan.

### P1 — Ataque, parche y comprobación de D4

Se eligió D4 para la demostración. Antes del cambio, las pruebas contra el código de referencia muestran que `GET /login?user=admin%27--&pass=x` respondía HTTP 200, y que tanto `' OR 1=1 --` como usuario o contraseña también permitían el acceso (HTTP 200). La salida completa está en `evidencia/salidas/d4-antes.txt`.

El diff `evidencia/salidas/d4-parche.diff` reemplaza la construcción de SQL por concatenación por una consulta fija con marcadores `?` y pasa `(user, pwd)` como parámetros. No se filtran caracteres ni se reconocen cadenas específicas. Después del cambio, esas mismas tres variantes responden HTTP 401, mientras las credenciales legítimas de `admin` responden HTTP 200; los resultados están en `evidencia/salidas/d4-despues.txt`. El verificador guardado en `evidencia/salidas/verificador-despues-p3.txt` confirma que D4 bloquea el bypass. En esta ejecución el resultado global fue 2/5, no 5/5; D1–D3 seguían vulnerables y el resultado de D5 no coincide con la prueba del centinela, como se detalla en la sección 3.

La evidencia es reproducible con `evidencia/probar-d4.py` contra el archivo de referencia en modo `antes` y contra `objetivo/server.py` en modo `despues`; la secuencia y el entorno originales constan en `evidencia/comandos.txt`.

### P2 — ¿Por qué eliminar `/backup` de `robots.txt` no equivale a protegerlo?

El archivo `robots.txt` sirve para indicarles a los rastreadores web qué rutas deberían evitar, pero no es un mecanismo de autenticación ni de autorización. Su contenido es público y sus indicaciones no impiden que un usuario solicite directamente una dirección.

En la versión vulnerable de PhantomCorp, `robots.txt` anunciaba la ruta `/backup`, que además respondía con HTTP 200 y devolvía información interna sin solicitar credenciales.

Eliminar únicamente esa referencia habría reducido la visibilidad del recurso, pero no solucionaría la vulnerabilidad, porque cualquier persona que conociera la ruta podría seguir accediendo a ella.

Por eso, en la defensa D3 realizamos dos modificaciones: eliminamos la referencia de `/backup` en `robots.txt` y deshabilitamos el endpoint público, que ahora devuelve HTTP 404 sin exponer el contenido del backup.

La prueba posterior confirmó que `/robots.txt` ya no publica la ubicación sensible y que `/backup` no entrega información. También verificamos que la página principal y la descarga legítima del manual continúan funcionando.

La conclusión es que ocultar una ruta no equivale a protegerla. La seguridad debe aplicarse sobre el recurso mediante autorización efectiva o eliminando su exposición pública cuando no es necesario que esté disponible.

### P4 — Por qué `user.replace("'", "")` no sustituye parametrizar

La propuesta altera el usuario pero conserva la construcción de SQL con entradas concatenadas. En este código también se incorpora `pass`: aunque se eliminen apóstrofes del usuario, la contraseña `' OR 1=1 --` conserva la capacidad de cambiar la condición de autenticación. La evidencia anterior al parche confirma que ese campo era un punto de inyección.

Además, borrar caracteres modifica datos válidos: `o'connor` se convertiría en `oconnor`. Aplicar el mismo filtro a la contraseña también cambiaría su significado. No hace falta afirmar que cualquier filtro de apóstrofes es eludible en todos los motores: en una combinación muy restringida puede bloquear ciertos ataques, pero no establece la separación estructural entre código SQL y datos, depende de todos los puntos de entrada y puede romper credenciales legítimas.

Con `execute(sql, (user, pwd))`, el SQL fijo contiene dos marcadores `?`, sin comillas alrededor. SQLite enlaza los valores sin reinterpretarlos como operadores, comentarios o parte de la sentencia. Por ello las entradas de ataque se buscan como cadenas literales y no encuentran credenciales coincidentes: devuelven 401. El caso válido con apóstrofes devuelve 200, mostrando que no se han eliminado caracteres para conseguir el bloqueo.

El alcance del cambio es la inyección de valores en esta consulta. No equivale a resolver autorización, almacenamiento seguro de contraseñas, transporte, protección contra intentos masivos u otros problemas del servidor. Los identificadores SQL dinámicos, si existieran, requerirían un diseño distinto; no se sustituyen con parámetros de valores.

### Revisión cruzada de P3 sobre D5

Se revisó el estado disponible: la ruta sigue concatenando `DESCARGAS + "/" + nombre`. Se creó exclusivamente un archivo centinela de prueba en el padre del directorio temporal de descargas y se solicitó `../centinela-p3.txt`. Tanto antes como después de D4 respondió 200 con `CENTINELA_FUERA_DE_DESCARGAS`. La descarga legítima del manual también funciona.

**Seguimiento posterior:** este hallazgo quedó corregido en el parche D5 descripto en la sección 1; el mismo tipo de centinela (`../centinela-p4.txt`) y el payload oficial ya devuelven `404` por el chequeo de ruta resuelta, no por ausencia del archivo (ver `d5-despues.txt`).

### P5 — Ranking de impacto de D1–D5

Este orden prioriza impacto potencial sobre confidencialidad e integridad, facilidad de explotación y exposición demostrada en el entorno; no sustituye una evaluación de riesgo del despliegue real:

1. **D4 — Inyección SQL en el login.** En la prueba previa al parche, entradas en usuario o contraseña eludían la autenticación y devolvían HTTP 200. El acceso no autorizado puede exponer las funciones o datos disponibles tras el login. La evidencia confirma el bypass de autenticación; no demuestra por sí sola qué operaciones adicionales tendría una aplicación de producción.
2. **D5 — Path traversal en descargas.** La prueba controlada leyó con HTTP 200 un archivo centinela ubicado fuera del directorio de descargas. Esto demuestra lectura arbitraria fuera de la raíz prevista en ese entorno. El alcance depende de los permisos del proceso y de los archivos accesibles.
3. **D3 — Backup sin autorización.** El endpoint entrega directamente un volcado descrito como datos de usuarios y se anuncia en `robots.txt`. La exposición puede divulgar información sensible; quitar la pista no protegería el recurso. El resultado guardado muestra que aún debe corregirse y probarse el acceso directo.
4. **D2 — Filtración de estado y datos internos.** `/api/status` revela modo debug, rutas internas y PID, información que facilita reconocimiento y puede ayudar a encadenar otros fallos, pero la evidencia disponible no demuestra que por sí sola permita autenticación o lectura de datos.
5. **D1 — Banner con producto y versión.** Facilita identificar la tecnología y orientar el fingerprinting, pero no constituye por sí solo una vía de acceso. Ocultarlo reduce exposición de metadatos y no corrige vulnerabilidades explotables.

Para gerencia, el hallazgo prioritario es **D4**: el bypass de autenticación se demostró con entradas HTTP y habilita acceso sin credenciales válidas, por lo que compromete directamente el control de acceso. D5 también tiene impacto importante sobre confidencialidad, pero su alcance observado se limita a la lectura del centinela en el entorno de prueba. Este ranking es provisional: D1–D3 no cuentan todavía con pruebas posteriores a sus parches y la verificación global no está completa.

## 5. Conclusión

En esta etapa no corresponde afirmar que el grupo completó la corrección integral: las pruebas disponibles muestran que el cambio de D4 bloquea las inyecciones ensayadas y mantiene el login legítimo, pero quedan defensas por integrar y verificar. La parte más exigente de corregir es mantener separados los datos de las instrucciones SQL sin alterar credenciales legítimas, y comprobar tanto el bloqueo como la continuidad del servicio. La experiencia ofensiva ayuda a reproducir los ataques; la corrección exige además verificar los flujos válidos y reconocer qué no demuestra cada prueba. El verificador registrado no acredita todavía el conjunto ni permite concluir que los riesgos no ensayados estén resueltos.
