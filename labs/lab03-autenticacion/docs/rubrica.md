# Laboratorio 03 — Rúbrica

**Total:** 100 · **Aprobación:** 60 · **Promoción práctica:** 80

| Componente | Puntos |
|---|---:|
| Parte A — análisis de la brecha | 30 |
| Parte B.1 — contraseñas (código + respuestas) | 30 |
| Parte B.2 — TOTP (código + respuestas) | 25 |
| Mini-research | 10 |
| Proceso — Git | 5 |

**B.1 (30):** `hash_password`/`verify_password` correctos, verificación en tiempo
constante, y explica salt e iteraciones con fundamento (no de memoria).
**B.2 (25):** `totp` da el vector RFC 6238 (287082 / 94287082); explica qué mitiga
y qué no el 2FA.
**Rechazo:** biblioteca externa en vez de stdlib; guardar contraseña en claro o
con sha256 pelado "porque anda"; IA no declarada.
