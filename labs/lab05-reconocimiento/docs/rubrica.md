# Laboratorio 05 — Rúbrica de evaluación

**Total:** 100 puntos
**Aprobación:** 60 puntos
**Nivel de promoción práctica (nota 8):** 80 puntos

> **Leé esta rúbrica antes de empezar, no después de entregar.** Tiene causales
> de rechazo automático. Saber cómo se corrige antes de hacerlo no es trampa: es
> lo normal en cualquier trabajo profesional.

---

## Resumen

| Componente | Puntos | Peso |
|---|---:|---:|
| **Parte práctica** — captura de las 5 flags | 20 | 20 % |
| **Mapa de superficie de ataque** — identificación + clasificación | 40 | 40 % |
| **Preguntas de análisis** (P1–P5) | 25 | 25 % |
| **Mini-research** | 10 | 10 % |
| **Proceso** — Git y colaboración | 5 | 5 % |
| **Total** | **100** | |

---

## Parte práctica — las 5 flags (20 puntos)

4 puntos por flag capturada, evidenciada con la captura de `./ctf status 05`.

| Puntos | Descriptor |
|---:|---|
| 20 | Las 5 flags capturadas. |
| 4×N | N flags capturadas. |
| 0 | Sin evidencia de captura. |

> Las flags demuestran que **operaste las tools**. No demuestran que entendiste:
> eso lo mide el mapa. Un grupo con 5 flags y un mapa flojo aprueba raspando.

---

## Mapa de superficie de ataque (40 puntos)

Se evalúa **por servicio** y por la **calidad de la clasificación**, no por la
cantidad de filas.

| Puntos | Descriptor |
|---:|---|
| 36–40 | Los 4 servicios identificados con **versión** y **evidencia** concreta (banner o línea de nmap). Clasificación de criticidad **fundamentada contra este caso**. CVE correcto donde corresponde, con su CVSS. |
| 28–35 | Servicios identificados con evidencia, pero la clasificación de criticidad es genérica o falta algún CVE relevante. |
| 20–27 | Identifica los servicios pero sin versión o sin evidencia; clasificación superficial. |
| 10–19 | Lista puertos abiertos sin identificar producto/versión. Es un `nmap` pegado, no un análisis. |
| 0–9 | Ausente o incorrecto. |

**Causal de rechazo automático de este componente:** inventar un CVE que no
aplica al servicio/versión, o afirmar una versión sin evidencia que la respalde.
**"No pude determinar la versión del puerto X" es una respuesta honesta y
válida** y no penaliza si está justificada.

---

## Preguntas de análisis P1–P5 (25 puntos)

5 puntos cada una.

| Puntos por pregunta | Descriptor |
|---:|---|
| 5 | Responde con precisión, usando **evidencia de lo que hizo en el lab**, con vocabulario técnico correcto. |
| 3 | Responde correctamente pero en general, sin bajar a lo que observó. |
| 1 | Responde de forma vaga o con imprecisiones conceptuales. |
| 0 | Ausente o incorrecta. |

Ojo particular:
- **P3** (la ironía de `robots.txt`): se busca que entiendan que un control
  pensado para una cosa (SEO) filtra información para otra (recon).
- **P5** (rol defensor): las medidas tienen que ser **concretas y aplicables a
  PhantomCorp**, no "poner un firewall" a secas.

---

## Mini-research (10 puntos)

| Puntos | Descriptor |
|---:|---|
| 9–10 | Investiga en profundidad una técnica/CVE, con fuentes verificables y explicación propia. |
| 5–8 | Correcto pero descriptivo; copia y pega reformulado. |
| 1–4 | Superficial o sin fuentes. |
| 0 | Ausente. |

---

## Proceso — Git y colaboración (5 puntos)

| Puntos | Descriptor |
|---:|---|
| 5 | Commits de **todos** los integrantes, mensajes claros, rama y directorio correctos. |
| 3 | Colaboración despareja o mensajes pobres. |
| 0 | Commits de una sola cuenta. **Se considera no entregado por el grupo.** |

---

## Causales de rechazo automático del trabajo completo

1. Escanear cualquier sistema que **no** sea el target de la cátedra. Esto no es
   una falta de forma: es un problema **legal y ético** (ver Uso responsable).
2. Entregar flags obtenidas leyendo el código del target o el `solucion.md` en
   lugar de operando las tools, y presentarlas como recon propio.
3. Uso de IA no declarado (ver `CONTRIBUTING.md`).
