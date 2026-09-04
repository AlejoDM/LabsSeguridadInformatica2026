# Laboratorio 09 — Rúbrica de evaluación

**Total:** 100 · **Aprobación:** 60 · **Promoción práctica (nota 8):** 80

> Leela antes de empezar. Tiene causales de rechazo automático.

## Resumen

| Componente | Puntos |
|---|---:|
| Parte práctica — 5 flags | 15 |
| **Agente completado (`agente_esqueleto.py`)** | 25 |
| **Auditoría crítica del agente** | 25 |
| Preguntas de análisis P1–P5 | 25 |
| Mini-research | 5 |
| Proceso — Git | 5 |

## Agente completado (25)

| Puntos | Descriptor |
|---:|---|
| 22–25 | El esqueleto corre, hace el loop completo (ejecuta tools y realimenta al LLM), encadena token→vault y trae el flag R5. Código limpio. |
| 16–21 | Corre pero con algún TODO resuelto de forma frágil (no realimenta bien, o no corta). |
| 8–15 | Corre solo con mock y a medias. |
| 0–7 | No corre o no se entregó. |

## Auditoría crítica del agente (25)

| Puntos | Descriptor |
|---:|---|
| 22–25 | Transcript analizado decisión por decisión, con aciertos **y** errores concretos, y análisis serio del guardrail (R4) y de qué otros faltarían. |
| 16–21 | Análisis correcto pero superficial en errores o en guardrails. |
| 8–15 | Describe la corrida sin criticarla. |
| 0–7 | Ausente. |

## Preguntas P1–P5 (25) · Mini-research (5) · Proceso (5)
5 pts por pregunta. Ojo **P5** (por qué los labs 05–08 eran requisito): es el
cierre conceptual del curso.

## Causales de rechazo del trabajo
1. **Subir una API key al repo** (aunque sea en un commit viejo). Rechazo + hay
   que rotarla: una key filtrada es una key comprometida.
2. Levantar el agente contra cualquier objetivo que no sea el target (Ley 26.388).
3. Entregar el esqueleto sin completar, o copiado del `agente_pentest.py` sin
   entenderlo (se pregunta en la defensa).
4. Uso de IA no declarado. *(Sí: declarar el uso de IA en un lab sobre agentes de
   IA. La herramienta se declara siempre.)*
