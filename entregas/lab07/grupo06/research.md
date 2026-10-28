# Mini-research — Laboratorio 07

**Grupo:** 06 · **Tema A:** consultas parametrizadas / prepared statements.
**Fecha:** 2026-10-23 · **Responsabilidad:** P4.

## Desarrollo

La SQL Injection ocurre cuando una aplicación incorpora datos controlados por el usuario directamente en la estructura de una sentencia SQL. Las consultas parametrizadas previenen este problema porque mantienen fija la instrucción y transmiten los valores por separado. En Python, el módulo `sqlite3` permite utilizar marcadores `?` y proporcionar los valores mediante una tupla [1]. SQLite documenta cómo se enlazan estos parámetros [2], mientras que OWASP recomienda esta técnica como una de las principales defensas contra SQL Injection [3].

Este ejemplo defensivo reproduce el enlace de parámetros en una base creada en RAM. Los nombres y claves son ficticios; no son cuentas del laboratorio. No se ejecuta una consulta vulnerable ni se envían requests a otro reto.

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE usuarios (nombre TEXT, clave TEXT)")
con.execute("INSERT INTO usuarios VALUES (?, ?)", ("admin", "clave-ficticia"))
sql = "SELECT nombre FROM usuarios WHERE nombre = ? AND clave = ?"
casos = [("admin", "clave-ficticia"), ("admin", "incorrecta"), ("admin' --", "incorrecta")]
for nombre, clave in casos:
    filas = con.execute(sql, (nombre, clave)).fetchall()
    print(repr(nombre), repr(clave), "=>", filas)
    assert bool(filas) == (nombre == "admin" and clave == "clave-ficticia")
con.close()
print("OK: el texto con comilla y comentario se trata como un valor literal.")

```

El ejemplo utiliza una base de datos SQLite en memoria y contempla tres casos: credenciales válidas, contraseña incorrecta y un nombre de usuario que contiene caracteres utilizados habitualmente en SQL Injection. El programa está diseñado para demostrar que la entrada maliciosa se interpreta como un valor literal y no modifica la estructura de la consulta. Su ejecución puede reproducirse con Python y no requiere conectarse al servidor de PhantomCorp.

La propiedad importante es la separación entre sintaxis y valores, no una sustitución textual manual. Por ello una llamada a `execute` con un SQL previamente concatenado sigue siendo insegura. Los marcadores no reemplazan nombres de tabla, columnas ni palabras clave: cualquier selección dinámica de esos elementos requiere alternativas predefinidas. Tampoco resuelven autorización, traversal o almacenamiento de contraseñas. En una aplicación real corresponde verificar hashes de contraseñas; el ejemplo usa texto ficticio solo para mostrar el filtro.

## Fuentes

1. Python Software Foundation. *sqlite3 — DB-API 2.0 interface for SQLite databases*. Documentación oficial de Python 3.12. https://docs.python.org/3.12/library/sqlite3.html
2. SQLite. *SQL Language Expressions*, apartado 4: Parameters. https://www.sqlite.org/lang_expr.html#varparam
3. OWASP Foundation. *SQL Injection Prevention Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html

## Reflexión

El ejemplo de SQLite permite comprender cómo las consultas parametrizadas evitan que los datos ingresados por un usuario modifiquen las instrucciones SQL. La principal enseñanza es que la seguridad no depende únicamente de filtrar caracteres peligrosos, sino de separar correctamente los datos del código. En una aplicación real, utilizaríamos consultas parametrizadas en todos los accesos a la base de datos y revisaríamos cualquier sentencia construida dinámicamente. Este mecanismo previene SQL Injection a través de los valores parametrizados, aunque debe complementarse con otros controles de seguridad, como la autorización y la protección de contraseñas.

## Declaración de IA

Codex (OpenAI) asistió en la investigación local, redacción y demostración. La verificación consistió en la lectura de las fuentes citadas y en la ejecución del ejemplo incluido, replicable localmente con Python y SQLite sin conexión a ninguna red. El responsable de la sección (P4) revisó las fuentes, comprobó que cada cita respalda la afirmación asociada y ejecutó el código de ejemplo antes de incorporarlo; la reflexión final fue revisada y apropiada por el autor responsable de esta sección.
