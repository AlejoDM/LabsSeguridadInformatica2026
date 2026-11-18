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

### Declaración de uso de IA — P5

**Herramienta:** Claude Code, modelo Opus 5.5.

**Finalidad y partes asistidas (validación, informe y recorrido):**

- Borradores de `design.md` y de los deltas de los changes 006 y 007. Los de 007
  (tasks 1.1 y 1.2) se hicieron en reemplazo de P1, con su acuerdo.
- Tests en rojo y código de `harness/sandbox.py`, `harness/validation.py`,
  `harness/validation_cli.py`, `harness/report_builder.py`,
  `harness/defectdojo_export.py` y `harness/pipeline.py`; controles nuevos en
  `harness/poc/catalog.py`; sección `sandbox` de `harness/profiles.yaml` (archivo
  de P3, con aviso).
- Mutaciones M10–M29, casos de evals de validación y redacción de esta sección.

**Verificación humana y comprobaciones realizadas:**

- P5 revisó y aceptó cada decisión de diseño antes de implementarla (límites del
  sandbox, alcance de la aprobación, política cuando el Reviewer no responde) y
  cada delta antes de los tests.
- P5 ejecutó en persona la prueba de aislamiento del sandbox (`False` hacia
  `1.1.1.1:80` y control positivo `True` hacia `dvwa.lab.test:80`) y la corrida
  real del recorrido, aprobando cada gate con la CLI después de revisar la lista
  de hallazgos.
- `pytest` en el runner del lab con Python 3.12: **362 passed, 1 skipped**.
  Evals golden **17/17**. Las 20 mutaciones fueron detectadas. Salidas en
  `entrega/evidencia/salidas/P5-*` y `mutacion-P5-*`.
- Los errores de la IA detectados durante el trabajo están en `ia-errores.md`.

**Límites de la verificación:**

- `ruff check` y `mypy --strict` pasan en los seis módulos y los dos archivos de
  tests de P5 (`P5-lint.txt`). `mypy` se corrió con `--follow-imports=silent`: no
  cubre los módulos de otros integrantes que P5 importa. Para los adaptadores y
  el loop A de P3, que no declaran tipos, se usó `cast` y un `type: ignore`
  explícito en lugar de modificarlos.
- Los changes 006 y 007 se archivaron sin la revisión cruzada (1.3) de otro
  integrante.
- La importación en DefectDojo fue una prueba de formato con los hallazgos del
  informe DEMO, en una instancia local; todavía no hay un informe entregado para
  importar.

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

## Validación, informe y recorrido de un comando (P5)

**Sandbox y loop C (change 006).** La validación ocurre en un contenedor nuevo
por verificación, en la red interna del laboratorio. El contenedor corre de
solo lectura, sin capacidades, sin volúmenes y con límites de memoria y
procesos. Se destruye siempre, aunque la verificación falle; si no se puede
destruir, el loop se aborta. Cada verificación hace una sola solicitud GET, sin
seguir redirecciones, con timeout de 10 s y respuesta truncada a 1 MB. El envío
pasa por `Harness.invoke` con un token de fase `validate`. Antes de crear el
contenedor, el Sender rechaza cualquier host que no sea del laboratorio, aunque
el token lo incluya. La aprobación del Reviewer se liga al hallazgo, a la
verificación y al hash de los parámetros: si el agente cambia un parámetro
después de aprobado, el hallazgo vuelve a `PENDING_HITL`. Nada se aprueba solo;
un hallazgo sin decisión figura como "no validado (sin aprobación)". Un hallazgo
queda validado solo si los dos intentos coinciden. La bitácora guarda el hash y
el largo del cuerpo de la respuesta, nunca el cuerpo.

La prueba de aislamiento la ejecutó una persona: desde la red del sandbox,
`1.1.1.1:80` no es alcanzable y `dvwa.lab.test:80` sí (control positivo).

**Huecos del kit encontrados.** `run_parametrized` aceptaba un `path` que
cambiaba el host (`//example.com/`), recorridos (`/../../etc/passwd`) y un
`param_name` con separadores de query; además, el catálogo aceptaba entradas
aprobadas por un agente. Los cuatro se corrigieron con test en rojo primero
(B1–B4 en `entrega/red-team.md`).

**Informe, entrega y exportación (change 007).** El informe toma el estado de
cada hallazgo de la bitácora del loop C, no de lo que declare el hallazgo: un
"validado" sin respaldo hace fallar la generación. Antes de generarlo se
verifica la cadena de la bitácora y que cada referencia de evidencia exista. El
informe se identifica por su hash, y la entrega exige una aprobación registrada
por una persona para ese hash exacto: si cambia un hallazgo, la aprobación
anterior no sirve. Si el contenido incluye cookies de sesión, tokens, contraseñas,
claves o el canario de la verificación de reflexión, la generación falla en vez
de redactarlos. La exportación a DefectDojo (formato de importación genérico)
solo procede con informes entregados, sin nombres de personas ni datos de
respuestas, y sin inventar severidad: el contrato no trae puntaje CVSS y se
marca `severity-unknown`. Un informe con alguna etapa simulada se marca **DEMO**
y no se puede entregar ni exportar.

**Recorrido de un comando.** `python -m harness.pipeline run` recorre RoE →
recon → análisis → validación → informe → entrega. El recon real de P3 corre
dentro del runner del laboratorio; el sandbox, desde el host. En cada gate el
comando espera una decisión registrada con la CLI en otra terminal. Corrida real
del 18/11/2026 (`entrega/evidencia/salidas/P5-recorrido-02/`):

| Etapa | Resultado |
|---|---|
| Recon (real) | `STOPPED`, grafo estabilizado: `dvwa.lab.test`, `juiceshop.lab.test` |
| Análisis | Simulado (`lab/analysis-fixture.json`): 4 candidatos del catálogo inerte |
| Validación (real, sandbox) | Falta de protección contra clickjacking, ausencia de CSP y cookie sin flags en DVWA: **validados** en los dos intentos. Clickjacking en Juice Shop: **no validado** (no se observó la debilidad) |
| Informe | Versión 1, **DEMO** por el análisis simulado: entrega bloqueada, sin exportación |
| Bitácoras exportadas | `harness-audit.json` y `evidence.json` verificadas (`ok`) |

Los vectores CVSS del análisis simulado son valores de ejemplo y no una
evaluación; por eso el informe de esta corrida no es un resultado de pentest.

**Prueba de formato en DefectDojo.** Como el informe es DEMO, el recorrido no lo
exporta. Para verificar el formato, se reconstruyó ese mismo informe desde su
bitácora exportada (mismo `report_hash`), se convirtieron sus hallazgos con el
exportador del proyecto marcándolos `[DEMO]` y se importaron en una instancia
local de DefectDojo con el parser *Generic Findings Import*. Se importaron los
4 hallazgos con su CWE, 3 como verificados y las etiquetas `severity-unknown`.
Al re-importar el mismo archivo no se creó ningún hallazgo: la deduplicación
por identificador estable funciona (`P5-defectdojo-prueba-formato.txt`).

**Mutaciones.** M10–M29 en `entrega/mutaciones.md`: cada control nuevo (barrera
de host, destrucción del contenedor, gate por hallazgo, ligadura al hash,
consistencia entre intentos, respaldo en bitácora, entrega, DEMO, datos
sensibles, exportación y gates del recorrido) hace fallar al menos un test al
desactivarlo.

**Límites y pendientes:** el análisis real depende del change 005 (P4); hasta
entonces ningún informe del recorrido se entrega ni se exporta. La bitácora del
recorrido se exporta en JSON verificable; la persistencia SQLite depende del
change 002 (P1). `deliver(report, reviewer_approved)` con booleano sigue
existiendo por compatibilidad, aunque el recorrido no lo usa. Falta la revisión
cruzada de 006 y 007, y la importación en DefectDojo de un informe entregado (hoy
solo hay una prueba de formato con el informe DEMO).
