# Laboratorio 02 — Rúbrica

**Total:** 100 · **Aprobación:** 60 · **Promoción práctica:** 80

| Componente | Puntos |
|---|---:|
| Parte A — análisis de la falla | 30 |
| Parte B.1 — romper XOR (código + mensaje) | 25 |
| Parte B.2 — MAC ingenuo/HMAC (código + respuestas) | 30 |
| Mini-research | 10 |
| Proceso — Git | 5 |

**Parte A (30):** identifica el mal uso (no "el algoritmo malo"), la propiedad
rota y la forma correcta, **con fuentes**. Confundir el algoritmo con su uso baja
la nota.

**Parte B.1 (25):** `romper_xor_1byte` funciona y recupera el mensaje; se explica
por qué el cifrado clásico falla.

**Parte B.2 (30):** los tres MAC implementados; las respuestas B.2.1–B.2.3
correctas. Ojo: entender length-extension (no solo nombrarlo) y el timing attack.

**Causales de rechazo:** usar una biblioteca externa de cripto en vez de la
stdlib; IA no declarada; commits de una sola cuenta.
