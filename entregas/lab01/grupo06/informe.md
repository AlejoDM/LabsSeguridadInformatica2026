# Laboratorio 01 — Informe

---

## Identificación

|                             |                                                                  |
| --------------------------- | ---------------------------------------------------------------- |
| **Grupo**                   | 06                                                               |
| **Caso asignado (Parte A)** | Morris Worm (1988)                                               |
| **Tema del mini-research**  | Tema 3 — La disponibilidad, la propiedad descuidada de la tríada |
| **Fecha de entrega**        |                                                                  |

### Integrantes

| Nombre y apellido  | Legajo | Usuario de GitHub   |
| ------------------ | ------ | ------------------- |
| Martín Beccereca   | 15154  | @martinbeccereca    |
| María Belén Benito | 14625  | @belubenito603-byte |
| Alejo De Miguel    | 15138  | @AlejoDM            |
| Tomás Giudici      | 14977  | @TomasGiudici       |
| Carolina Suppo     | 15057  | @carosuppo          |

---

# PARTE A — Análisis del incidente bajo la lente CIA

## A.1 — Cronología

| Fecha                      | Hecho                                                                                                                                                                                                                                                      | Fuente                                                                                                                                                                                |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1988-11-02 (noche)         | Robert Tappan Morris, estudiante de posgrado de Cornell, libera el gusano desde una máquina del MIT para disimular su origen real.                                                                                                                         | [_United States v. Morris_, 928 F.2d 504 (2d Cir. 1991)](https://law.resource.org/pub/us/case/reporter/F2/928/928.F2d.504.90-1336.774.html)                                           |
| 1988-11-02/03              | El gusano se propaga explotando cuatro vectores: un bug en el modo debug de `sendmail`, un desbordamiento en `fingerd`, la función de "trusted hosts" (`rsh`/`rexec`) y adivinación de contraseñas.                                                        | [_United States v. Morris_, 928 F.2d 504 (2d Cir. 1991)](https://law.resource.org/pub/us/case/reporter/F2/928/928.F2d.504.90-1336.774.html)                                           |
| 1988-11 (horas siguientes) | Un error en su lógica de reinfección (probabilidad de re-copiarse aun en máquinas ya infectadas) provoca que se acumulen decenas de procesos por host, agotando CPU y memoria; ~6.000 de los ~60.000 hosts conectados a Internet (~10 %) quedan afectados. | [Lawrence Livermore National Laboratory, _"The 1988 Morris worm, the internet's first cyberattack"_](https://st.llnl.gov/news/look-back/1988-morris-worm-internets-first-cyberattack) |
| 1988-11 (días siguientes)  | DARPA encarga al Software Engineering Institute de Carnegie Mellon la creación de un centro de coordinación de emergencias informáticas; nace así el CERT/CC, en respuesta directa a este incidente.                                                       | [Carnegie Mellon University SEI, _"History of Innovation"_](https://www.sei.cmu.edu/history-of-innovation/)                                                                           |
| 1990-05-16                 | El tribunal de distrito (juez Howard G. Munson, Distrito Norte de Nueva York) dicta sentencia: 3 años de libertad condicional, 400 horas de servicio comunitario y una multa de USD 10.050.                                                                | [_United States v. Morris_, 928 F.2d 504 (2d Cir. 1991)](https://law.resource.org/pub/us/case/reporter/F2/928/928.F2d.504.90-1336.774.html)                                           |
| 1991-03-07                 | La Corte de Apelaciones del Segundo Circuito confirma la condena, convirtiendo el caso en la primera confirmada bajo la Computer Fraud and Abuse Act de 1986.                                                                                              | [_United States v. Morris_, 928 F.2d 504 (2d Cir. 1991)](https://law.resource.org/pub/us/case/reporter/F2/928/928.F2d.504.90-1336.774.html)                                           |

---

## A.2 — Activo afectado

**Activo principal:** los recursos de cómputo —ciclos de CPU, memoria y
espacio en la tabla de procesos— de las máquinas Unix derivadas de BSD (VAX
y Sun-3, entre otras) conectadas a Internet en noviembre de 1988. No un dato
puntual, sino la capacidad operativa de esos equipos para seguir prestando
servicio.

**Por qué es el principal:** es el recurso que el gusano consumió de forma
directa e incontrolada. El programa reinfectaba repetidamente una misma
máquina —un fallo en el mecanismo pensado para evitarlo— y cada reinfección
sumaba un proceso más, hasta un comportamiento equivalente a una bomba de
forks que agotaba CPU y memoria. La propia [Lawrence Livermore National
Laboratory](https://st.llnl.gov/news/look-back/1988-morris-worm-internets-first-cyberattack)
lo resume así: _"the Morris worm did not damage or destroy files, it slowed
systems to a crawl"_ — es decir, el efecto es enteramente sobre
disponibilidad, no sobre confidencialidad ni integridad de ningún dato. Los
cuatro vectores de propagación (bug de `sendmail`, bug de `fingerd`,
"trusted hosts" y adivinación de contraseñas) documentados en [_United
States v. Morris_](https://law.resource.org/pub/us/case/reporter/F2/928/928.F2d.504.90-1336.774.html)
fueron el medio para llegar a ese activo, no el activo en sí.

**Otros activos afectados:** la conectividad operativa de ARPANET/Internet
como red compartida. Numerosas instituciones —universidades, centros de
investigación militar— debieron desconectarse preventivamente de la red
durante horas o días para contener la propagación y desinfectar sus equipos,
interrumpiendo el intercambio de correo y archivos entre sitios. Es un
impacto de disponibilidad de segundo orden, derivado del agotamiento de
recursos en cada host individual, no un activo distinto al principal.

---

## A.3 — Matriz CIA

_Una fila por propiedad. La columna «Evidencia» tiene que citar un hecho
concreto del incidente, no una generalidad._

> **Advertencia.** «No» es una respuesta válida y muchas veces la correcta.
> El error típico es marcar las tres propiedades en «Sí» porque el incidente
> fue grave. La gravedad no es una propiedad de la tríada. Si marcás que se
> violó la integridad, tenés que mostrar **qué dato específico fue alterado**.
> Si no podés mostrarlo, la respuesta es «No».

| Propiedad            | ¿Se violó?        | Evidencia concreta |
| -------------------- | ----------------- | ------------------ |
| **Confidencialidad** | Sí / No / Parcial |                    |
| **Integridad**       | Sí / No / Parcial |                    |
| **Disponibilidad**   | Sí / No / Parcial |                    |

**Justificación ampliada de la propiedad más discutible:**

_De las tres, ¿cuál fue la más difícil de determinar y por qué? Desarrollá._

---

## A.4 — Encadenamiento amenaza → vulnerabilidad → impacto

_Redacción en prosa, no viñetas. Usá los términos con precisión: una amenaza
no es una vulnerabilidad, un exploit no es una vulnerabilidad, y el impacto
no es el ataque._

```
amenaza  →  explota  →  vulnerabilidad  →  sobre  →  activo  →  produce  →  impacto
```

| Elemento                                                     | En este caso |
| ------------------------------------------------------------ | ------------ |
| **Amenaza** _(quién / qué, con qué motivación)_              |              |
| **Vulnerabilidad** _(la debilidad concreta que se explotó)_  |              |
| **Activo** _(sobre qué recayó)_                              |              |
| **Impacto** _(consecuencia sobre el negocio o las personas)_ |              |

**Redacción:**

_Un párrafo que encadene los cuatro elementos anteriores._

---

## A.5 — Dos controles mitigantes

_Controles que, de haber estado implementados, habrían evitado o reducido el
incidente. Específicos y justificados contra **este** caso. «Tener antivirus»
o «capacitar a los usuarios» no califica._

### Control 1

|                                                     |     |
| --------------------------------------------------- | --- |
| **Qué es**                                          |     |
| **Propiedad de la tríada que protege**              |     |
| **Por qué habría funcionado en este caso concreto** |     |

### Control 2

|                                                     |     |
| --------------------------------------------------- | --- |
| **Qué es**                                          |     |
| **Propiedad de la tríada que protege**              |     |
| **Por qué habría funcionado en este caso concreto** |     |

---

## A.6 — Fuentes consultadas (Parte A)

_Formato APA. Indicá para cada una si es primaria (informe oficial, documento
del fabricante, resolución judicial, paper) o secundaria (nota periodística,
entrada de blog)._

1.
2.
3.

---

# PARTE B — Integridad con funciones de hash

## B.1 — Evidencia de ejecución

_Pegá la salida real de cada comando. No la transcribas a mano: copiala tal
cual sale de la terminal._

### Generación del manifiesto

```
$ python3 src/integridad.py generar --dir data/muestra --salida manifest.sha256

Manifiesto generado: manifest.sha256
Directorio base:     data\muestra
Archivos indexados:  4
```

### Verificación sobre un directorio íntegro

```
$ python3 src/integridad.py verificar --dir data/muestra --manifiesto manifest.sha256
$ echo "código de salida: $?"

Directorio:  data\muestra
Manifiesto:  manifest.sha256

  OK             4
  MODIFICADO     0
  FALTANTE       0
  NUEVO          0

INTEGRIDAD VERIFICADA — sin diferencias contra el manifiesto.
código de salida: 0
```

### Detección de la modificación de un byte

_Esta prueba es obligatoria y tiene una penalización específica en la rúbrica
si falla._

```
$ printf 'X' >> data/muestra/transferencia.txt
$ python3 src/integridad.py verificar --dir data/muestra --manifiesto manifest.sha256
$ echo "código de salida: $?"

Directorio:  data\muestra
Manifiesto:  manifest.sha256

  OK             3
  MODIFICADO     1
  FALTANTE       0
  NUEVO          0

Hallazgos:
  [MODIFICADO] transferencia.txt

INTEGRIDAD COMPROMETIDA — 1 hallazgo(s).
código de salida: 1
```

### Detección de archivo faltante y de archivo nuevo

```
python3 data/generar_datos.py
python3 src/integridad.py generar --dir data/muestra --salida manifest.sha256
Remove-Item data/muestra/politica_seguridad.md
python3 src/integridad.py verificar --dir data/muestra --manifiesto manifest.sha256
Write-Output "código de salida: $LASTEXITCODE"

Directorio:  data\muestra
Manifiesto:  manifest.sha256

  OK             3
  MODIFICADO     0
  FALTANTE       1
  NUEVO          0

Hallazgos:
  [FALTANTE] politica_seguridad.md

INTEGRIDAD COMPROMETIDA — 1 hallazgo(s).
código de salida: 1

python3 data/generar_datos.py
python3 src/integridad.py generar --dir data/muestra --salida manifest.sha256
Set-Content -Path data/muestra/nuevo.txt -Value "archivo nuevo"
python3 src/integridad.py verificar --dir data/muestra --manifiesto manifest.sha256
Write-Output "código de salida: $LASTEXITCODE"

Directorio:  data\muestra
Manifiesto:  manifest.sha256

  OK             4
  MODIFICADO     0
  FALTANTE       0
  NUEVO          1

Hallazgos:
  [NUEVO] nuevo.txt

INTEGRIDAD COMPROMETIDA — 1 hallazgo(s).
código de salida: 1
```

### Efecto avalancha

```
$ python3 src/integridad.py avalancha --a "transferencia: $1000" --b "transferencia: $1001"

mensaje A: "transferencia: $1000"
  SHA-256: 341511c4c817d55f30c81e212d0e82b0b16dd5a58d49fe5e45c9d5c998ab794a
mensaje B: "transferencia: $1001"
  SHA-256: 5fb87fd7adf8a226f61c666a3ed140b147501b8a1b8e1822e57fc4b3925323d9

Distancia de Hamming: 139 de 256 bits (54.30 %)
Efecto avalancha: para entradas distintas se espera un valor cercano al 50 %.
```

**Distancia obtenida:** 139 bits de 256 (54.30 %)

_¿Coincide con lo esperado? ¿Qué esperaban antes de correrlo?_

Sí, coincide con lo esperado. Antes de ejecutar la prueba esperábamos que, al cambiar un solo carácter del mensaje, aproximadamente la mitad de los 256 bits del hash SHA-256 fueran diferentes, es decir, un valor cercano al 50 % (128 bits). Se obtuvo una distancia de 139 bits (54,30 %), por lo que el resultado es razonablemente cercano a lo esperado y demuestra el efecto avalancha.

### HMAC

```
$ python3 src/integridad.py mac --clave "secreto" --mensaje "transferir 1000"

mensaje:      "transferir 1000"
HMAC-SHA256:  96bc66546d55627136aeaaefbcead75520a57e19539834d03e74d705b70ff9fe
```

```
$ python3 src/integridad.py mac --clave "secreto" --mensaje "transferir 1000" --verificar <tag válido>
$ python3 src/integridad.py mac --clave "secreto" --mensaje "transferir 1000" --verificar <tag alterado>

Salida 1:
mensaje:      "transferir 1000"
HMAC-SHA256:  96bc66546d55627136aeaaefbcead75520a57e19539834d03e74d705b70ff9fe
tag recibido: 96bc66546d55627136aeaaefbcead75520a57e19539834d03e74d705b70ff9fe

TAG VÁLIDO — el mensaje es auténtico e íntegro.

Salida 2 (se cambiaron los dos últimos dígitos por gr):
HMAC-SHA256:  96bc66546d55627136aeaaefbcead75520a57e19539834d03e74d705b70ff9fe
tag recibido: 96bc66546d55627136aeaaefbcead75520a57e19539834d03e74d705b70ff9gr

TAG INVÁLIDO — el mensaje fue alterado o la clave no es la correcta.
```

---

## B.2 — Decisiones de implementación

_Qué decisiones tuvieron que tomar que el enunciado no resolvía por ustedes.
Ejemplos: cómo trataron los enlaces simbólicos, qué hicieron con los archivos
vacíos, cómo excluyeron el manifiesto del recorrido, qué pasa si el directorio
está vacío. Una o dos oraciones por decisión._

| Decisión                        | Qué hicimos                                                                                                                            | Por qué                                                                                                                                |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Enlaces simbólicos              | Excluimos los enlaces simbólicos del recorrido.                                                                                        | El manifiesto representa únicamente archivos regulares contenidos en el directorio y evita seguir referencias hacia archivos externos. |
| Exclusión del manifiesto        | Comparamos las rutas resueltas del archivo recorrido y del manifiesto antes de calcular el hash.                                       | Así evitamos que el manifiesto se incluya a sí mismo o aparezca como un archivo nuevo durante la verificación.                         |
| Directorio vacío                | Se devuelven las cuatro categorías aunque todas estén vacías.                                                                          | Mantiene siempre la misma estructura de retorno y permite verificar correctamente un directorio sin archivos.                          |
| Cálculo de distancia de Hamming | Comparamos los digests byte por byte mediante XOR y contamos la cantidad de bits diferentes.                                           | La consigna requiere medir la diferencia en bits, no solamente en bytes.                                                               |
| Comparación del tag             | Utilizamos hmac.compare_digest() en lugar de == para verificar el tag recibido.                                                        | compare_digest() está diseñado para realizar una comparación resistente a diferencias de tiempo y evitar filtraciones mediante timing. |
| Verificación opcional           | Si no se proporciona un tag esperado, calculamos y devolvemos solamente el HMAC; si se proporciona, además realizamos la verificación. | Permite utilizar la misma función tanto para generar un tag como para verificar uno recibido.                                          |

---

## B.3 — Preguntas de análisis

> **Se responden con fundamento técnico, no con opinión.** Dos o tres párrafos
> cada una. Las respuestas de una línea no suman puntos.

### 1. El manifiesto por sí solo no alcanza

_Un atacante con acceso de escritura al directorio también puede escribir
`manifest.sha256`. ¿Qué le impide modificar un archivo y regenerar el
manifiesto para que todo dé `OK`? ¿Qué habría que cambiar en el esquema para
que ese ataque no funcione?_

**Respuesta:**

Un manifiesto de hashes permite detectar modificaciones solamente si podemos confiar en que el propio manifiesto no fue alterado. Si un atacante tiene permisos para modificar tanto los archivos protegidos como manifest.sha256, nada le impide cambiar un archivo y luego regenerar el manifiesto con el nuevo hash. Al verificarlo posteriormente, el digest calculado coincidiría con el valor manipulado y el sistema informaría incorrectamente que la integridad está verificada.

Para evitarlo, el manifiesto debe protegerse de forma independiente. Por ejemplo, podría almacenarse en una ubicación de solo lectura para el atacante o autenticarse mediante un HMAC cuya clave secreta no esté disponible en el directorio protegido. Otra alternativa es firmarlo digitalmente manteniendo la clave privada fuera del alcance del atacante. De esta manera, modificar y regenerar el manifiesto ya no sería suficiente, porque el atacante también tendría que producir una autenticación o firma válida.

### 2. Qué agrega HMAC y qué no

_¿Qué propiedad de seguridad aporta HMAC que un hash simple no aporta? Y la
parte importante: ¿qué **no** resuelve HMAC? Pensá en el no repudio y en
quién conoce la clave._

**Respuesta:**

Un hash simple, como SHA-256, permite detectar modificaciones en un mensaje si se dispone de un hash de referencia que no pueda ser alterado por un atacante. Sin embargo, si un atacante puede modificar tanto el mensaje como el hash almacenado, puede recalcular el hash correspondiente y la modificación podría no ser detectada.

HMAC agrega una clave secreta compartida al proceso de autenticación. Por lo tanto, un atacante que no conozca la clave no puede generar un HMAC válido para un mensaje modificado. De esta forma, HMAC proporciona integridad y autenticación del mensaje.

HMAC no proporciona no repudio, porque las partes que conocen la misma clave secreta pueden generar tags válidos. Para obtener no repudio se utilizan mecanismos como las firmas digitales, donde la clave privada pertenece exclusivamente al firmante.

### 3. MD5 y SHA-1

_Ambos siguen apareciendo en software en producción. ¿Qué propiedad
criptográfica se les rompió, exactamente? ¿Hay algún uso en el que todavía
sean aceptables, o ninguno? Fundamentá con al menos una fuente._

**Respuesta:**

La propiedad criptográfica que se considera rota en MD5 y SHA-1 es la resistencia a colisiones, es posible construir dos mensajes diferentes que produzcan el mismo valor hash. En MD5 existen ataques prácticos de colisión desde hace años, por lo que RFC 6151 indica que no debe utilizarse cuando se requiere resistencia a colisiones.

En SHA-1 también se demostraron colisiones prácticas. NIST señala que esta debilidad afecta especialmente a aplicaciones como las firmas digitales, donde la resistencia a colisiones es fundamental, y recomienda migrar a SHA-2 o SHA-3.

Esto no significa que se hayan demostrado ataques de preimagen equivalentes para ambas funciones. En particular, RFC 6194 señala que no se conocían ataques de preimagen o segunda preimagen específicos contra SHA-1 completo; la debilidad relevante para su desuso criptográfico es la pérdida de resistencia a colisiones.

Todavía pueden existir usos no criptográficos o de compatibilidad con sistemas antiguos. Por ejemplo, RFC 6151 considera aceptable MD5 cuando se utiliza únicamente como checksum para detectar errores accidentales, no como mecanismo de seguridad. Para SHA-1, NIST permite ciertos usos heredados, como verificar firmas o timestamps antiguos, y algunos usos específicos como HMAC-SHA-1, aunque recomienda abandonar SHA-1 progresivamente. Para aplicaciones criptográficas nuevas, la recomendación es utilizar SHA-256/SHA-2 o SHA-3.

**Fuente:**

1. RFC 6151 — _Updated Security Considerations for the MD5 Message-Digest and the HMAC-MD5 Algorithms._ RFC 6151 — RFC Editor
2. NIST — _Transitioning Away from SHA-1 for All Applications._ NIST — SHA-1 transition

### 4. Comparación en tiempo constante

_¿Por qué comparar un tag de autenticación con `==` puede filtrar información
al atacante, y cómo lo evita `hmac.compare_digest()`? Describí el ataque
concreto que esto previene._

**Respuesta:**

Se utiliza hmac.compare_digest() para comparar el HMAC calculado con el tag recibido porque está diseñado para realizar comparaciones resistentes a ataques basados en diferencias de tiempo. Una comparación convencional mediante == puede finalizar antes cuando encuentra una diferencia, lo que potencialmente puede generar variaciones observables en el tiempo de ejecución.

Por ello, en la verificación del HMAC utilizamos hmac.compare_digest() en lugar de ==, reduciendo el riesgo de filtración de información mediante un ataque de timing. Esto se refiere específicamente a la comparación del tag y no significa que todo el programa ejecute todas sus operaciones en tiempo constante.

### 5. SHA-256 para contraseñas: mala idea

_SHA-256 es una función de hash criptográfica sólida. ¿Por qué, entonces, es
una mala elección para almacenar contraseñas? ¿Qué se usa en su lugar y qué
propiedad tienen esas funciones que SHA-256 no tiene?_

**Respuesta:**

Aunque SHA-256 es una función de hash criptográfica robusta para garantizar la integridad de datos y verificar firmas digitales (resistente a colisiones y preimágenes), resulta una **pésima elección para el almacenamiento de contraseñas**. La razón fundamental radica en que SHA-256 fue expresamente diseñada para ser **computacionalmente rápida y altamente eficiente en hardware**. Dado que las contraseñas elegidas por humanos poseen una entropía intrínsecamente baja, un atacante que obtenga una base de datos de hashes puede aprovechar esta velocidad para ejecutar ataques masivos de fuerza bruta, ataques por diccionario y búsquedas con tablas arcoíris (_rainbow tables_). Utilizando hardware paralelo moderno (como clústeres de GPUs, FPGAs o circuitos integrados dedicados ASICs), un atacante puede calcular **miles de millones de hashes SHA-256 por segundo por dispositivo**, descifrando contraseñas comunes o de longitud media en cuestión de segundos o minutos. Además, un hash simple no incluye intrínsecamente un mecanismo obligatorio de _salt_, lo que permite atacar múltiples usuarios a la vez si no se gestiona manualmente.

En su lugar, los estándares modernos de seguridad exigen el uso de **funciones de derivación de claves basadas en contraseñas (KDF)** y algoritmos especializados de hashing de contraseñas, tales como **Argon2id** (estándar recomendado por la _Password Hashing Competition_ e IETF RFC 9106), **bcrypt** (basado en el algoritmo Eksblowfish), **scrypt** y **PBKDF2**.

Estas funciones poseen tres propiedades esenciales que SHA-256 no tiene:

1. **Factor de trabajo / lentitud configurable (_Work Factor / Cost Parameter_):** Permiten ajustar deliberadamente la cantidad de iteraciones y el tiempo de cómputo necesario para calcular un único hash. Esto permite calibrar el sistema para que verificar un intento de inicio de sesión legítimo tome una fracción de segundo imperceptible para el usuario en el servidor (ej. 100 a 300 ms), pero vuelva computacionalmente inviable para un atacante probar billones de combinaciones. Este parámetro de costo puede incrementarse en el tiempo a medida que el hardware de los atacantes se vuelve más potente.
2. **Dureza de memoria (_Memory-Hardness_):** Algoritmos como Argon2id y scrypt requieren grandes cantidades de memoria RAM rápida para cada cálculo de hash. Esta característica neutraliza la ventaja de las GPUs y ASICs masivos (que poseen miles de núcleos pero muy poca memoria rápida local por hilo), haciendo que la construcción de hardware paralelo para ataques de fuerza bruta sea económicamente prohibitiva.
3. **Salteado automático e intrínseco (_Built-in Salting_):** Integran por diseño la generación y almacenamiento de un _salt_ criptográfico aleatorio único por cada contraseña en la propia cadena del hash. Esto garantiza que dos usuarios con la misma contraseña generen hashes completamente distintos y anula por completo la eficacia de ataques precalculados mediante tablas arcoíris.

---

# Cierre

## Dificultades encontradas

- **Integración de fuentes primarias y rigor histórico/técnico:** En la investigación sobre el Morris Worm y en el mini-research de disponibilidad, la principal dificultad fue filtrar el material de divulgación periodística para centrarse exclusivamente en fuentes primarias, documentos judiciales (_United States v. Morris_), estándares oficiales (NIST SP 800-34 Rev. 1, guías de CISA) y literatura académica arbitrada.
- **Comprensión de la distancia de Hamming sobre bits crudos:** En la implementación práctica de la Parte B, fue fundamental distinguir el cálculo de bits sobre los bytes devueltos por `digest()` frente a los caracteres hexadecimales de `hexdigest()`, evitando desvirtuar el concepto criptográfico del efecto avalancha.
- **Análisis de tiempo constante:** El estudio de ataques de canal lateral (_timing attacks_) permitió comprender por qué la comparación byte a byte mediante `==` expone información crítica y por qué es mandatorio utilizar `hmac.compare_digest()`.

---

## Distribución del trabajo

| Integrante                               | Aportes                                                                                                                                                                                                                       |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Alejo De Miguel (@AlejoDM)               | Parte A, apertura: Investigación histórica del Morris Worm, redacción de A.1 (Cronología verificada) y A.2 (Activo afectado y justificación).                                                                                 |
| María Belén Benito (@belubenito603-byte) | Parte A, cierre: Matriz CIA (A.3), Encadenamiento amenaza→vulnerabilidad→activo→impacto (A.4), Controles mitigantes específicos (A.5) y Fuentes A.6.                                                                          |
| Tomás Giudici (@TomasGiudici)            | Parte B, manifiesto: Implementación de `generar_manifiesto` y `verificar_manifiesto` en `src/integridad.py`, captura de evidencias obligatorias (manifiesto, verificación, prueba de 1 byte), decisiones de B.2 y Pregunta 1. |
| Carolina Suppo (@carosuppo)              | Parte B, criptografía: Implementación de `distancia_hamming_bits` y `calcular_mac` en `src/integridad.py`, captura de evidencias (avalancha y HMAC), decisiones de B.2 y Preguntas de análisis 2, 3 y 4.                      |
| Martín Beccereca (@martinbeccereca)      | Mini-research (Tema 3: Disponibilidad y Ransomware), Pregunta de análisis 5 (SHA-256 vs KDFs para contraseñas), armado de `INTEGRANTES.md`, coordinación y cierre del informe, verificación contra rúbrica.                   |

---

## Declaración de uso de asistentes de IA

**¿El grupo usó asistentes de IA en este trabajo?** Sí

| Herramienta                                           | Para qué se usó                                                                | Qué partes del entregable afectó                                         | Cómo se verificó que lo devuelto era correcto                                                                                                                     |
| ----------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Gemini 3.7 Flash / Gemini Deep Research / Claude Code | Redacción, estructuración y asistencia analítica en el informe y mini-research | A.1, A.2, Pregunta B.5, Mini-research (research.md), secciones de cierre | Cada fuente, cita bibliográfica, cálculo y concepto técnico fue verificado accediendo a los textos primarios originales y corriendo las pruebas correspondientes. |

**Declaración:**

El grupo declara que comprende el contenido íntegro de lo entregado y que
puede explicar y defender oralmente cualquier parte del código y del análisis,
independientemente de la asistencia recibida.

---

## Fuentes consultadas (general)

1. United States v. Morris, 928 F.2d 504 (2d Cir. 1991).
   https://law.resource.org/pub/us/case/reporter/F2/928/928.F2d.504.90-1336.774.html
2. Carnegie Mellon University, Software Engineering Institute. (s.f.). _History
   of Innovation_. https://www.sei.cmu.edu/history-of-innovation/
3. Lawrence Livermore National Laboratory. (s.f.). _The 1988 Morris worm, the
   internet's first cyberattack_.
   https://st.llnl.gov/news/look-back/1988-morris-worm-internets-first-cyberattack
4. Cybersecurity and Infrastructure Security Agency, & Federal Bureau of Investigation. (2023). _#StopRansomware Guide_. CISA. https://www.cisa.gov/sites/default/files/2023-05/StopRansomware_Guide_508c%20(1).pdf
5. National Institute of Standards and Technology. (2010). _Contingency Planning Guide for Federal Information Systems_ (NIST Special Publication 800-34, Rev. 1). U.S. Department of Commerce. https://doi.org/10.6028/NIST.SP.800-34r1
6. Cartwright, A., Cartwright, E., & Webb, J. (2020). An economic analysis of ransomware and its welfare consequences. _Royal Society Open Science_, 7(3), 190023. https://doi.org/10.1098/rsos.190023
7. Samonas, S., & Coss, D. (2014). The CIA strikes back: Redefining confidentiality, integrity and availability in security. _Journal of Information System Security_, 10(3), 21-45. https://www.researchgate.net/publication/317011931_The_CIA_strikes_back_Redefining_confidentiality_integrity_and_availability_in_security
8. Biryukov, A., Dinu, D., & Khovratovich, D. (2016). _Argon2: New Generation of Memory-Hard Functions for Password Hashing and Other Applications_. In 2016 IEEE European Symposium on Security and Privacy (EuroS&P) (pp. 292-302). IEEE. https://doi.org/10.1109/EuroSP.2016.31
