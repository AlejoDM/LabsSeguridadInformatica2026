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

**Herramienta:** Codex (OpenAI).

- **Finalidad del uso:** apoyo para ejecutar y documentar R2 dentro del contenedor autorizado, y para redactar la fila `scanner-ua` y la respuesta P2.
- **Partes asistidas:** evidencia de la alerta R2, registro de la flag, tabla de firmas para `scanner-ua`, respuesta P2 y bitácora.
- **Verificación:** la solicitud usó únicamente `curl -A sqlmap http://phantomcorp/` desde `cyberlab-attacker`; se contrastó el texto del informe contra la respuesta HTTP cruda y el verificador oficial.

**Herramienta:** Codex (OpenAI).

**Finalidad y partes asistidas:** apoyo para la ejecución de R3 y revisión limitada del aporte P2.
**Verificación realizada:** contraste con el ruleset HTTP real, aceptación de la flag por el motor oficial y comprobaciones locales de la expresión propuesta.

## 1. Flags capturadas (salida de `./ctf status 10`)

*Pendiente de completar cuando se resuelvan los 5 retos.*

| Reto | Estado | Evidencia |
|---|---|---|
| R1 — Vista inicial del SOC | Obtenida | [Línea base del SOC](evidencia/salidas/r1-soc-inicial.txt) y [envío de R1](evidencia/salidas/r1-submit.txt) |
| R3 — Ruleset publicado | Obtenida y aceptada en esta sesión | [Ruleset original](evidencia/salidas/r3-ruleset.txt), [envío R3](evidencia/salidas/r3-submit.txt) y [estado parcial](evidencia/salidas/status-10-p3.txt) |
| R2 — Detección por User-Agent | Obtenida | [Respuesta y alerta `scanner-ua`](evidencia/salidas/r2-scanner-ua.txt) y [envío de R2](evidencia/salidas/r2-submit.txt) |

### Contexto de la vista `/soc` (línea base, R1)

`GET /soc` devuelve, antes de cualquier prueba del grupo, 120 líneas de tráfico más el mensaje de acceso con la flag de R1. Cada línea tiene la estructura `<origen> - <método> <ruta> <código> <etiqueta>`: una IP de origen, el verbo y la ruta solicitados, el código HTTP de respuesta y una etiqueta `BENIGN` o `ALERT[<firma>]` con, en algunos casos, un comentario adicional. Esta línea base es la referencia contra la que se compara todo lo que el grupo genere después: cualquier evento nuevo que aparezca tras una prueba propia debe poder explicarse por esa prueba, y todo lo que no se explique así es candidato a intrusión real (R5).

## 2. Tabla de firmas

| Firma | Cómo se evade | Cómo se mejora la detección |
|---|---|---|
| scanner-ua | La detección observada depende de que el cliente declare literalmente `sqlmap`; por lo tanto, un atacante podría declarar una User-Agent de navegador y evitar esta firma aislada. Esto describe una limitación del control dentro del laboratorio; no se realizó esa prueba de evasión. | No usar la User-Agent como decisión única. El ruleset R3 publica coincidencias con `sqlmap|nikto|nmap|dirb`; no acredita herramientas reales ni intención. Conservarla como señal de baja confianza y correlacionarla con método/ruta, errores, velocidad y variedad de requests, parámetros anómalos y secuencias de enumeración. Aplicar límites de tasa y detecciones de comportamiento, y corregir la vulnerabilidad de la aplicación para que una solicitud sospechosa no implique compromiso. |
| sqli-union | |

## 3. Preguntas P1–P5

**P1.** ¿Por qué la detección por firmas es evadible por diseño? ¿Qué la complementa?

Una firma detecta una **cadena o patrón concreto**, no la intención ni el efecto de una acción. Para que funcione, el defensor tiene que anticipar de antemano exactamente qué forma va a tener el ataque: un User-Agent, una secuencia literal como `UNION SELECT `, una ruta. El problema es que casi siempre existen muchas formas distintas de lograr el mismo efecto sin que ninguna de ellas calce con la cadena exacta que la regla busca. En R4, por ejemplo, el ruleset de este lab exige un espacio después de `UNION SELECT` para disparar la firma `sqli-union`; para el intérprete SQL, un espacio y un comentario `/**/` son equivalentes como separador, pero para una regla que busca el carácter espacio literal, no lo son. La firma es evadible porque codifica una **forma superficial** del ataque, no su significado.

Esto no es un defecto corregible de una vez: es una limitación estructural de cualquier sistema que decida "coincide / no coincide" contra un conjunto finito de patrones conocidos. Siempre va a quedar afuera alguna variante sintáctica, codificación o transformación que un atacante puede probar. Por eso la detección por firma nunca debería ser la única capa. Se complementa con: (a) **validación y parametrización en la aplicación**, que elimina la causa raíz en vez de solo detectar el síntoma; (b) **normalización/canonicalización** de la entrada antes de aplicar la firma, para que variantes de encoding o espaciado converjan a una forma comparable; (c) **detección por comportamiento y correlación**, que mira patrones de uso (frecuencia, secuencia de endpoints, volumen) en vez de una cadena puntual, y que es precisamente lo que permite encontrar la intrusión de R5 aunque no dispare ninguna firma puntual; y (d) **revisión humana**, porque ninguna de las capas anteriores sustituye el criterio de alguien que mire el log completo y note lo que no encaja.

**P2.** La firma `sqli-union` exigía un espacio. Reescribí la regla para que NO se evada con `/**/`. ¿Se puede hacer una firma "perfecta"?

La fuente observada es [el ruleset crudo de R3](evidencia/salidas/r3-ruleset.txt): `el query matchea /union\s+select/`. Aunque su nota dice «un ESPACIO», `\s+` normalmente expresa uno o más caracteres de espacio en blanco, no exclusivamente un espacio ASCII. No se inspeccionó la implementación: el modo de comparación, la decodificación y el motor no se deducen de esa descripción. La limitación relevante es que un comentario no coincide con `\s+`.

Una propuesta conceptual, en sintaxis de expresiones regulares de Python, es:

```text
(?i)\bunion(?:\s|/\*[\s\S]*?\*/)+select\b
```

El modificador `(?i)` ignora mayúsculas; los límites `\b` delimitan las palabras; el grupo repetido acepta espacios en blanco o comentarios de bloque completos, incluso combinados. `[\s\S]*?` incluye saltos de línea y termina en el primer cierre del comentario. Así reconoce `UNION/**/SELECT`, además de `UNION SELECT` y mezclas de ambos separadores. Es una propuesta para detección: no se instaló ni se probó una evasión HTTP de R4.

Antes de inspeccionar, extraer el parámetro con la misma decodificación que la aplicación, con límites de tamaño y costo de procesamiento. Una alternativa es canonicalizar comentarios ordinarios como espacios y aplicar `(?i)\bunion\s+select\b`. Esto requiere un analizador compatible con el dialecto y contexto: no eliminar comentarios dentro de cadenas ni tratar comentarios ejecutables de ciertos dialectos como si fueran espacios inocuos. Conservar tanto el original como la representación normalizada permite auditar la decisión. No decodificar repetidamente sin límite.

No hay una firma perfecta: esta propuesta cubre el separador solicitado, pero no todo SQLi, variantes de dialecto o diferencias entre parsers. Texto legítimo como documentación que incluya `UNION/**/SELECT` también podría coincidir. Se deben evaluar falsos positivos con tráfico representativo, acotar la inspección por contexto y probar regresiones. La aplicación debe usar consultas parametrizadas, validación de entradas y privilegios mínimos de BD; correlación y revisión humana complementan las alertas. Una coincidencia de regex no prueba explotación ni compromiso.

**P3.** Detectar por User-Agent: ¿por qué es una detección débil? ¿Qué mirarías en lugar de "quién dice ser"?

**P4.** El R5: la intrusión estaba en el log. ¿Qué habría hecho que se detecte automáticamente y no dependiera de que alguien la mire?

**P5.** Cierre del curso: recorriste ataque (05–08), agentes (09) y defensa (10). ¿Qué cambió en cómo pensás la seguridad?

## 4. Bitácora

### P3 — Consulta del ruleset y validación de R3 (2026-10-23)

Los comandos HTTP se ejecutaron desde `cyberlab-attacker`, la misma consola usada por `make shell`, mediante `docker exec` en modo no interactivo. Los comandos de administración de Docker se ejecutaron desde la raíz del repositorio en el host. El registro ampliado se conserva en [evidencia/comandos.txt](evidencia/comandos.txt).

1. **Consulta inicial y diagnóstico.** Se consultó el ruleset:

   ```bash
   docker exec cyberlab-attacker bash -c 'curl -sS http://phantomcorp/soc/reglas'
   docker inspect cyberlab-phantomcorp --format '{{index .Config.Labels "com.docker.compose.project.config_files"}}'
   docker exec cyberlab-attacker bash -c 'curl -sS -i http://phantomcorp/'
   ```

   La primera consulta devolvió `Not Found` ([salida conservada](evidencia/salidas/r3-intento-target-lab09.txt)). Las etiquetas del contenedor indicaron el compose de Lab 09 y el portal respondió con el banner `PhantomCapstone/1.0`.

2. **Activación del target correcto y captura de R3.**

   ```powershell
   docker compose -p cyberlab --project-directory . -f entorno/docker-compose.yml -f labs/lab10-deteccion-evasion/entorno/target.compose.yml up -d --build phantomcorp
   docker exec cyberlab-attacker bash -c 'curl -sS http://phantomcorp/soc/reglas' > entregas/lab10/grupo06/evidencia/salidas/r3-ruleset.txt
   ```

   El [ruleset obtenido](evidencia/salidas/r3-ruleset.txt) publicó cuatro firmas y la flag de R3. El reemplazo del target inició otra sesión: sus logs no deben considerarse una continuación de la línea base anterior de R1.

3. **Validación de la flag y consulta del progreso.** Por los finales de línea CRLF de Windows, el motor se ejecutó en una copia temporal normalizada a LF dentro del contenedor, sin alterar sus archivos originales. Desde la raíz de esa copia se ejecutó:

   ```bash
   bash ./ctf submit 10 R3 'FLAG{signature_ruleset}'
   bash ./ctf status 10
   ```

   El verificador [aceptó R3](evidencia/salidas/r3-submit.txt). El [estado parcial](evidencia/salidas/status-10-p3.txt) mostró únicamente R3, 1/5: no se encontró el archivo de progreso anterior al preparar la copia. Se conservan las evidencias históricas de R1/R2 sin atribuirles validación actual. Se copió el progreso generado al host mediante:

   ```powershell
   docker cp cyberlab-attacker:/tmp/lab10-p3/.progreso/10.done .progreso/10.done
   ```

4. **Comprobación de la regla propuesta para P2.** Se envió un script por entrada estándar a `docker exec -i cyberlab-attacker python3 -`. Los [ocho casos locales](evidencia/salidas/p3-regresion-regla.txt) verificaron espacios, comentarios, límites de palabras y un posible falso positivo. No generaron solicitudes HTTP ni constituyen una ejecución de R4.
