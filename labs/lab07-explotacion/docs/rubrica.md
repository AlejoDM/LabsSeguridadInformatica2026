# Laboratorio 07 — Rúbrica de evaluación

**Total:** 100 · **Aprobación:** 60 · **Promoción práctica (nota 8):** 80

> Leela antes de empezar. Tiene causales de rechazo automático.

## Resumen

| Componente | Puntos |
|---|---:|
| Parte práctica — 5 flags | 20 |
| Tabla de explotación (payload → efecto → defensa) | 40 |
| Preguntas de análisis P1–P5 | 25 |
| Mini-research | 10 |
| Proceso — Git | 5 |

## Tabla de explotación (40)

| Puntos | Descriptor |
|---:|---|
| 36–40 | Las 5 vulns con **payload exacto**, la **consulta/comando/ruta resultante** reconstruida, el **impacto** y una **defensa concreta y correcta** para cada una. |
| 28–35 | Payloads correctos pero la reconstrucción o la defensa es genérica en alguna. |
| 20–27 | Explota pero no explica el mecanismo (pega el payload sin reconstruir la query). |
| 10–19 | Solo flags, sin análisis. |
| 0–9 | Ausente o incorrecto. |

**Rechazo del componente:** proponer como defensa algo que no previene la vuln
(ej. "validar del lado del cliente" para el IDOR), o presentar flags obtenidas del
`solucion.md`.

## Preguntas P1–P5 (25) · Mini-research (10) · Proceso (5)
Igual que labs anteriores. Ojo P4 (por qué parametrizar mata la SQLi) y P5 (dónde
va el control de acceso).

## Causales de rechazo del trabajo
1. Explotar cualquier sistema que no sea el target de la cátedra (Ley 26.388).
2. Flags del solucion.md presentadas como propias.
3. Uso de IA no declarado.
