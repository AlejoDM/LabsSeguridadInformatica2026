# Informe — Laboratorio Extra 4: Cracking de contraseñas

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

- **Finalidad y partes asistidas:** asistencia para generar la implementación de `aplicar_reglas` y sus pruebas, ejecutar comprobaciones sobre el caso, consultar la documentación de NIST y redactar el análisis y las evidencias del informe.
- **Verificación:** Revisión del código y reproducción manual de las pruebas.

**Herramienta:** ChatGPT (OpenAI), aporte de Persona 2.

- **Finalidad:** asistencia para implementar las funciones `cargar_sombra()` y `crackear()`, preparar las pruebas aisladas y redactar la respuesta P2 sobre el salt.
- **Partes asistidas:** implementación de las dos funciones, script `evidencia/probar-p2.py`, documentación de P2 y registro de pruebas.
- **Verificación:** se comprobó que el archivo de hashes contiene cuatro registros, que `cracker.py` compila correctamente y que el ataque de diccionario encuentra una contraseña ficticia en una prueba aislada. La ejecución integrada de R2 sigue pendiente de la implementación de `hash_de()` por Persona 1.

## 1. Tabla de resultados

| Usuario | Algoritmo | ¿Cayó? | Técnica | Contraseña del caso | Tiempo |
|---|---|---|---|---|---|
| admin | sha256 | Sí, en prueba aislada de reglas; falta CLI integrada | palabra + año | `phantom2026` | 0,000337 s, 95 intentos en esta ejecución aislada |

### Implementación de P2

Se completaron las funciones `cargar_sombra()` y `crackear()` en `cracker.py`.

La función `cargar_sombra()` lee el archivo de hashes, ignora las líneas vacías y los comentarios, y devuelve una lista de tuplas con usuario, algoritmo, salt y hash. Se verificó que el archivo proporcionado por la cátedra contiene cuatro registros: operador, analista, admin y root.

La función `crackear()` recorre las palabras de un diccionario y compara sus hashes con los registros pendientes. Cuando se habilita `con_reglas`, utiliza las variantes generadas por `aplicar_reglas()`. Devuelve un diccionario con las contraseñas encontradas. En la ejecución general se omite PBKDF2 para evitar pruebas masivas de alto costo; su medición se realiza por separado.

Se comprobó la compilación con `py -3 -m py_compile` y se ejecutó una prueba aislada con un usuario ficticio, un hash SHA-256 con salt y un diccionario temporal. La prueba encontró correctamente la contraseña esperada.

**Resultado:** `PRUEBA P2 SUPERADA`.

**Evidencia:** `evidencia/probar-p2.py` y `evidencia/salidas/p2-prueba-aislada.txt`.

La prueba aislada utiliza una implementación temporal de hash dentro del script de prueba, sin alterar `hash_de()` de Persona 1. Queda pendiente ejecutar el cracker completo y documentar R2 cuando se integre esa función.

### Implementación de P3

`aplicar_reglas(palabra)` devuelve una lista de candidatos en orden estable. Combina la palabra original, capitalización inicial, minúsculas y mayúsculas con los sufijos vacíos, 2024–2026 y 1/12/123, tal como propone el contrato del esqueleto. Deduplica conservando el primer orden de aparición: máximo 28 variantes por entrada. No incluye nombres de usuarios, contraseñas completas ni flags del caso. Los años son un rango explícito de la consigna, no dependen del reloj.

Pruebas con `luna`, `LuNa`, cadena vacía, números y Unicode confirman lista de strings, original primero, ausencia de duplicados, repetibilidad y combinaciones de capitalización/sufijos. `capitalize()` normaliza a minúsculas el resto; la variante original también se conserva. La función no elimina espacios de la entrada; el tratamiento de líneas del diccionario corresponde a P2.

### Alcance de la prueba de R3

Como `hash_de`, `cargar_sombra` y `crackear` aún no están implementadas por P1/P2, se adjunta `evidencia/probar-p3.py`: prueba aislada que importa la función del cracker y compara sus candidatos con SHA-256(salt_bytes + password_bytes) usando hashlib. Recibe las rutas y el usuario por argumentos, se limita al caso SHA-256 y no intenta PBKDF2. No sustituye las implementaciones de P1/P2 ni la integración de P5.

Sobre las 49 palabras del diccionario puro no hubo coincidencia. Con las reglas se encontró `phantom2026`, derivada de `phantom`, en el intento 95. La contraseña no se obtuvo del generador ni de soluciones. Se confirmó el loot con el subcomando oficial `descifrar` de la copia. La ejecución `crackear ... --reglas` todavía falla en `cargar_sombra`, y su error se conserva en `cli-pendiente-integracion.txt`. **No se presenta la prueba aislada como ejecución exitosa del cracker integrado.**

## 2. Medición de velocidad (P1)


## 3. El loot

Salida real del CLI, también conservada en `evidencia/salidas/loot-admin.txt`:

```text
Notas de admin — CONFIDENCIAL
==========================
Recuperaste esto porque la contraseña era débil.
Evidencia: FLAG{crack_reglas_mangling}
```

Demuestra acceso al texto cifrado del ejercicio con la contraseña recuperada. En una empresa, la reutilización de una contraseña como clave de cifrado podría extender el impacto de una filtración de hashes a documentos protegidos con ella. Este caso no demuestra acceso a cuentas o servicios reales; su XOR repetido es un mecanismo educativo.

## 4. Las flags

R3 se presentó después de obtenerla del loot. El primer envío fue rechazado por el formato CRLF del manifiesto. `evidencia/validar-r3-crlf.sh` reutiliza las funciones oficiales con una copia temporal normalizada, sin editar motor ni manifiesto ni escribir el progreso a mano. La salida de aceptación y el estado oficial muestran **R3 resuelto, 1/3**. La flag aceptada no elimina la necesidad de repetir R3 con el CLI integrado.

## 5. Preguntas P1–P5

### P2 — ¿Para qué sirve el salt y por qué no impide ataques de diccionario?

El *salt* es un valor aleatorio que se incorpora al proceso de generación del hash de una contraseña. Su finalidad es evitar que dos usuarios con la misma contraseña tengan necesariamente el mismo hash y dificultar el uso de tablas precalculadas, como las *rainbow tables*.

Al utilizar un salt diferente para cada usuario, es necesario calcular los candidatos para cada registro, en lugar de reutilizar directamente los mismos hashes.

Sin embargo, el salt no impide un ataque de diccionario. Si una contraseña es común o predecible y aparece entre los candidatos, se puede calcular su hash utilizando el salt correspondiente y compararlo con el hash almacenado.

En este laboratorio trabajamos con hashes MD5 y SHA-256 que incorporan salt. Esto permite comprobar que el salt no reemplaza la necesidad de utilizar contraseñas difíciles de adivinar ni algoritmos de derivación costosos, como PBKDF2.

**En conclusión**, el salt dificulta los ataques basados en tablas precalculadas y evita que hashes iguales revelen directamente contraseñas compartidas, pero no impide probar contraseñas mediante un diccionario.

### P3 — Complejidad predecible y NIST

Una política que cuenta caracteres de distintas clases no mide cuán fácil es adivinar la elección humana. Nuestro generador no exploró todas las cadenas posibles: probó unas pocas transformaciones previsibles de palabras conocidas. Agregar el año produce candidatos baratos de enumerar.

**Discrepancia del enunciado:** la contraseña observada es `phantom2026` (11 caracteres, minúsculas y dígitos, sin mayúsculas). Por eso no cumple literalmente la condición de mayúsculas que afirma la pregunta. No se modifica el resultado para ajustarlo al relato. La debilidad conceptual permanece: una variante con inicial mayúscula también está cubierta por las reglas, aunque no es la contraseña recuperada.

Según NIST SP 800-63B-4, sección 3.1.1.2, la longitud mínima es 15 caracteres para contraseñas usadas como único factor; pueden admitirse ocho cuando forman parte de MFA. Se recomienda permitir al menos 64 como longitud máxima admitida. No se deben imponer mezclas obligatorias de tipos de caracteres ni cambios periódicos sin indicios de compromiso. Debe contrastarse la contraseña completa con una lista de valores comunes, esperables o comprometidos. [Fuente oficial, consultada el 28/10/2026](https://pages.nist.gov/800-63-4/sp800-63b.html#passwordver).

Para el caso, una longitud mayor y evitar elecciones previsibles es más útil que añadir mecánicamente una mayúscula y un año. La limitación de intentos en el login protege frente a intentos online, pero no detiene este ataque offline contra una copia de hashes; el almacenamiento con salt y derivación costosa aborda ese segundo escenario. No debe interpretarse que una regla de longitud garantiza por sí sola resistencia a cualquier ataque.

## 6. Conclusión
