# Informe — Laboratorio Extra 4: Cracking de contraseñas

**Grupo:** 06
**Fecha:** 2026-10-29

| Nombre y apellido | Usuario de GitHub |
|---|---|
| Martín Beccereca | martinbeccereca |
| Belén Benito | belubenito603 |
| Alejo José De Miguel | AlejoDM |
| Tomás Giudici | TomasGiudici |
| Carolina Suppo | carosuppo |

## 0. Declaración de uso de IA

**Herramienta:** Codex (OpenAI).

- **Finalidad y partes asistidas:** asistencia para generar la implementación de `aplicar_reglas` y sus pruebas, implementar `hash_de()`, ejecutar comprobaciones sobre el caso, medir tasas locales, consultar la documentación de NIST y redactar el análisis y las evidencias del informe.
- **Verificación:** Revisión del código, reproducción manual de las pruebas y ejecución de `evidencia/medir-p1.py` sobre la copia entregable.

**Herramienta:** ChatGPT (OpenAI).

- **Finalidad:** asistencia para implementar las funciones `cargar_sombra()` y `crackear()`, preparar las pruebas aisladas y redactar el análisis sobre el salt.
- **Partes asistidas:** implementación de las dos funciones, script `evidencia/probar-p2.py`, documentación del análisis sobre el salt y registro de pruebas.
- **Verificación:** se comprobó que el archivo de hashes contiene cuatro registros, que `cracker.py` compila correctamente y que el ataque de diccionario encuentra una contraseña ficticia en una prueba aislada. La ejecución integrada posterior documenta la recuperación de `operador` y `analista`.

**Herramienta:** Opencode.

- **Finalidad y partes asistidas:** apoyo para estructurar la medición controlada de PBKDF2 y redactar su análisis, incluida la estimación condicionada para GPUs.
- **Verificación:** la muestra de 20 candidatos y el cálculo se revisaron personalmente contra `evidencia/salidas/p4-pbkdf2-muestra.txt`. La tasa por GPU se identifica como supuesto y no como benchmark medido.

## Alcance y criterio de evidencia

Las pruebas se limitaron a los artefactos ficticios del laboratorio y a candidatos sintéticos para las mediciones. Se distinguen tres tipos de afirmaciones: resultados observados en salidas conservadas, estimaciones derivadas de tasas locales y escenarios teóricos expresamente identificados. Una prueba aislada de una función no se presenta como sustituto de una ejecución integrada del CLI.

## 1. Tabla de resultados

| Usuario | Algoritmo | ¿Cayó? | Técnica | Contraseña del caso | Tiempo |
|---|---|---|---|---|---|
| operador | md5 | Sí, mediante CLI integrado | diccionario | `riverplate` | No medido en la corrida de recuperación |
| analista | sha256 | Sí, mediante CLI integrado | diccionario | `matecocido` | No medido en la corrida de recuperación |
| admin | sha256 | Sí, en prueba aislada de reglas; falta CLI integrada | palabra + año | `phantom2026` | 0,000337 s, 95 intentos en esta ejecución aislada |
| root | pbkdf2 | No recuperada; control negativo del caso | Muestra de costo acotada, sin búsqueda exhaustiva | — | 13,97 candidatos/s en la muestra independiente |

### Carga de registros y ataque de diccionario

Se completaron las funciones `cargar_sombra()` y `crackear()` en `cracker.py`.

La función `cargar_sombra()` lee el archivo de hashes, ignora las líneas vacías y los comentarios, y devuelve una lista de tuplas con usuario, algoritmo, salt y hash. Se verificó que el archivo proporcionado por la cátedra contiene cuatro registros: operador, analista, admin y root.

La función `crackear()` recorre las palabras de un diccionario y compara sus hashes con los registros pendientes. Cuando se habilita `con_reglas`, utiliza las variantes generadas por `aplicar_reglas()`. Devuelve un diccionario con las contraseñas encontradas. En la ejecución general se omite PBKDF2 para evitar pruebas masivas de alto costo; su medición se realiza por separado.

Se comprobó la compilación con `py -3 -m py_compile` y se ejecutó una prueba aislada con un usuario ficticio, un hash SHA-256 con salt y un diccionario temporal. La prueba encontró correctamente la contraseña esperada.

**Resultado:** `PRUEBA P2 SUPERADA`.

**Evidencia:** `evidencia/probar-p2.py` y `evidencia/salidas/p2-prueba-aislada.txt`.

La prueba aislada utiliza una implementación temporal de hash dentro del script de prueba, sin alterar el código principal. La ejecución posterior del cracker completo quedó registrada en `evidencia/salidas/r1-r2-diccionario.txt`.

### Reglas de transformación

`aplicar_reglas(palabra)` devuelve una lista de candidatos en orden estable. Combina la palabra original, capitalización inicial, minúsculas y mayúsculas con los sufijos vacíos, 2024–2026 y 1/12/123, tal como propone el contrato del esqueleto. Deduplica conservando el primer orden de aparición: máximo 28 variantes por entrada. No incluye nombres de usuarios, contraseñas completas ni flags del caso. Los años son un rango explícito de la consigna, no dependen del reloj.

Pruebas con `luna`, `LuNa`, cadena vacía, números y Unicode confirman lista de strings, original primero, ausencia de duplicados, repetibilidad y combinaciones de capitalización/sufijos. `capitalize()` normaliza a minúsculas el resto; la variante original también se conserva. La función no elimina espacios de la entrada; el tratamiento de líneas corresponde a la lectura del diccionario.

### Alcance de la prueba de R3

En la etapa documentada por esta prueba, el programa completo todavía no estaba integrado. Por eso se adjunta `evidencia/probar-p3.py`: prueba aislada que importa la función del cracker y compara sus candidatos con SHA-256(salt_bytes + password_bytes) usando hashlib. Recibe las rutas y el usuario por argumentos, se limita al caso SHA-256 y no intenta PBKDF2. No sustituye una ejecución integrada del CLI.

Sobre las 49 palabras del diccionario puro no hubo coincidencia. Con las reglas se encontró `phantom2026`, derivada de `phantom`, en el intento 95. La contraseña no se obtuvo del generador ni de soluciones. Se confirmó el loot con el subcomando oficial `descifrar` de la copia. En aquella etapa, la ejecución `crackear ... --reglas` fallaba en `cargar_sombra`, y su error se conserva en `cli-pendiente-integracion.txt`. **La prueba aislada no se presenta como ejecución exitosa del cracker integrado.**

### Revisión cruzada de las reglas

Se revisó la implementación de `aplicar_reglas()` y se ejecutó el script `evidencia/probar-p3.py` sobre el código del grupo.

Las pruebas confirmaron que la función genera variantes con capitalización y sufijos, conserva un orden estable, evita candidatos duplicados y funciona con distintas entradas.

En la prueba aislada sobre `admin`, el diccionario sin reglas no encontró coincidencias en 49 intentos. Con reglas se recuperó la contraseña del caso en 95 intentos y se comprobó el descifrado del loot.

**Resultado de la revisión:** aprobada para los casos evaluados. No se modificó la implementación revisada.

**Evidencia:** `evidencia/salidas/p2-revision-p3.txt`.
## 2. Medición de velocidad

Se ejecutó `evidencia/medir-p1.py` con Python 3.12.13 en Windows 11, en el procesador indicado en la salida cruda. El script importa la copia entregable de `cracker.py`, llama a `hash_de()` para candidatos sintéticos y usa los salts del caso; no intenta recuperar secretos durante la medición. Para reducir el ruido de mediciones muy cortas, se toma la mediana de 25 series de 100 intentos para MD5/SHA-256 y de 3 series de 20 intentos para PBKDF2, con `time.perf_counter()`.

| Algoritmo | Intentos/segundo (máquina local) | Muestra | Estimación para 49 candidatos |
|---|---:|---:|---:|
| MD5 con salt | 454545,45 | Mediana de 25 × 100 | 0,000108 s |
| SHA-256 con salt | 493096,65 | Mediana de 25 × 100 | 0,000099 s |
| PBKDF2-HMAC-SHA256 (200.000 iteraciones) | 13,73 | Mediana de 3 × 20 | 3,567582 s |

La evidencia completa —versión de Python, sistema, procesador, tamaños de salida y manejo del algoritmo no soportado— está en `evidencia/salidas/p1-benchmark.txt`; el procedimiento reproducible es `evidencia/medir-p1.py`. Los tiempos de diccionario son estimaciones de `49 / tasa`, no ejecuciones adicionales.

### Tasas medidas y significado para un atacante

MD5 y SHA-256 quedaron en el mismo orden de magnitud: SHA-256 resultó 1,08 veces más rápido en esta corrida, una diferencia demasiado pequeña para generalizarla como propiedad del algoritmo o del hardware. PBKDF2-200k fue aproximadamente 33.106 veces más lento que MD5 (4,52 órdenes de magnitud) y 35.914 veces más lento que SHA-256 (4,56 órdenes). La diferencia relevante proviene de que MD5 y SHA-256 hacen un hash rápido por candidato, mientras que PBKDF2 aplica 200.000 iteraciones de HMAC-SHA256. La documentación de Python describe a PBKDF2 como una función de derivación ajustable, lenta y con salt, diseñada para contraseñas, no como un hash rápido directo. [Python `hashlib`](https://docs.python.org/3/library/hashlib.html#key-derivation).

La consigna propone como escenario pedagógico una GPU capaz de realizar `10^9` intentos/s contra MD5. Esa tasa hipotética es unas 2.200 veces la tasa MD5 local medida (3,34 órdenes de magnitud); sobre 49 candidatos, el cociente idealizado sería `49 / 10^9 = 4,9 × 10⁻⁸ s`. Ese cociente expresa solo trabajo de cómputo: para un lote de 49 candidatos no representa una latencia de extremo a extremo, porque omite preparación, transferencia y ejecución. No es una medición de esta GPU ni una tasa aplicable a SHA-256 o PBKDF2: para esos algoritmos depende de la implementación, la memoria y las iteraciones. En particular, trasladar `10^9` intentos/s a PBKDF2-200k sería incorrecto; su propósito es elevar el trabajo de cada candidato incluso en hardware paralelo.


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

## 5. Preguntas de análisis

### ¿Para qué sirve el salt y por qué no impide ataques de diccionario?

El *salt* es un valor aleatorio y no secreto que se incorpora al proceso de generación del hash de una contraseña. Su finalidad es evitar que dos usuarios con la misma contraseña tengan necesariamente el mismo hash y dificultar el uso reutilizable de tablas precalculadas, como las *rainbow tables*.

Al utilizar un salt diferente para cada usuario, es necesario calcular los candidatos para cada registro, en lugar de reutilizar directamente los mismos hashes.

Sin embargo, el salt no impide un ataque de diccionario. Si una contraseña es común o predecible y aparece entre los candidatos, se puede calcular su hash utilizando el salt correspondiente y compararlo con el hash almacenado.

En este laboratorio trabajamos con hashes MD5 y SHA-256 que incorporan salt. Esto permite comprobar que el salt no reemplaza la necesidad de utilizar contraseñas difíciles de adivinar ni algoritmos de derivación costosos, como PBKDF2. OWASP recomienda algoritmos lentos y adaptables para almacenar contraseñas y salt único por contraseña; SHA-256 rápido no es adecuado para ese fin. [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).

**En conclusión**, el salt dificulta los ataques basados en tablas precalculadas y evita que hashes iguales revelen directamente contraseñas compartidas, pero no impide probar contraseñas mediante un diccionario.

### Complejidad predecible y NIST

Una política que cuenta caracteres de distintas clases no mide cuán fácil es adivinar la elección humana. Nuestro generador no exploró todas las cadenas posibles: probó unas pocas transformaciones previsibles de palabras conocidas. Agregar el año produce candidatos baratos de enumerar.

**Discrepancia del enunciado:** la contraseña observada es `phantom2026` (11 caracteres, minúsculas y dígitos, sin mayúsculas). Por eso no cumple literalmente la condición de mayúsculas que afirma la pregunta. No se modifica el resultado para ajustarlo al relato. La debilidad conceptual permanece: una variante con inicial mayúscula también está cubierta por las reglas, aunque no es la contraseña recuperada.

Según NIST SP 800-63B-4, sección 3.1.1.2, la longitud mínima es 15 caracteres para contraseñas usadas como único factor; pueden admitirse ocho cuando forman parte de MFA. Se recomienda permitir al menos 64 como longitud máxima admitida. No se deben imponer mezclas obligatorias de tipos de caracteres ni cambios periódicos sin indicios de compromiso. Debe contrastarse la contraseña completa con una lista de valores comunes, esperables o comprometidos. [NIST SP 800-63B-4, consultado el 29/10/2026](https://pages.nist.gov/800-63-4/sp800-63b.html#passwordver).

Para el caso, una longitud mayor y evitar elecciones previsibles es más útil que añadir mecánicamente una mayúscula y un año. La limitación de intentos en el login protege frente a intentos online, pero no detiene este ataque offline contra una copia de hashes; el almacenamiento con salt y derivación costosa aborda ese segundo escenario. No debe interpretarse que una regla de longitud garantiza por sí sola resistencia a cualquier ataque.

### Trabajo por intento y por qué root no cayó

PBKDF2-HMAC-SHA256 repite la función de derivación 200.000 iteraciones por candidato, frente a una sola operación de MD5 o SHA-256 en los registros rápidos. En la muestra controlada se calcularon 20 candidatos sintéticos usando el salt de `root`, sin compararlos con su hash ni intentar recuperar su contraseña. En Python 3.13, sobre Windows 11 y el procesador informado en la salida, el cálculo tomó 1,431237 s: 13,97 candidatos/s (71,562 ms por candidato). La ejecución reproducible es `python entregas/labextra4/grupo06/evidencia/medir-pbkdf2.py`; la salida está en `evidencia/salidas/p4-pbkdf2-muestra.txt`.

La muestra usa directamente `hashlib.pbkdf2_hmac` de la biblioteca estándar para aislar el costo de derivación, por lo que no se presenta como una prueba del CLI integrado. Al ritmo observado, recorrer los 49 candidatos del diccionario en esta misma máquina tomaría aproximadamente 3,51 s; es una extrapolación del promedio, no una corrida adicional. El salt no evita probar palabras, pero obliga a calcularlas por registro. Además, el caso establece que la contraseña de `root` no está en el diccionario: completar la búsqueda no produciría una coincidencia.

Para el escenario de 1.000 GPUs no hay benchmark local de GPU. Si se supone, solo como ejemplo, una tasa de `v = 100` candidatos/s por GPU, el cociente de trabajo agregado es `T ≈ N/(1000·v) = 49/(1000·100) = 0,00049 s`. Sin embargo, como hay solo 49 candidatos, no pueden aprovecharse más de 49 GPUs para esa búsqueda: el límite ideal de pared es aproximadamente un intento por GPU (`1/v = 0,01 s`), más el costo de distribución y arranque. Ambas cifras son escenarios teóricos, no una medición ni una extrapolación de la tasa de CPU.

## 6. Conclusión

El caso demuestra que un salt evita reutilizar cálculos precalculados, pero no vuelve resistente una contraseña incluida en un diccionario ni una variante previsible de esa palabra. Las mediciones locales ubican MD5 y SHA-256 en el mismo orden de magnitud y muestran que PBKDF2-200k eleva el costo por candidato en más de cuatro órdenes de magnitud en este equipo. Para un sistema real, la política debe combinar contraseñas largas y bloqueadas contra listas de valores comprometidos con un algoritmo de almacenamiento lento y adaptable, salt único y parámetros revisables. La guía de OWASP prioriza Argon2id y, cuando se necesita PBKDF2-HMAC-SHA256 por requisitos de compatibilidad o FIPS, indica al menos 600.000 iteraciones; ese número es una recomendación externa actual, no una medición de este laboratorio. [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).
