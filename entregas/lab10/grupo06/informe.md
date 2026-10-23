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

*Pendiente de completar por el grupo.*

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

**P2.** La firma `sqli-union` exigía un espacio. Reescribí la regla para que NO se evada con `/**/`. ¿Se puede hacer una firma "perfecta"?

**P3.** Detectar por User-Agent: ¿por qué es una detección débil? ¿Qué mirarías en lugar de "quién dice ser"?

**P4.** El R5: la intrusión estaba en el log. ¿Qué habría hecho que se detecte automáticamente y no dependiera de que alguien la mire?

**P5.** Cierre del curso: recorriste ataque (05–08), agentes (09) y defensa (10). ¿Qué cambió en cómo pensás la seguridad?

## 4. Bitácora
