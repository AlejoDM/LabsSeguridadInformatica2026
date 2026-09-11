# Laboratorio 01 — Informe

---

## Identificación

| | |
|---|---|
| **Grupo** | 06 |
| **Caso asignado (Parte A)** | Morris Worm (1988) |
| **Tema del mini-research** | Tema 3 — La disponibilidad, la propiedad descuidada de la tríada |
| **Fecha de entrega** | |

### Integrantes

| Nombre y apellido | Legajo | Usuario de GitHub |
|---|---|---|
| Martín Beccereca | 15154 | @martinbeccereca |
| María Belén Benito | 14625 | @belubenito603-byte |
| Alejo De Miguel | 15138 | @AlejoDM |
| Tomás Giudici | 14977 | @TomasGiudici |
| Carolina Suppo | 15057 | @carosuppo |

---

# PARTE A — Análisis del incidente bajo la lente CIA

## A.1 — Cronología

| Fecha | Hecho | Fuente |
|---|---|---|
| 1988-11-02 (noche) | Robert Tappan Morris, estudiante de posgrado de Cornell, libera el gusano desde una máquina del MIT para disimular su origen real. | [*United States v. Morris*, 928 F.2d 504 (2d Cir. 1991)](https://law.resource.org/pub/us/case/reporter/F2/928/928.F2d.504.90-1336.774.html) |
| 1988-11-02/03 | El gusano se propaga explotando cuatro vectores: un bug en el modo debug de `sendmail`, un desbordamiento en `fingerd`, la función de "trusted hosts" (`rsh`/`rexec`) y adivinación de contraseñas. | [*United States v. Morris*, 928 F.2d 504 (2d Cir. 1991)](https://law.resource.org/pub/us/case/reporter/F2/928/928.F2d.504.90-1336.774.html) |
| 1988-11 (horas siguientes) | Un error en su lógica de reinfección (probabilidad de re-copiarse aun en máquinas ya infectadas) provoca que se acumulen decenas de procesos por host, agotando CPU y memoria; ~6.000 de los ~60.000 hosts conectados a Internet (~10 %) quedan afectados. | [Lawrence Livermore National Laboratory, *"The 1988 Morris worm, the internet's first cyberattack"*](https://st.llnl.gov/news/look-back/1988-morris-worm-internets-first-cyberattack) |
| 1988-11 (días siguientes) | DARPA encarga al Software Engineering Institute de Carnegie Mellon la creación de un centro de coordinación de emergencias informáticas; nace así el CERT/CC, en respuesta directa a este incidente. | [Carnegie Mellon University SEI, *"History of Innovation"*](https://www.sei.cmu.edu/history-of-innovation/) |
| 1990-05-16 | El tribunal de distrito (juez Howard G. Munson, Distrito Norte de Nueva York) dicta sentencia: 3 años de libertad condicional, 400 horas de servicio comunitario y una multa de USD 10.050. | [*United States v. Morris*, 928 F.2d 504 (2d Cir. 1991)](https://law.resource.org/pub/us/case/reporter/F2/928/928.F2d.504.90-1336.774.html) |
| 1991-03-07 | La Corte de Apelaciones del Segundo Circuito confirma la condena, convirtiendo el caso en la primera confirmada bajo la Computer Fraud and Abuse Act de 1986. | [*United States v. Morris*, 928 F.2d 504 (2d Cir. 1991)](https://law.resource.org/pub/us/case/reporter/F2/928/928.F2d.504.90-1336.774.html) |

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
lo resume así: *"the Morris worm did not damage or destroy files, it slowed
systems to a crawl"* — es decir, el efecto es enteramente sobre
disponibilidad, no sobre confidencialidad ni integridad de ningún dato. Los
cuatro vectores de propagación (bug de `sendmail`, bug de `fingerd`,
"trusted hosts" y adivinación de contraseñas) documentados en [*United
States v. Morris*](https://law.resource.org/pub/us/case/reporter/F2/928/928.F2d.504.90-1336.774.html)
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

*Una fila por propiedad. La columna «Evidencia» tiene que citar un hecho
concreto del incidente, no una generalidad.*

> **Advertencia.** «No» es una respuesta válida y muchas veces la correcta.
> El error típico es marcar las tres propiedades en «Sí» porque el incidente
> fue grave. La gravedad no es una propiedad de la tríada. Si marcás que se
> violó la integridad, tenés que mostrar **qué dato específico fue alterado**.
> Si no podés mostrarlo, la respuesta es «No».

| Propiedad | ¿Se violó? | Evidencia concreta |
|---|---|---|
| **Confidencialidad** | Sí / No / Parcial | |
| **Integridad** | Sí / No / Parcial | |
| **Disponibilidad** | Sí / No / Parcial | |

**Justificación ampliada de la propiedad más discutible:**

*De las tres, ¿cuál fue la más difícil de determinar y por qué? Desarrollá.*

---

## A.4 — Encadenamiento amenaza → vulnerabilidad → impacto

*Redacción en prosa, no viñetas. Usá los términos con precisión: una amenaza
no es una vulnerabilidad, un exploit no es una vulnerabilidad, y el impacto
no es el ataque.*

```
amenaza  →  explota  →  vulnerabilidad  →  sobre  →  activo  →  produce  →  impacto
```

| Elemento | En este caso |
|---|---|
| **Amenaza** *(quién / qué, con qué motivación)* | |
| **Vulnerabilidad** *(la debilidad concreta que se explotó)* | |
| **Activo** *(sobre qué recayó)* | |
| **Impacto** *(consecuencia sobre el negocio o las personas)* | |

**Redacción:**

*Un párrafo que encadene los cuatro elementos anteriores.*

---

## A.5 — Dos controles mitigantes

*Controles que, de haber estado implementados, habrían evitado o reducido el
incidente. Específicos y justificados contra **este** caso. «Tener antivirus»
o «capacitar a los usuarios» no califica.*

### Control 1

| | |
|---|---|
| **Qué es** | |
| **Propiedad de la tríada que protege** | |
| **Por qué habría funcionado en este caso concreto** | |

### Control 2

| | |
|---|---|
| **Qué es** | |
| **Propiedad de la tríada que protege** | |
| **Por qué habría funcionado en este caso concreto** | |

---

## A.6 — Fuentes consultadas (Parte A)

*Formato APA. Indicá para cada una si es primaria (informe oficial, documento
del fabricante, resolución judicial, paper) o secundaria (nota periodística,
entrada de blog).*

1.
2.
3.

---

# PARTE B — Integridad con funciones de hash

## B.1 — Evidencia de ejecución

*Pegá la salida real de cada comando. No la transcribas a mano: copiala tal
cual sale de la terminal.*

### Generación del manifiesto

```
$ python3 src/integridad.py generar --dir data/muestra --salida manifest.sha256

(pegar salida)
```

### Verificación sobre un directorio íntegro

```
$ python3 src/integridad.py verificar --dir data/muestra --manifiesto manifest.sha256
$ echo "código de salida: $?"

(pegar salida)
```

### Detección de la modificación de un byte

*Esta prueba es obligatoria y tiene una penalización específica en la rúbrica
si falla.*

```
$ printf 'X' >> data/muestra/transferencia.txt
$ python3 src/integridad.py verificar --dir data/muestra --manifiesto manifest.sha256
$ echo "código de salida: $?"

(pegar salida — debe reportar MODIFICADO y salir con 1)
```

### Detección de archivo faltante y de archivo nuevo

```
(pegar los comandos que usaron y la salida)
```

### Efecto avalancha

```
$ python3 src/integridad.py avalancha --a "transferencia: $1000" --b "transferencia: $1001"

(pegar salida)
```

**Distancia obtenida:** ____ bits de 256 (____ %)

*¿Coincide con lo esperado? ¿Qué esperaban antes de correrlo?*

### HMAC

```
$ python3 src/integridad.py mac --clave "secreto" --mensaje "transferir 1000"

(pegar salida)
```

```
$ python3 src/integridad.py mac --clave "secreto" --mensaje "transferir 1000" --verificar <tag válido>
$ python3 src/integridad.py mac --clave "secreto" --mensaje "transferir 1000" --verificar <tag alterado>

(pegar ambas salidas)
```

---

## B.2 — Decisiones de implementación

*Qué decisiones tuvieron que tomar que el enunciado no resolvía por ustedes.
Ejemplos: cómo trataron los enlaces simbólicos, qué hicieron con los archivos
vacíos, cómo excluyeron el manifiesto del recorrido, qué pasa si el directorio
está vacío. Una o dos oraciones por decisión.*

| Decisión | Qué hicimos | Por qué |
|---|---|---|
| | | |
| | | |

---

## B.3 — Preguntas de análisis

> **Se responden con fundamento técnico, no con opinión.** Dos o tres párrafos
> cada una. Las respuestas de una línea no suman puntos.

### 1. El manifiesto por sí solo no alcanza

*Un atacante con acceso de escritura al directorio también puede escribir
`manifest.sha256`. ¿Qué le impide modificar un archivo y regenerar el
manifiesto para que todo dé `OK`? ¿Qué habría que cambiar en el esquema para
que ese ataque no funcione?*

**Respuesta:**

---

### 2. Qué agrega HMAC y qué no

*¿Qué propiedad de seguridad aporta HMAC que un hash simple no aporta? Y la
parte importante: ¿qué **no** resuelve HMAC? Pensá en el no repudio y en
quién conoce la clave.*

**Respuesta:**

---

### 3. MD5 y SHA-1

*Ambos siguen apareciendo en software en producción. ¿Qué propiedad
criptográfica se les rompió, exactamente? ¿Hay algún uso en el que todavía
sean aceptables, o ninguno? Fundamentá con al menos una fuente.*

**Respuesta:**

**Fuente:**

---

### 4. Comparación en tiempo constante

*¿Por qué comparar un tag de autenticación con `==` puede filtrar información
al atacante, y cómo lo evita `hmac.compare_digest()`? Describí el ataque
concreto que esto previene.*

**Respuesta:**

---

### 5. SHA-256 para contraseñas: mala idea

*SHA-256 es una función de hash criptográfica sólida. ¿Por qué, entonces, es
una mala elección para almacenar contraseñas? ¿Qué se usa en su lugar y qué
propiedad tienen esas funciones que SHA-256 no tiene?*

**Respuesta:**

Aunque SHA-256 es una función de hash criptográfica robusta para garantizar la integridad de datos y verificar firmas digitales (resistente a colisiones y preimágenes), resulta una **pésima elección para el almacenamiento de contraseñas**. La razón fundamental radica en que SHA-256 fue expresamente diseñada para ser **computacionalmente rápida y altamente eficiente en hardware**. Dado que las contraseñas elegidas por humanos poseen una entropía intrínsecamente baja, un atacante que obtenga una base de datos de hashes puede aprovechar esta velocidad para ejecutar ataques masivos de fuerza bruta, ataques por diccionario y búsquedas con tablas arcoíris (*rainbow tables*). Utilizando hardware paralelo moderno (como clústeres de GPUs, FPGAs o circuitos integrados dedicados ASICs), un atacante puede calcular **miles de millones de hashes SHA-256 por segundo por dispositivo**, descifrando contraseñas comunes o de longitud media en cuestión de segundos o minutos. Además, un hash simple no incluye intrínsecamente un mecanismo obligatorio de *salt*, lo que permite atacar múltiples usuarios a la vez si no se gestiona manualmente.

En su lugar, los estándares modernos de seguridad exigen el uso de **funciones de derivación de claves basadas en contraseñas (KDF)** y algoritmos especializados de hashing de contraseñas, tales como **Argon2id** (estándar recomendado por la *Password Hashing Competition* e IETF RFC 9106), **bcrypt** (basado en el algoritmo Eksblowfish), **scrypt** y **PBKDF2**.

Estas funciones poseen tres propiedades esenciales que SHA-256 no tiene:

1. **Factor de trabajo / lentitud configurable (*Work Factor / Cost Parameter*):** Permiten ajustar deliberadamente la cantidad de iteraciones y el tiempo de cómputo necesario para calcular un único hash. Esto permite calibrar el sistema para que verificar un intento de inicio de sesión legítimo tome una fracción de segundo imperceptible para el usuario en el servidor (ej. 100 a 300 ms), pero vuelva computacionalmente inviable para un atacante probar billones de combinaciones. Este parámetro de costo puede incrementarse en el tiempo a medida que el hardware de los atacantes se vuelve más potente.
2. **Dureza de memoria (*Memory-Hardness*):** Algoritmos como Argon2id y scrypt requieren grandes cantidades de memoria RAM rápida para cada cálculo de hash. Esta característica neutraliza la ventaja de las GPUs y ASICs masivos (que poseen miles de núcleos pero muy poca memoria rápida local por hilo), haciendo que la construcción de hardware paralelo para ataques de fuerza bruta sea económicamente prohibitiva.
3. **Salteado automático e intrínseco (*Built-in Salting*):** Integran por diseño la generación y almacenamiento de un *salt* criptográfico aleatorio único por cada contraseña en la propia cadena del hash. Esto garantiza que dos usuarios con la misma contraseña generen hashes completamente distintos y anula por completo la eficacia de ataques precalculados mediante tablas arcoíris.

---

# Cierre

## Dificultades encontradas

- **Integración de fuentes primarias y rigor histórico/técnico:** En la investigación sobre el Morris Worm y en el mini-research de disponibilidad, la principal dificultad fue filtrar el material de divulgación periodística para centrarse exclusivamente en fuentes primarias, documentos judiciales (*United States v. Morris*), estándares oficiales (NIST SP 800-34 Rev. 1, guías de CISA) y literatura académica arbitrada.
- **Comprensión de la distancia de Hamming sobre bits crudos:** En la implementación práctica de la Parte B, fue fundamental distinguir el cálculo de bits sobre los bytes devueltos por `digest()` frente a los caracteres hexadecimales de `hexdigest()`, evitando desvirtuar el concepto criptográfico del efecto avalancha.
- **Análisis de tiempo constante:** El estudio de ataques de canal lateral (*timing attacks*) permitió comprender por qué la comparación byte a byte mediante `==` expone información crítica y por qué es mandatorio utilizar `hmac.compare_digest()`.

---

## Distribución del trabajo

| Integrante | Aportes |
|---|---|
| Alejo De Miguel (@AlejoDM) | Parte A, apertura: Investigación histórica del Morris Worm, redacción de A.1 (Cronología verificada) y A.2 (Activo afectado y justificación). |
| María Belén Benito (@belubenito603-byte) | Parte A, cierre: Matriz CIA (A.3), Encadenamiento amenaza→vulnerabilidad→activo→impacto (A.4), Controles mitigantes específicos (A.5) y Fuentes A.6. |
| Tomás Giudici (@TomasGiudici) | Parte B, manifiesto: Implementación de `generar_manifiesto` y `verificar_manifiesto` en `src/integridad.py`, captura de evidencias obligatorias (manifiesto, verificación, prueba de 1 byte), decisiones de B.2 y Pregunta 1. |
| Carolina Suppo (@carosuppo) | Parte B, criptografía: Implementación de `distancia_hamming_bits` y `calcular_mac` en `src/integridad.py`, captura de evidencias (avalancha y HMAC), decisiones de B.2 y Preguntas de análisis 2, 3 y 4. |
| Martín Beccereca (@martinbeccereca) | Mini-research (Tema 3: Disponibilidad y Ransomware), Pregunta de análisis 5 (SHA-256 vs KDFs para contraseñas), armado de `INTEGRANTES.md`, coordinación y cierre del informe, verificación contra rúbrica. |

---

## Declaración de uso de asistentes de IA

**¿El grupo usó asistentes de IA en este trabajo?** Sí

| Herramienta | Para qué se usó | Qué partes del entregable afectó | Cómo se verificó que lo devuelto era correcto |
|---|---|---|---|
| Gemini 3.7 Flash / Gemini Deep Research / Claude Code | Redacción, estructuración y asistencia analítica en el informe y mini-research | A.1, A.2, Pregunta B.5, Mini-research (research.md), secciones de cierre | Cada fuente, cita bibliográfica, cálculo y concepto técnico fue verificado accediendo a los textos primarios originales y corriendo las pruebas correspondientes. |

**Declaración:**

El grupo declara que comprende el contenido íntegro de lo entregado y que
puede explicar y defender oralmente cualquier parte del código y del análisis,
independientemente de la asistencia recibida.

---

## Fuentes consultadas (general)

1. United States v. Morris, 928 F.2d 504 (2d Cir. 1991).
   https://law.resource.org/pub/us/case/reporter/F2/928/928.F2d.504.90-1336.774.html
2. Carnegie Mellon University, Software Engineering Institute. (s.f.). *History
   of Innovation*. https://www.sei.cmu.edu/history-of-innovation/
3. Lawrence Livermore National Laboratory. (s.f.). *The 1988 Morris worm, the
   internet's first cyberattack*.
   https://st.llnl.gov/news/look-back/1988-morris-worm-internets-first-cyberattack
4. Cybersecurity and Infrastructure Security Agency, & Federal Bureau of Investigation. (2023). *#StopRansomware Guide*. CISA. https://www.cisa.gov/sites/default/files/2023-05/StopRansomware_Guide_508c%20(1).pdf
5. National Institute of Standards and Technology. (2010). *Contingency Planning Guide for Federal Information Systems* (NIST Special Publication 800-34, Rev. 1). U.S. Department of Commerce. https://doi.org/10.6028/NIST.SP.800-34r1
6. Cartwright, A., Cartwright, E., & Webb, J. (2020). An economic analysis of ransomware and its welfare consequences. *Royal Society Open Science*, 7(3), 190023. https://doi.org/10.1098/rsos.190023
7. Samonas, S., & Coss, D. (2014). The CIA strikes back: Redefining confidentiality, integrity and availability in security. *Journal of Information System Security*, 10(3), 21-45. https://www.researchgate.net/publication/317011931_The_CIA_strikes_back_Redefining_confidentiality_integrity_and_availability_in_security
8. Biryukov, A., Dinu, D., & Khovratovich, D. (2016). *Argon2: New Generation of Memory-Hard Functions for Password Hashing and Other Applications*. In 2016 IEEE European Symposium on Security and Privacy (EuroS&P) (pp. 292-302). IEEE. https://doi.org/10.1109/EuroSP.2016.31

