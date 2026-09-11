# Informe — Laboratorio 02 · Criptografía

**Grupo:** 06 · **Integrantes:**

- Beccereca, Martín - martinbeccereca
- Benito, María Belén
- De Miguel, Alejo - AlejoDM
- Giudici, Tomás
- Suppo, Carolina - carosuppo

**Fecha:** 04/09/2026

---

## 0. Declaración de uso de IA

**Herramienta: Google Antigravity (Gemini 3.7 Flash)**
- **Finalidad del uso:** Estructuración del informe Markdown.
- **Partes generadas o asistidas:** Estructuración del esquema del informe.
- **Verificación:** Todos los datos históricos, volúmenes de registros expuestos, detalles criptográficos y fuentes bibliográficas fueron contrastados y verificados manualmente contra publicaciones de seguridad primarias.

**Herramienta: Claude Code**
- **Finalidad del uso:** Apoyo en la redacción del mini-research (investigación con fuentes verificables) y en la consolidación de la bitácora de comandos de la Parte B.
- **Partes generadas o asistidas:** `research.md` (mini-research, Tema C) y sección 4 — Bitácora del informe.
- **Verificación:** Las fuentes citadas en el mini-research se consultaron entrando a cada documento antes de citarlas.

---

## 1. Parte A — Análisis de la falla

**Caso:** Adobe 2013 (Cifrado simétrico 3DES en modo ECB de contraseñas y almacenamiento de pistas en texto claro)

### A.1 — Qué prometía el sistema y Cronología de hechos

#### Promesa del sistema

El sistema de gestión de identidades de Adobe (Adobe ID / _Identity Management Services_) prometía garantizar la confidencialidad, autenticidad y resguardo seguro de las credenciales de acceso de sus usuarios registrados frente a intrusiones externas, asegurando que las contraseñas no pudieran ser leídas en claro ni reconstruidas por terceros no autorizados, al tiempo que garantizaba la integridad y protección de la propiedad intelectual de sus productos comerciales [3, 7].

#### Cronología (Hitos principales)

1. **Mediados de 2013:** Atacantes vulneran la red interna de Adobe (vía servidores con vulnerabilidades en ColdFusion) y exfiltran repositorios y la base de identidades [1].
2. **17/09/2013:** Los investigadores Alex Holden y Brian Krebs descubren en un servidor clandestino 40 GB de código fuente y una base masiva de usuarios de Adobe [2].
3. **03/10/2013:** Adobe publica su anuncio oficial admitiendo el acceso no autorizado a 2.9 millones de cuentas activas y robo de código fuente de Acrobat, ColdFusion y Photoshop [3].
4. **Finales de Octubre 2013:** Se filtra públicamente en internet el volcado `users.tar.gz` (3.8 GB) con 152.989.508 registros de cuentas [4].
5. **04/11/2013:** Análisis de seguridad revelan el ranking de contraseñas más comunes exponiendo la vulnerabilidad del cifrado simétrico por repetición de patrones [5].
6. **Noviembre 2013:** Investigadores criptográficos confirman el mal uso de 3DES en modo ECB sin sal (_salt_) y el almacenamiento de pistas en texto plano [6].
7. **2014–Presente:** Estudios académicos consolidan el caso como el ejemplo paradigmático de falla por preservar patrones y sustitución inadecuada de funciones hash unidireccionales [7].

---

### A.2 — Activo afectado y contexto del mal uso

#### Activos concretos comprometidos:

1. **Base de Datos de Credenciales de Adobe ID (`users.tar.gz`):**
   - 152.989.508 registros de usuarios, conteniendo cada uno: identificador único interno, dirección de correo electrónico, nombre de usuario, contraseña cifrada simétricamente en bloques fijos y pistas de contraseña almacenadas en texto plano sin cifrar [4, 6].
2. **Información Financiera Parcial de Clientes:**
   - 38 millones de registros de transacciones activas con números de tarjetas de crédito/débito cifrados, fechas de vencimiento y nombres asociados [2, 3].
3. **Propiedad Intelectual y Código Fuente:**
   - Repositorios de código fuente privativo de herramientas comerciales críticas: Adobe Acrobat, Adobe ColdFusion / ColdFusion Builder y Adobe Photoshop [2, 3].

#### Contexto del mal uso criptográfico:

La falla no radicó en una debilidad matemática intrínseca del algoritmo de cifrado en sí (Triple DES / 3DES), sino en un grave error de diseño y mal uso conceptual de las primitivas criptográficas:

- Cifrado reversible en vez de hashing unidireccional: Se utilizó cifrado simétrico reversible para guardar contraseñas en lugar de una función de derivación de claves / hashing unidireccional lento y con sal aleatoria (salted password hashing como bcrypt, PBKDF2 o scrypt) [6, 7].
- Modo ECB (Electronic Codebook) y misma clave global: Al cifrar con una única clave en modo ECB sin vector de inicialización (IV) ni salting, bloques idénticos de texto plano producen bloques idénticos de texto cifrado [6, 7].
- Pistas en texto plano vinculadas: Al incluir pistas de contraseña en texto claro junto con los bloques cifrados idénticos, los atacantes pudieron descifrar por correlación y análisis de frecuencia millones de contraseñas de toda la base (por ejemplo, identificando qué criptograma correspondía a contraseñas universales como "123456" o "password" y cruzándolo con las pistas de los usuarios) [5, 6].

---

### A.3 — Propiedad rota y explotación

_(A completar por el integrante asignado)_

---

### A.4 — Lo correcto

_(A completar por el integrante asignado)_

---

## 2. Parte B.1 — Romper el XOR

La clave hallada es `0x37` y el mensaje es `Memo interno PhantomCorp: la clave del wifi de invitados es Phantom-Guest-2026. No compartir fuera de la empresa.`.

### ¿Por qué falla un cifrado clásico de clave corta?

Un XOR con una clave de un solo byte no proporciona una cantidad suficiente de incertidumbre criptográfica. Aunque el XOR sea una operación matemáticamente válida para cifrar y descifrar, utilizar una clave de solamente 8 bits deja únicamente 2^8 = 256 claves posibles.

Por lo tanto, un atacante puede probar todas las claves mediante fuerza bruta y utilizar características estadísticas del lenguaje para identificar automáticamente el texto correcto. El problema principal no es XOR en sí mismo, sino el uso de una clave extremadamente corta y repetida.

Este ejemplo demuestra que un cifrado con un espacio de claves pequeño no ofrece confidencialidad frente a un atacante que pueda realizar una búsqueda exhaustiva.

---

## 3. Parte B.2 — Autenticación

### B.2.1 — ¿Por qué `sha256(clave || mensaje)` permite un ataque de length-extension?

Utilizar `sha256(clave || mensaje)` como MAC es inseguro debido a la forma en que SHA-256 procesa la información. El algoritmo trabaja con el mensaje en bloques sucesivos y el hash final depende del estado interno obtenido después de procesarlos.

Si un atacante conoce un mensaje y su MAC correspondiente:

`MAC = SHA256(clave || mensaje)`

puede utilizar ese hash como punto de partida para continuar el cálculo y agregar nuevos datos al final del mensaje. Para realizar el ataque no necesita conocer el contenido de la clave secreta, aunque sí debe conocer o estimar su longitud para poder reproducir correctamente el padding utilizado por SHA-256.

De esta forma, puede construir un mensaje como:

`mensaje || padding || contenido_agregado`

y obtener un MAC válido para ese mensaje extendido sin conocer la clave.

Por ejemplo, si un sistema autentica el mensaje `usuario=123&accion=consultar`, un atacante que conozca el MAC podría intentar agregar al final `&admin=true` y calcular un nuevo MAC válido. Esto no significa que pueda modificar libremente cualquier parte del mensaje original, sino que puede extenderlo agregando información al final.

Por este motivo, utilizar directamente `sha256(clave || mensaje)` no es una forma segura de construir un MAC.

### B.2.2 — ¿Cómo lo resuelve HMAC estructuralmente?

HMAC evita este problema porque no se limita a concatenar la clave con el mensaje y calcular un único hash. Utiliza una construcción de dos niveles en la que la clave secreta interviene dos veces, combinada con dos valores diferentes denominados `ipad` y `opad`.

De forma simplificada, HMAC tiene la siguiente estructura:

`H((K ⊕ opad) || H((K ⊕ ipad) || mensaje))`

Primero se calcula un hash interno utilizando la clave combinada con `ipad` y el mensaje. Luego, el resultado de ese hash se utiliza como entrada de un segundo hash, donde vuelve a intervenir la clave, esta vez combinada con `opad`.

Esto hace que el valor final que recibe un atacante sea el resultado del hash externo y no un estado interno que pueda reutilizar directamente para continuar procesando datos. Por lo tanto, aunque se utilice SHA-256 dentro de HMAC, un atacante no puede aprovechar un ataque de length-extension para generar un HMAC válido de un mensaje extendido, ya que para calcular correctamente el hash externo sigue necesitando conocer la clave secreta.

### B.2.3 — ¿Qué ataque evita `hmac.compare_digest()`?

`hmac.compare_digest()` se utiliza para reducir el riesgo de ataques de temporización o _timing attacks_ durante la verificación de un MAC.

Una comparación convencional puede detenerse cuando encuentra el primer byte diferente. Esto puede generar pequeñas variaciones en el tiempo de respuesta dependiendo de cuántos bytes iniciales coincidan con el valor correcto.

Por ejemplo, si el MAC correcto comienza con `a7f3`, un atacante podría realizar muchas pruebas con valores como `0000`, `a000`, `a700` o `a7f0`. Si las comparaciones que tienen más bytes correctos al comienzo tardan ligeramente más, podría utilizar esas diferencias de tiempo para ir deduciendo progresivamente el MAC esperado.

## `hmac.compare_digest()` está diseñado para realizar la comparación sin que el tiempo dependa de la posición del primer byte diferente. De esta manera se reduce la información que puede obtener un atacante midiendo los tiempos de respuesta y se evita que esa diferencia funcione como un canal lateral para intentar descubrir un MAC válido.

## 4. Bitácora

```bash
$ python3 src/cripto.py xor --texto hola --clave K
2324272a

$ python3 src/cripto.py romper --hex $(cat data/muestra/reto_xor.hex)
clave=0x37
Memo interno PhantomCorp: la clave del wifi de invitados es Phantom-Guest-2026. No compartir fuera de la empresa.

$ python3 src/cripto.py mac --clave secreta --msg "pago 100" --modo ingenuo
a8cc54c07b3acb7470c25ab9eea5234bfa2562e37298eee275e39a457004b725

$ python3 src/cripto.py mac --clave secreta --msg "pago 100" --modo hmac
5ec4a52407221836a66e8d654d914aaa4b18bd31cf31907348bcd292677b902e
```

---

## 5. Fuentes consultadas

1. **Huntress Threat Library:** [Adobe Data Breach Analysis](https://www.huntress.com/threat-library/data-breach/adobe-data-breach) — Análisis del vector de ataque y exfiltración de código fuente.
2. **KrebsOnSecurity (Brian Krebs, 03/10/2013):** [Adobe to Announce Cyberattack, Exfiltration of Customer Data and Source Code](https://krebsonsecurity.com/2013/10/adobe-to-announce-cyberattack-exfiltration-of-customer-data-and-source-code/) — Reporte del hallazgo del servidor con los datos exfiltrados.
3. **Adobe Systems Inc. (Brad Arkin, CSO, 03/10/2013):** [Important Customer Security Announcement](https://www.adobe.com) — Comunicado oficial de seguridad de Adobe.
4. **Have I Been Pwned (Troy Hunt):** [Adobe Data Breach Details](https://haveibeenpwned.com/Breach/Adobe) — Verificación de los 152.989.508 registros comprometidos y estructura de datos expuesta.
5. **KrebsOnSecurity (Brian Krebs, 04/11/2013):** [Top 100 Most Common Passwords from Adobe Hack](https://krebsonsecurity.com/2013/11/top-100-most-common-passwords-from-adobe-hack/) — Análisis de repetición de patrones y frecuencias en contraseñas cifradas.
6. **DeHashed Insights:** [Adobe Data Breach October 2013 Analysis](https://dehashed.com/insights/adobe-data-breach-2013-october) — Análisis técnico del esquema de cifrado 3DES en modo ECB y el impacto de las pistas en texto plano.
7. **ResearchGate Case Study:** [Adobe Cyberattack 2013: Case study](https://www.researchgate.net/publication/388499862_Adobe_Cyberattack_2013_Case_study) — Estudio académico sobre la arquitectura, fallas de diseño criptográfico y consecuencias del incidente.
