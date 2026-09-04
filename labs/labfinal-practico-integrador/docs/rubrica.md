# Práctico Final — Rúbrica

**Total:** 100 · **Aprobación:** 60 · **Promoción práctica (nota 8):** 80

Este práctico integra el curso; la rúbrica pesa fuerte en el **informe**.

| Componente | Puntos |
|---|---:|
| Los 4 hitos del engagement (flags) | 20 |
| Resumen ejecutivo (claridad, sin jerga, útil para decidir) | 15 |
| Hallazgos técnicos (severidad CVSS + evidencia + impacto) | 30 |
| Remediaciones (correctas y concretas) | 20 |
| Narrativa y conclusión | 10 |
| Proceso — Git y colaboración | 5 |

**Hallazgos técnicos (30):** cada hallazgo con CVSS **justificado**, evidencia
**reproducible** e impacto ligado a ESTE sistema. Un CVSS inventado o una
evidencia que no reproduce baja fuerte.
**Remediaciones (20):** deben prevenir la vulnerabilidad de raíz (consultas
parametrizadas, no "validar del lado del cliente"; no exponer backups; tokens no
predecibles). Igual que en los labs 07–10.

**Causales de rechazo:**
1. Auditar algo fuera del alcance (Ley 26.388).
2. Informe copiado de otro grupo sin atribución, o flags/hallazgos del solucion.md.
3. IA no declarada.
4. Acción destructiva sobre el target (viola las Reglas del engagement).
