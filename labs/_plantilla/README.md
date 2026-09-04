# Laboratorio NN — <Tema>

**Unidad N** · <título de la unidad según el programa>
**Modalidad:** grupos de 4 a 5 integrantes
**Entrega:** fork + Pull Request, en `entregas/labNN/grupoXX/`
**Entorno:** Docker · <o "teoría/código" si no usa Docker>

> Plantilla. Copiá este directorio a `labs/labNN-tema/`, completá cada sección y
> borrá estas notas en cursiva. Respetá la **anatomía de 4 partes**: no la saltees,
> es lo que hace que el alumno pueda seguir el lab solo.

---

## El escenario

*Enganchá con la narrativa PhantomCorp. ¿Qué fase del engagement es? ¿Qué
descubrió/logró el alumno en el lab anterior que ahora continúa? La historia es
lo que los mantiene metidos en la materia.*

---

## Por qué este laboratorio

*El concepto, desde cero. ¿Qué problema resuelve la técnica de este lab? ¿Dónde
encaja en la cadena de ataque (Kill Chain / ATT&CK / PTES)? Todavía sin tocar una
tool.*

---

## Objetivos de aprendizaje

*Lista numerada, verbos concretos (ejecutar, clasificar, distinguir...). Cerrá con
la tributación al Diseño Curricular.*

---

## Requisitos

*Docker + lo que sume este lab. Verificaciones (`docker compose version`, etc.).*

---

## Preparación del entorno

```bash
make setup          # una vez en todo el curso
./ctf lab NN        # levanta el entorno y abre esta guía
make shell          # entrás a la consola del atacante
```

> **Regla de oro.** Solo se opera contra los contenedores de la cátedra. Ver
> [Uso responsable](../../CONTRIBUTING.md). Ley 26.388.

---

## Cómo se juega

*Explicá las flags (`./ctf submit NN R1 '...'`) y que la NOTA está en el informe,
no en las flags.*

---

## Parte 1 · TEORÍA

*El concepto explicado. Tablas comparativas, diagramas ASCII de dónde encaja.*

## Parte 2 · EJEMPLOS

*2-3 casos reales que ilustran el patrón. "Cómo se ve esto en la vida real."*

## Parte 3 · TOOLS

*Cada herramienta: qué hace · anatomía del comando · cómo leer la salida · cómo
clasificar lo que encontrás. Que el alumno practique cada una a medida que lee.*

## Parte 4 · PRÁCTICA

*La tabla de retos: técnica + pista (NO el comando exacto). El alumno descubre el
"cómo".*

| Reto | Técnica | Pista |
|---|---|---|
| **R1** | | |

## Parte 5 · CLASIFICACIÓN / ENTREGABLE

*El deliverable que evalúa la rúbrica. Tabla de análisis + preguntas P1..P5.*

---

## Qué se entrega

*Qué archivos, en `entregas/labNN/grupoXX/`, y la fecha límite.*

## Uso responsable

*Recordatorio legal específico a las técnicas de este lab.*
