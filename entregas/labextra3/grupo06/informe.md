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

**Herramienta:** Codex (OpenAI).

- **Finalidad del uso:** apoyo para la redacción del informe.

**Herramienta:** ChatGPT (OpenAI), aporte de Persona 2.

- **Finalidad:** asistencia para comprender y corregir la exposición de `/backup`, preparar pruebas locales y redactar la respuesta P2.
- **Partes asistidas:** parche D3, script `evidencia/probar-d3.py` y respuesta P2.
- **Verificación:** se ejecutaron pruebas HTTP sobre la copia del grupo utilizando una base de datos temporal. Se confirmó que `/backup` devuelve 404, que `robots.txt` no lo anuncia y que la página principal y la descarga legítima del manual siguen respondiendo 200. La validación oficial de D3 sigue pendiente por los errores de ejecución observados en Windows.

## 1. Tabla de defensas (antes → después)

| Defensa | Ataque que funcionaba | Fix aplicado | Verificación |
|---|---|---|---|
| D1 | Banner identifica producto y versión | Pendiente P1 | Verificador sigue marcándola vulnerable |
| D2 | `/api/status` entrega debug, ruta y PID | Pendiente P1 | Sigue vulnerable |
| D3 |aprobada por el verificador oficial; flag aceptada mediante normalización temporal de CRLF. Evidencias: d3-verificador.txt y d3-submit-compatibilidad.txt.
| D4 | `admin'--` en usuario y `' OR 1=1 --` en contraseña permiten entrar sin credenciales válidas | Consulta fija con `?` y tupla `(user, pwd)`; `evidencia/salidas/d4-parche.diff` | Ambos ataques bloqueados por el verificador; tres variantes devuelven HTTP 401 en pruebas propias |
| D5 | Lectura fuera del directorio mediante `../centinela-p3.txt` | Pendiente P4 | HTTP 200 con contenido del centinela: sigue vulnerable, pese al verde del verificador Windows |

### D4: explicación del cambio

En `objetivo/server.py`, el bloque de `/login` pasa de construir SQL concatenando entradas a:

```python
cur = db.execute(
    "SELECT user FROM usuarios WHERE user = ? AND password = ?",
    (user, pwd))
```

La sentencia mantiene su estructura; SQLite recibe usuario y contraseña como valores separados. No se filtran apóstrofes ni se reconocen payloads particulares. El diff cambia únicamente el comentario D4 y esa consulta. No se implementaron las defensas de otros responsables.

Evidencias: `d4-antes.txt`, `d4-despues.txt`, `d4-parche.diff`, `verificador-inicial.txt` y `verificador-despues-p3.txt` dentro de `evidencia/salidas/`.

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

## 4. Preguntas P1–P5

Preguntas P1, P3 y P5: pendientes de sus responsables según el plan.

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

## 5. Conclusión
