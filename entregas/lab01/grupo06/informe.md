# Laboratorio 01 — Informe

---

## Identificación

| | |
|---|---|
| **Grupo** | 06 |
| **Caso asignado (Parte A)** | Morris Worm (1988) |
| **Tema del mini-research** | |
| **Fecha de entrega** | |

### Integrantes

| Nombre y apellido | Legajo | Usuario de GitHub |
|---|---|---|
| Martín Beccereca | | @martinbeccereca |
| María Belén Benito | | @ |
| Alejo De Miguel | | @AlejoDM |
| Tomás Giudici | | @ |
| Carolina Suppo | | @ |

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

---

# Cierre

## Dificultades encontradas

*Qué les costó, dónde se trabaron, qué decidieron y por qué. Esta sección se
lee y suma. No es relleno: es donde se ve si entendieron el problema.*

---

## Distribución del trabajo

*Quién hizo qué. Tiene que ser consistente con el historial de commits.*

| Integrante | Aportes |
|---|---|
| | |
| | |
| | |
| | |
| | |

---

## Declaración de uso de asistentes de IA

**¿El grupo usó asistentes de IA en este trabajo?** Sí

| Herramienta | Para qué se usó | Qué partes del entregable afectó | Cómo se verificó que lo devuelto era correcto |
|---|---|---|---|
| Claude Code | Redacción del informe del laboratorio | A.1 — Cronología y A.2 — Activo afectado | Cada fuente fue consultada antes de redactarla |

**Declaración:**

El grupo declara que comprende el contenido íntegro de lo entregado y que
puede explicar y defender oralmente cualquier parte del código y del análisis,
independientemente de la asistencia recibida.

---

## Fuentes consultadas (general)

*Las fuentes de la Parte B, Mini-research y demás secciones las agregan
Personas 2 a 5 a continuación de esta lista.*

1. United States v. Morris, 928 F.2d 504 (2d Cir. 1991).
   https://law.resource.org/pub/us/case/reporter/F2/928/928.F2d.504.90-1336.774.html
2. Carnegie Mellon University, Software Engineering Institute. (s.f.). *History
   of Innovation*. https://www.sei.cmu.edu/history-of-innovation/
3. Lawrence Livermore National Laboratory. (s.f.). *The 1988 Morris worm, the
   internet's first cyberattack*.
   https://st.llnl.gov/news/look-back/1988-morris-worm-internets-first-cyberattack
