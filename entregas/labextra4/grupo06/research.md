# Research — Lab Extra 4: cracking de contraseñas

**Opción elegida:** B — Hashcat y herramientas profesionales  
**Fecha de consulta:** 29/10/2026

## Hashcat y el paralelismo de GPU

Hashcat es un único programa que puede ejecutar modos de ataque en CPU o GPU mediante distintos backends —CUDA, HIP, Metal y OpenCL— y distribuir trabajo entre varios dispositivos compatibles. En un ataque offline, cada candidato se puede verificar de manera independiente: el motor genera candidatos y los dispositivos calculan sus hashes en paralelo. Por eso una GPU puede evaluar millones o miles de millones de hashes rápidos por segundo. La tasa real depende del modo, los parámetros, el hardware, la versión y el ajuste del kernel; no es una propiedad universal de “la GPU”. Hashcat incorpora benchmarks por modo precisamente para medir el dispositivo y configuración concretos. [Documentación de Hashcat](https://hashcat.net/hashcat/) · [Hashcat, benchmark público en foro](https://hashcat.net/forum/thread-11750.html)

Un benchmark publicado el 04/01/2024 para Hashcat v6.2.6 en **ocho RTX 4090** informa una tasa agregada de **1.177,6 GH/s para MD5 (modo 0)** y **1.708,7 kH/s para bcrypt (modo 3200, parámetro de iteración 32)**. En ese equipo y configuración, MD5 produjo cerca de **690.000 veces** más verificaciones por segundo que bcrypt. Es un contraste de órdenes de magnitud, no una comparación de resistencia bajo parámetros equivalentes: el modo MD5 del benchmark es un hash rápido y sin salt, mientras que bcrypt incorpora un costo configurable. En el laboratorio, además, se trata de MD5 con salt, así que no corresponde trasladar directamente la tasa de modo 0 al caso. [Salida de benchmark publicada en el foro oficial de Hashcat](https://hashcat.net/forum/thread-11750.html)

Para Argon2id, un análisis de Specops resumido el 21/07/2026 por CyberInsider reporta aproximadamente **490 verificaciones/s** para un sistema con ocho RTX 5090; el mismo resumen da alrededor de **221.000 millones de SHA-256/s** en ese sistema. La razón entre esas tasas es aproximadamente `4,5 × 10^8`, para las configuraciones concretas del estudio. El resultado ilustra cómo un KDF con uso de memoria puede limitar la ventaja de multiplicar GPUs, pero no se debe combinar aritméticamente con el benchmark anterior: cambian tanto el equipo como la prueba, y el resumen no detalla todos los parámetros de Argon2id. El dato no es una medición de este grupo. [Estudio de Specops](https://specopssoft.com/blog/does-argon2-mean-password-uncrackable/) · [Resumen y cifras publicadas](https://cyberinsider.com/argon2-algorithm-dramatically-slows-password-cracking-by-high-end-gpus/)

Argon2 fue diseñado como una función de derivación con uso intensivo de memoria; sus parámetros de memoria, iteraciones y paralelismo deben formar parte de cualquier cifra reportada. La ocupación de memoria limita cuántos cálculos simultáneos caben en una GPU, por lo que añadir unidades de cómputo no escala como con un hash rápido. La documentación actual de Hashcat distingue Argon2 de Argon2id y marca el modo Argon2id de referencia como *bridged*: la tasa depende también de la variante, su implementación y sus parámetros, no solo del nombre del algoritmo. Tampoco significa que Argon2 vuelva irrecuperable cualquier contraseña: una contraseña filtrada, reutilizada o muy predecible puede aparecer pronto en una lista de candidatos. [RFC 9106 — Argon2](https://www.rfc-editor.org/rfc/rfc9106.html) · [Modos de Hashcat](https://hashcat.net/hashcat/)

## Máscara, combinator y reglas

Un ataque **mask** fija un patrón por posición y enumera las combinaciones compatibles. Por ejemplo, `?u?l?l?l?d?d` expresa una mayúscula, tres minúsculas y dos dígitos; reduce el espacio frente a probar todos los caracteres en todas las posiciones, a costa de no hallar contraseñas que no sigan ese patrón. El ataque **combinator** concatena cada palabra de una lista con cada palabra de otra: con listas de tamaños *A* y *B* genera hasta *A × B* combinaciones. Hashcat también permite aplicar reglas de transformación a las palabras de diccionario. [Mask attack](https://hashcat.net/wiki/doku.php?id=mask_attack) · [Combinator attack](https://hashcat.net/wiki/doku.php?id=combinator_attack) · [Rule-based attack](https://hashcat.net/wiki/doku.php?id=rule_based_attack)

La `aplicar_reglas()` de este práctico es una implementación acotada y estable: aplica capitalizaciones y sufijos predefinidos a cada palabra del diccionario. El motor de reglas de Hashcat ofrece un lenguaje más amplio de transformaciones y filtros; no es lo mismo que una máscara posicional ni que combinar dos listas. Los tres enfoques son formas de priorizar candidatos informados, no de demostrar que se probó todo el espacio posible.

## Rainbow tables y salt

Una rainbow table precalcula cadenas de valores hash para recuperar candidatos contra muchos hashes rápidos, amortizando el cálculo previo. Un salt único y aleatorio por registro cambia la entrada del hash: la misma contraseña produce resultados distintos según el salt y una tabla preparada para un salt no se reutiliza directamente con otro. Esto vuelve impráctico precalcular una tabla universal para todas las cuentas. El salt **no** detiene un diccionario: todavía es posible calcular cada candidato con el salt de cada registro. Para almacenamiento moderno se necesita además un esquema de contraseñas lento y ajustable, como Argon2id o bcrypt, con parámetros apropiados. [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) · [RFC 9106](https://www.rfc-editor.org/rfc/rfc9106.html)

## Contraseñas comprometidas, NIST y k-anonymity

NIST SP 800-63B-4 pide cotejar la contraseña propuesta con una lista de valores comunes, esperables o comprometidos, y no imponer reglas mecánicas de composición como “una mayúscula, un número y un símbolo”. Para una contraseña usada como único factor fija un mínimo de 15 caracteres; si se usa solo como parte de MFA puede admitirse un mínimo de ocho. Tampoco recomienda forzar cambios periódicos sin evidencia de compromiso. Una lista de bloqueo se concentra en elecciones que los atacantes suelen probar primero; las reglas de composición pueden generar sustituciones previsibles y una falsa sensación de seguridad. [NIST SP 800-63B-4, §3.1.1.2](https://pages.nist.gov/800-63-4/sp800-63b.html#passwordver)

Have I Been Pwned permite comprobar contraseñas comprometidas con un esquema de **k-anonymity**: el cliente calcula localmente el SHA-1 de la contraseña y envía solamente los primeros cinco caracteres hexadecimales del hash a la API de Pwned Passwords. El servicio devuelve los sufijos de todos los hashes con ese prefijo y sus recuentos; el cliente compara localmente el sufijo completo y descarta las entradas que no coinciden. Así no se envían la contraseña ni su hash completo. SHA-1 aquí es únicamente un índice de consulta, no una recomendación para almacenar contraseñas. El prefijo todavía revela información parcial, por lo que el procedimiento reduce la exposición pero no equivale a anonimato absoluto. [Documentación de Pwned Passwords](https://haveibeenpwned.com/API/v3#PwnedPasswords) · [HIBP: guía NIST](https://haveibeenpwned.com/NIST)

## Fuentes consultadas

- Hashcat, página oficial y capacidades del programa: <https://hashcat.net/hashcat/>.
- Hashcat, benchmark publicado para ocho RTX 4090, Hashcat v6.2.6: <https://hashcat.net/forum/thread-11750.html>.
- Specops, investigación sobre Argon2id: <https://specopssoft.com/blog/does-argon2-mean-password-uncrackable/>; resumen secundario de las cifras: <https://cyberinsider.com/argon2-algorithm-dramatically-slows-password-cracking-by-high-end-gpus/>.
- RFC 9106, especificación de Argon2: <https://www.rfc-editor.org/rfc/rfc9106.html>.
- OWASP, almacenamiento de contraseñas: <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>.
- NIST SP 800-63B-4, verificación de contraseñas: <https://pages.nist.gov/800-63-4/sp800-63b.html#passwordver>.
- Have I Been Pwned, API de Pwned Passwords y búsquedas por rango: <https://haveibeenpwned.com/API/v3#PwnedPasswords>.

## Declaración de uso de IA

**Herramienta:** Opencode.  
**Finalidad y partes asistidas:** búsqueda y síntesis de fuentes, comparación de benchmarks públicos y redacción de esta investigación y su cierre sobre NIST/HIBP.  
**Verificación:** las cifras de Hashcat se contrastaron con la salida pública enlazada y se recalculó su relación; las cifras de Argon2id se atribuyen al estudio de Specops tal como las reporta CyberInsider, sin presentarlas como medición local ni como comparación de parámetros equivalentes. P4 debe realizar la lectura humana final de las fuentes y el texto antes de la entrega.
