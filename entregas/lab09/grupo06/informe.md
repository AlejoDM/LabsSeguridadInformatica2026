# Informe — Laboratorio 09 · Agentes de pentest

**Grupo:** 06
**Fecha:** 2026-10-23
**Proveedor usado:** mock

| Nombre y apellido | Usuario de GitHub |
|---|---|
| Martín Beccereca | martinbeccereca |
| Belén Benito | belubenito01 |
| Alejo José De Miguel | AlejoDM |
| Tomás Giudici | TomasGiudici |
| Carolina Suppo | carosuppo |

## 0. Declaración de uso de IA

*Pendiente de completar por el grupo.*

## 1. Flags capturadas

*(salida de `./ctf status 09`, pendiente de completar cuando se resuelvan los 5 retos)*

| Reto | Estado | Evidencia |
|---|---|---|
| R1 — Recon inicial | Obtenida | [Transcript de referencia](evidencia/salidas/referencia-mock.txt) (pasos 1-2) y [envío de R1](evidencia/salidas/r1-submit.txt) |

## 2. Tu agente

*Pendiente del responsable de R5: adjuntar `src/agente_esqueleto.py` completado y su salida trayendo el flag R5.*

## 3. Auditoría crítica del agente

**Transcript:** *(pegar la corrida completa o remitir a `evidencia/salidas/referencia-mock.txt`)*

**Aciertos y errores:** *(decisión por decisión)*

| Paso | Acción solicitada | Resultado observado | Evaluación humana |
|---|---|---|---|
| 1 | `nmap_scan({'host': 'phantomcorp'})` | `error nmap: Command [...] timed out after 60 seconds` (ver `evidencia/salidas/referencia-mock.txt`, paso 1) | Insuficiente, pero razonable como primer intento: `nmap -sV` es una decisión de recon estándar y coherente con lo practicado en el Lab 05. El error es del entorno (timeout), no una decisión incorrecta del agente. Un operador humano habría reintentado con un escaneo más acotado (por ejemplo, menos puertos o sin `-sV`) en vez de abandonar la vía por completo; el agente, en cambio, pasó directamente a otra tool. |
| 2 | `http_get({'url': 'http://phantomcorp/'})` | `HTTP 200` con header `X-Recon-Flag: FLAG{agente_primer_recon}` y cuerpo "PhantomCorp Capstone. Auditame." (ver paso 2) | Adecuada: ante el fallo de `nmap_scan`, el agente cambió de tool en vez de insistir con la misma acción fallida, y la petición HTTP directa a la raíz del sitio es la alternativa obvia de recon cuando se sabe (de los labs anteriores) que el objetivo expone un servicio web. Encontró la flag en el primer intento con esa tool, sin pasos redundantes. |

**Límite de esta auditoría:** este análisis cubre únicamente los pasos 1 y 2 (R1); no evalúa R2-R5, que corresponden a otros responsables de la tabla según el reparto del grupo. Tampoco demuestra que el agente "razone" de forma general: en modo `mock` la secuencia de decisiones es fija y determinista, no generada por un LLM real; esa distinción se retoma en P2.

**El guardrail (R4):** *(qué pasó y por qué importa; qué otros agregarían)*

## 4. Preguntas de análisis
**P1 — el loop de tool-use.**
**P2 — LLM vs. script fijo.**
**P3 — ventaja del diseño agnóstico.**
**P4 — dos riesgos y su guardrail.**
**P5 — por qué los labs 05–08 eran requisito.**
