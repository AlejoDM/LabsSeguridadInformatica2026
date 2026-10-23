# Informe — Laboratorio 10 · Detección y evasión

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

**Herramienta:** Claude Code.

- **Finalidad del uso:** apoyo para acceder a la vista `/soc` y capturar su línea base antes de cualquier prueba del grupo, y para redactar la estructura inicial del informe, la fila de R1 en la tabla de flags, el contexto de la vista del SOC y la respuesta a P1.
- **Partes asistidas:** estructura de `entregas/lab10/grupo06/`, fila "R1 — Vista inicial del SOC" en la tabla de flags, subsección "Contexto de la vista `/soc`" y respuesta a P1.
- **Verificación:** la consulta a `/soc` se ejecutó con `curl` de solo lectura contra `phantomcorp`, dentro del contenedor `cyberlab-attacker`, antes de generar cualquier tráfico de prueba; la salida se guardó cruda y sin editar en `evidencia/salidas/`. La respuesta a P1 describe limitaciones generales de la detección por firma, citando únicamente lo que el ruleset del lab ya hace explícito en el enunciado de R4 (el espacio exigido por `sqli-union`), sin adelantar trabajo de R2-R5 que corresponde a otros responsables. Se revisó el contenido antes de incorporarlo.

## 1. Flags capturadas (salida de `./ctf status 10`)

*Pendiente de completar cuando se resuelvan los 5 retos.*

| Reto | Estado | Evidencia |
|---|---|---|
| R1 — Vista inicial del SOC | Obtenida | [Línea base del SOC](evidencia/salidas/r1-soc-inicial.txt) y [envío de R1](evidencia/salidas/r1-submit.txt) |

### Contexto de la vista `/soc` (línea base, R1)

`GET /soc` devuelve, antes de cualquier prueba del grupo, 120 líneas de tráfico más el mensaje de acceso con la flag de R1. Cada línea tiene la estructura `<origen> - <método> <ruta> <código> <etiqueta>`: una IP de origen, el verbo y la ruta solicitados, el código HTTP de respuesta y una etiqueta `BENIGN` o `ALERT[<firma>]` con, en algunos casos, un comentario adicional. Esta línea base es la referencia contra la que se compara todo lo que el grupo genere después: cualquier evento nuevo que aparezca tras una prueba propia debe poder explicarse por esa prueba, y todo lo que no se explique así es candidato a intrusión real (R5).

## 2. Tabla de firmas

| Firma | Cómo se evade | Cómo se mejora la detección |
|---|---|---|
| scanner-ua | | |
| sqli-union | | |

## 3. Preguntas P1–P5

**P1.** ¿Por qué la detección por firmas es evadible por diseño? ¿Qué la complementa?

Una firma detecta una **cadena o patrón concreto**, no la intención ni el efecto de una acción. Para que funcione, el defensor tiene que anticipar de antemano exactamente qué forma va a tener el ataque: un User-Agent, una secuencia literal como `UNION SELECT `, una ruta. El problema es que casi siempre existen muchas formas distintas de lograr el mismo efecto sin que ninguna de ellas calce con la cadena exacta que la regla busca. En R4, por ejemplo, el ruleset de este lab exige un espacio después de `UNION SELECT` para disparar la firma `sqli-union`; para el intérprete SQL, un espacio y un comentario `/**/` son equivalentes como separador, pero para una regla que busca el carácter espacio literal, no lo son. La firma es evadible porque codifica una **forma superficial** del ataque, no su significado.

Esto no es un defecto corregible de una vez: es una limitación estructural de cualquier sistema que decida "coincide / no coincide" contra un conjunto finito de patrones conocidos. Siempre va a quedar afuera alguna variante sintáctica, codificación o transformación que un atacante puede probar. Por eso la detección por firma nunca debería ser la única capa. Se complementa con: (a) **validación y parametrización en la aplicación**, que elimina la causa raíz en vez de solo detectar el síntoma; (b) **normalización/canonicalización** de la entrada antes de aplicar la firma, para que variantes de encoding o espaciado converjan a una forma comparable; (c) **detección por comportamiento y correlación**, que mira patrones de uso (frecuencia, secuencia de endpoints, volumen) en vez de una cadena puntual, y que es precisamente lo que permite encontrar la intrusión de R5 aunque no dispare ninguna firma puntual; y (d) **revisión humana**, porque ninguna de las capas anteriores sustituye el criterio de alguien que mire el log completo y note lo que no encaja.

**P2.** La firma `sqli-union` exigía un espacio. Reescribí la regla para que NO se evada con `/**/`. ¿Se puede hacer una firma "perfecta"?

**P3.** Detectar por User-Agent: ¿por qué es una detección débil? ¿Qué mirarías en lugar de "quién dice ser"?

**P4.** El R5: la intrusión estaba en el log. ¿Qué habría hecho que se detecte automáticamente y no dependiera de que alguien la mire?

**P5.** Cierre del curso: recorriste ataque (05–08), agentes (09) y defensa (10). ¿Qué cambió en cómo pensás la seguridad?

## 4. Bitácora
