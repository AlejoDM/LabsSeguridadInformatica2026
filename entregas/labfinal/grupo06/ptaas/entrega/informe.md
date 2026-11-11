# Informe técnico — PTaaS · Grupo 06

> Borrador de P1. Solo tiene la sección 0 por ahora; el resto se completa al integrar.
> **No commiteado a propósito:** lo sube el grupo cuando esté completo.

## 0. Declaración de uso de IA

**Herramienta:** Claude Code, modelo Haiku 5.5.

**Finalidad y partes asistidas (persona 1, bitácora y auditoría):**
- Explicación de la estructura del kit y de las reglas de `CLAUDE.md` / `AGENTS.md`.
- Borrador de la firma del contrato de bitácora (`harness/audit.py`), del test que la cubre (`tests/test_audit_persistence.py`) y de la ayuda para corregir un orden de imports con ruff.
- Borrador de `openspec/changes/002-audit-persistence/design.md` y del delta `specs/audit-log/spec.md`.
- Redacción de la nota de traspaso `handoffs/` y del registro `ia-errores.md`.

**Verificación humana y comprobaciones realizadas:**
- Corrida de la línea base del kit: `pytest -q` (77 passed), `evals/run_evals.py --mode golden` (10/10) y `tools/progress.py`. Salidas crudas en `entrega/evidencia/salidas/arranque-p1.txt`.
- `pytest` del contrato nuevo (5 passed), `mypy --strict harness/audit.py` (sin errores) y `ruff check` (limpio tras corregir imports).
- El test en rojo se committeó antes del contrato, y se comprobó que fallaba por la ausencia del módulo.
- Un error de la IA (rama creada con upstream a `main`) se detectó con `git status` y se corrigió; queda en `ia-errores.md`.

**Límites de la verificación:**
- Las pruebas se corrieron con Python 3.14; el kit y el CI apuntan a Python 3.12. No se probó en 3.12.
- No se levantó el laboratorio `lab/` (Docker): no hay evidencia de funcionamiento contra DVWA ni Juice Shop.
- El diseño y el delta todavía no fueron revisados por otro integrante (tarea 1.3 abierta).
- Los requisitos de `design.md` (triggers, ancla, concurrencia) son decisiones propuestas; no están implementadas ni probadas en SQLite todavía.
