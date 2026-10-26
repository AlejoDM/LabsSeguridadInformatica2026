# Informe — Laboratorio 07 · Explotación

**Grupo:** 06
**Fecha:** 2026-10-23

| Nombre y apellido | Usuario de GitHub |
|---|---|
| Martín Beccereca | martinbeccereca |
| Belén Benito | belubenito01 |
| Alejo José De Miguel | AlejoDM |
| Tomás Giudici | TomasGiudici |
| Carolina Suppo | carosuppo |

## 0. Declaración de uso de IA

**Herramientas:** Claude Code y Codex (OpenAI).

- **Finalidad del uso:** apoyo para redactar la estructura inicial del informe, las filas R1/R2 del inventario, P1/P2 y las bitácoras correspondientes.
- **Partes asistidas:** informe, filas R1/R2 de la tabla de explotación, respuestas P1/P2 y comandos de R1/R2.
- **Verificación:** los payloads se enviaron con `curl --data-urlencode` contra el contenedor `phantomcorp` desde la consola atacante; las respuestas HTTP (línea base, bypass y `UNION`) se conservaron sin editar en `evidencia/salidas/`. Las reconstrucciones de consultas SQL son inferencias razonadas a partir de esas respuestas, no una lectura del código del servidor. Se revisó el contenido antes de incorporarlo.

**Herramienta:** ChatGPT.

- **Finalidad del uso:** asistencia en la ejecución guiada del Reto 5, interpretación de respuestas HTTP, validación de la flag y redacción de la documentación.
- **Partes asistidas:** fila R5 de la tabla de explotación, respuesta P5 y registro de comandos.
- **Verificación:** las solicitudes se ejecutaron contra el contenedor autorizado `phantomcorp`. Se compararon las respuestas del perfil propio y del administrador, se conservaron las salidas originales y se confirmó la aceptación de la flag mediante una copia temporal del validador.

## 1. Flags capturadas

*(salida de `./ctf status 07`, pendiente de completar cuando se resuelvan los 5 retos)*

## 2. Tabla de explotación

| Vuln | Payload usado | Consulta/comando/ruta resultante | Impacto | Defensa concreta |
|---|---|---|---|---|
| SQLi auth (R1) | `user=admin' --`, `pass=cualquiercosa` (enviados con `--data-urlencode` a `POST /login`) | Reconstrucción razonada, a partir del comportamiento observado: `SELECT * FROM usuarios WHERE user='admin' --' AND pass='cualquiercosa'`. El `--` comenta todo lo que sigue en la sentencia, por lo que la comparación de `pass` nunca se evalúa. | Demostrado: la respuesta pasó de `401 Credenciales invalidas` (línea base con `user=test`/`pass=test`) a `200 Bienvenido admin (rol: admin)` con la flag `FLAG{sqli_auth_bypass}`, sin conocer la contraseña real de `admin`. No demostrado: no se intentó leer ni modificar otras tablas, ni se probó con otros usuarios. | Usar consultas parametrizadas (prepared statements) para que `user` y `pass` viajen siempre como datos, nunca como parte del texto SQL; además, cuenta de base de datos de mínimo privilegio y mensajes de error no verbosos. Validar el formato del input en el cliente no alcanza: el servidor debe tratar el valor como dato en todos los casos. |
| SQLi UNION (R2) | `q=Router' UNION SELECT * FROM secrets -- `, enviado con `curl -G --data-urlencode` a `GET /buscar`. | Reconstrucción razonada: la consulta original parece devolver dos columnas para una búsqueda. El payload cierra el valor de búsqueda, agrega `UNION SELECT * FROM secrets` y comenta el resto. Los nombres exactos de tablas, columnas y predicado no fueron observados; quedan como inferencia. | Demostrado: la respuesta `200` mostró `flag_union - $FLAG{sqli_union_dump}`. Se leyó al menos una fila de la tabla `secrets` sin autenticación. No demostrado: no se enumeraron otras tablas, no se modificaron datos y no se verificaron permisos adicionales de la cuenta de base. | Usar consultas parametrizadas para toda entrada de búsqueda y mantener la cuenta de base de datos con privilegios mínimos; no exponer errores SQL detallados al cliente. Como controles complementarios, registrar intentos anómalos y aplicar validación de formato, sin reemplazar la parametrización. |
| Command injection (R3) | | | | |
| Path traversal (R4) | `archivo=../flags/lfi.txt`, enviado mediante `curl -G --data-urlencode` a `GET /descargar`. | El servidor parte del directorio `public/`. El segmento `../` permite retroceder un nivel y acceder a `flags/lfi.txt`, fuera del directorio previsto. La resolución de esa ruta es una reconstrucción razonada del comportamiento observado. | Demostrado: el servidor respondió `HTTP 200 OK` y devolvió `FLAG{path_traversal_lfi}`. Se logró leer un archivo fuera del directorio público. No se probaron otros archivos ni permisos adicionales. Evidencias: [línea base](evidencia/salidas/r4-traversal-base.txt) y [prueba de traversal](evidencia/salidas/r4-traversal.txt). | Resolver la ruta canónica y verificar que permanezca dentro del directorio autorizado. Preferir identificadores de archivos o listas blancas en lugar de aceptar rutas arbitrarias proporcionadas por el usuario. |
| IDOR (R5) | `id=1`, enviado mediante `GET /perfil?id=1`. Se utilizó `id=3` como línea base. | El servidor recibió una solicitud del perfil administrativo mediante el parámetro `id`. Al cambiar el identificador de `3` a `1`, devolvió el objeto correspondiente a `admin` sin exigir credenciales adicionales. No se observó una comprobación de autorización que impidiera acceder al perfil ajeno. | Se demostró el acceso a información privada del administrador: el servidor respondió `HTTP 200 OK` y devolvió el perfil `admin`, incluyendo su nota privada y la flag `FLAG{idor_broken_access}`. No se modificaron datos ni se obtuvo una sesión administrativa. Evidencias: [perfil propio](evidencia/salidas/r5-idor-base.txt) y [perfil administrativo](evidencia/salidas/r5-idor-admin.txt). | Implementar controles de autorización por objeto en el servidor. Cada solicitud debe comprobar que el usuario autenticado tiene permisos para acceder al perfil solicitado. Aplicar denegación por defecto y pruebas automatizadas de autorización. |

## 3. Preguntas de análisis
**P1 — por qué funciona el bypass (con la query).**

El login construye, aparentemente, una consulta del estilo `SELECT * FROM usuarios WHERE user='<user>' AND pass='<pass>'`, insertando directamente los valores recibidos del formulario en el texto SQL. Con `user=test` y `pass=test` la respuesta fue `401 Credenciales invalidas`, lo que confirma que, con datos normales, el servidor evalúa ambas condiciones.

Al enviar `user=admin' --` como payload, la consulta reconstruida queda `SELECT * FROM usuarios WHERE user='admin' --' AND pass='cualquiercosa'`. En SQL, `--` inicia un comentario de línea: todo lo que sigue, incluida la comparación `AND pass='cualquiercosa'` y la comilla de cierre que hubiera quedado descolgada, se descarta. La base de datos termina ejecutando, en los hechos, `SELECT * FROM usuarios WHERE user='admin'`, que es verdadera sin importar qué contraseña se haya mandado.

La causa raíz es que el servidor mezcló **datos** (lo que escribió el usuario) con **código** (la sentencia SQL) en el mismo string, sin separar ambos. Por eso el payload no "adivina" la contraseña: la elimina de la ecuación. La respuesta observada (`200 Bienvenido admin (rol: admin)` con la flag) es consistente con esa reconstrucción, aunque el texto exacto de la consulta en el servidor no es visible desde afuera y queda como inferencia razonada, no como hecho confirmado línea por línea.
**P2 — por qué el UNION necesita igual número de columnas.**

`UNION` combina dos conjuntos de resultados en una única tabla lógica. Por eso cada `SELECT` debe aportar la misma cantidad de columnas, en el mismo orden posicional, y con tipos compatibles o convertibles. De lo contrario, el motor SQL no puede decidir qué valor de la segunda consulta corresponde a cada columna de la primera y devuelve un error de aridad o de tipo.

En R2, la consulta base devolvió cada producto en dos campos visibles: nombre y precio. La carga manual `Router' UNION SELECT * FROM secrets -- ` fue aceptada y la respuesta mostró `flag_union - $FLAG{sqli_union_dump}`. Esto demuestra que, en este entorno, la tabla `secrets` aporta una forma compatible de dos columnas para el `UNION`. No se leyó el código ni se observaron los nombres exactos de esas columnas.

Si no se conociera el número de columnas, se puede inferir de forma controlada mediante respuestas y errores: por ejemplo, probar `ORDER BY 1`, `ORDER BY 2`, etc., hasta que un índice deje de ser válido; o intentar `UNION SELECT NULL --`, luego `UNION SELECT NULL,NULL --` y continuar hasta obtener una respuesta compatible. Esas técnicas describen un método posible para otro objetivo; en esta práctica no se ejecutaron, porque el enunciado ya indicaba que el buscador devolvía dos columnas y la evidencia manual con `UNION` fue suficiente.
**P3 — qué sigue después del RCE.**
**P4 — por qué parametrizar mata la SQLi.**

Las consultas parametrizadas previenen SQL Injection porque separan la estructura de la sentencia SQL de los datos ingresados por el usuario. En lugar de construir una consulta concatenando cadenas de texto, se define previamente la instrucción SQL y se proporcionan los valores mediante parámetros.

De esta manera, aunque un usuario introduzca comillas, operadores o instrucciones SQL, la base de datos interpreta esa entrada como un valor y no como parte del código de la consulta.

En los casos R1 y R2 del laboratorio, esto habría impedido que las entradas modificaran la lógica de autenticación o incorporaran una cláusula `UNION` para consultar otra tabla.

Por lo tanto, la parametrización soluciona la causa principal de estas inyecciones: la posibilidad de que los datos del usuario sean interpretados como instrucciones SQL. Validar caracteres o filtrar entradas puede complementar la seguridad, pero no reemplaza las consultas parametrizadas.

**P5 — dónde va el control de acceso (IDOR).**

El control de acceso debe realizarse en el servidor, ya que es el encargado de comprobar si un usuario tiene permiso para acceder a un recurso determinado.

Es importante diferenciar autenticación de autorización. La autenticación permite verificar quién es el usuario, mientras que la autorización determina a qué información o funcionalidades puede acceder.

En el Reto 5 comprobamos que, al modificar el parámetro `id` de `3` a `1`, el servidor devolvió información privada correspondiente al administrador. Esto demuestra que el endpoint no aplicó correctamente una restricción de acceso al objeto solicitado en el contexto de la prueba.

Para evitar esta vulnerabilidad, el backend debe verificar en cada solicitud que el usuario tenga autorización para consultar ese perfil. No alcanza con ocultar botones, bloquear campos o controlar el acceso únicamente desde el frontend, porque las solicitudes HTTP pueden realizarse directamente con herramientas como `curl`.

Como solución, recomendamos implementar verificaciones de permisos del lado servidor, aplicar el principio de denegación por defecto y limitar el acceso de cada usuario a los recursos que realmente le corresponden.

# R4 — Path Traversal

curl -sS -i -G http://phantomcorp/descargar --data-urlencode "archivo=catalogo.txt" | tee /loot/r4-traversal-base.txt
curl -sS -i -G http://phantomcorp/descargar --data-urlencode "archivo=../flags/lfi.txt" | tee /loot/r4-traversal.txt
./ctf submit 07 R4 'FLAG{path_traversal_lfi}'
