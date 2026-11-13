# Informe técnico — PTaaS · Grupo 06

> Borrador de integración. La sección 0 corresponde a P1; el aporte P2 que sigue
> queda pendiente de integración y revisión por P1.

## 0. Declaración de uso de IA

**Herramienta:** Claude Code, modelo Haiku 5.5.

**Finalidad y partes asistidas (bitácora y auditoría):**

- Borrador de la firma del contrato de bitácora (`harness/audit.py`), del test que la cubre (`tests/test_audit_persistence.py`) y de la ayuda para corregir un orden de imports con ruff.
- Borrador de `openspec/changes/002-audit-persistence/design.md` y del delta `specs/audit-log/spec.md`.
- Redacción de la nota de traspaso `handoffs/2026-11-11_p1-a-todos_contrato-audit.md`.

**Verificación humana y comprobaciones realizadas:**

- Corrida de la línea base del kit: `pytest -q` (77 passed), `evals/run_evals.py --mode golden` (10/10) y `tools/progress.py`. Salidas crudas en `entrega/evidencia/salidas/arranque-p1.txt`.
- `pytest` del contrato nuevo (5 passed), `mypy --strict harness/audit.py` (sin errores) y `ruff check` (limpio tras corregir imports).

**Límites de la verificación:**

- Las pruebas se corrieron con Python 3.14; el kit y el CI apuntan a Python 3.12. No se probó en 3.12.
- No se levantó el laboratorio `lab/` (Docker): no hay evidencia de funcionamiento contra DVWA ni Juice Shop.
- El diseño y el delta todavía no fueron revisados por otro integrante (tarea 1.3 abierta).
- Los requisitos de `design.md` (triggers, ancla, concurrencia) son decisiones propuestas; no están implementadas ni probadas en SQLite todavía.

### Declaración de uso de IA — P2

**Herramientas utilizadas:** opencode con DeepSeek V4.1 Flash en la
implementación inicial y GPT-6 Luna en la revisión posterior.

**Finalidad y partes asistidas (autorización y red team):**

- Asistencia en el parser de RoE, la emisión de tokens, los controles del Guard,
  los tests adversariales y la revisión de selección de herramientas.

**Verificación humana y comprobaciones realizadas:**

- Corrida de `pytest` (162 passed), `evals/run_evals.py --mode golden` (10/10),
  `tools/progress.py`, `ruff` y el chequeo focal de `mypy`. Salidas crudas en
  `entrega/evidencia/salidas/`.
- Registro de los errores detectados y sus correcciones en `ia-errores.md` y
  `entrega/retrospectiva.md`.

**Límites de la verificación:**

- Las pruebas se corrieron con Python 3.13; el kit y el CI apuntan a Python 3.12.
  No se probó en 3.12 ni se ejecutaron escaneos contra DVWA o Juice Shop.

## Autorización, RoE, tokens y red team

Se implementó el parser YAML del Rules of Engagement (RoE), que limita dominios
y CIDR al laboratorio declarado en `harness/profiles.yaml` y verifica aprobación,
ventana con zona horaria, fases y exclusiones. El emisor genera tokens por fase
con TTL tomado de `policy.yaml`, registra emisiones y rechazos, y vincula cada
token al engagement. El Guard incluye comprobaciones de normalización, IPv6,
engagement y resolución DNS opcional. Para emitir tokens se hizo obligatorio el
sink de auditoría; queda pendiente conectar el sink persistente SQLite de P1.
También se incorporaron `RedirectPolicy` y `validate_parameters` como controles
reutilizables por los adaptadores.

Los intentos adversariales A1–A10 están en `tests/test_redteam_guard.py` y las
mutaciones M1–M9 en `entrega/mutaciones.md`, con salidas en
`entrega/evidencia/salidas/`. Para los gates 007 · 3.1 y 3.3 se agregaron pruebas
que rechazan hallazgos incompletos y entregas sin aprobación. No se modificó
`harness/reporting.py`, que corresponde a P5.

En la revisión posterior se agregaron pruebas para la expiración exacta del
token, fases vacías, exclusiones combinadas, contactos inválidos, fases
desconocidas y el hash de aprobación. La evidencia local registra **162 tests
aprobados**, **10/10 evals golden** y `ruff` limpio en los archivos P2 revisados.
Las comprobaciones se ejecutaron con `python -X utf8` por la codificación de la
consola Windows. `progress.py` informa 003 en **13/14**: sigue pendiente la
revisión cruzada humana 1.3. La spec de autorización contiene **23 Scenarios**.

El chequeo focal `mypy --strict --follow-imports=skip` pasó para `roe.py` y
`tokens.py`. Al seguir imports, mypy informa errores en las interfaces de
`contracts.py` y `policy_loader.py`, que no corresponden a esos dos archivos.

**Límites y pendientes:** A4 depende de configurar `Guard(resolver=...)` en
runtime y A5 de que el adaptador HTTP de 004 use `RedirectPolicy`; ambas
integraciones siguen pendientes. También falta una revisión humana de si los
bypass encontrados son reales y si las correcciones son suficientes, además de
la revisión cruzada 003 · 1.3. Los commits de tests y correcciones se conservaron
en la historia local: `98e85f4` → `1b9392e` y `9a76691` → `937a234`. La rama aún
no se publicó en el remoto. La prueba de “emisor único” de `ScopeToken` es
estática: la clase sigue siendo pública y puede construirse desde fuera del
paquete, por lo que no impide en runtime la fabricación de tokens. También falta
una revisión independiente de seguridad del diff.
