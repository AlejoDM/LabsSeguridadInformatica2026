# Informe de mutaciones — controles evaluados

Cada mutación se aplicó sobre el código real, se ejecutó el test que debía
detectarla y se restauró el archivo original. Las salidas completas quedaron en
`entrega/evidencia/salidas/mutacion-M*.txt`.

| # | Control mutado | Mutación aplicada | Test que la detectó | Resultado |
|---|---|---|---|---|
| M1 | `Guard._in_scope` (`harness/contracts.py`) | `return True` al inicio | `test_activo_fuera_de_alcance...`, A2, A3 | 8 tests fallaron |
| M2 | Resta de exclusiones (`harness/tokens.py`) | Usar `scope_networks()` sin restar exclusiones | `test_exclusion_de_host_prevalece...` | 1 test falló |
| M3 | Validación de CIDR (`harness/roe.py`) | Devolver el CIDR sin comprobar prefijo ni laboratorio | `test_roe_con_cidr_...`, A8 | 10 tests fallaron |
| M4 | Ligadura a engagement (`Guard.is_allowed`) | Desactivar la comparación de `engagement_id` | `test_token_de_otro_engagement...`, A6 | 2 tests fallaron |
| M5 | Revalidación DNS (`Guard._resolves_in_scope`) | `return True` al inicio | A4 (fuera de alcance y mixta) | 2 tests fallaron |
| M6 | Validación de host en redirecciones (`RedirectPolicy`) | `_host_permitido` siempre `True` | A5 (host externo, protocol-relative, sufijo) | 3 tests fallaron |
| M7 | Validación de parámetros (`validate_parameters`) | Devolver los parámetros sin validar | A9 (`parameters`) | 5 tests fallaron |
| M8 | Lock de la bitácora (`AuditLog.record_decision`) | Quitar el lock y agregar 1 ms entre leer `prev` y append | A10 concurrente | La cadena se bifurcó (`prev=GENESIS` duplicado) |
| M9 | Fase autorizada (`tokens.issue`) | Desactivar el chequeo de `authorized_phases` | `test_roe_valido_emite_token_solo_de_la_fase_pedida` | 1 test falló |

## Detalle de las mutaciones más relevantes

### M1 — El control de alcance (`_in_scope` en `True`)

Salida (resumen):

```text
FAILED tests/test_authorization.py::test_activo_fuera_de_alcance_se_bloquea_y_registra
FAILED tests/test_authorization.py::test_dominio_y_subdominio_en_alcance_pero_no_sufijo_enganoso
FAILED tests/test_redteam_guard.py::test_a2_sufijo_enganoso_se_bloquea[...] (4 casos)
FAILED tests/test_redteam_guard.py::test_a3_ipv4_mapeada_a_ipv6...
FAILED tests/test_redteam_guard.py::test_a3_ipv6_se_evalua_contra_su_cidr
8 failed, 45 passed
```

Restaurado: `53 passed`. Evidencia: `mutacion-M1-in_scope.txt`.

### M8 — Concurrencia de la bitácora

Sin lock y con una pausa entre leer el último hash y agregar el registro, dos
hilos tomaron el mismo `prev`:

```text
AssertionError: assert 'GENESIS' == '103e5543cab8...'
FAILED tests/test_redteam_guard.py::test_a10_escritura_concurrente_conserva_la_cadena
```

Con el lock restaurado: `1 passed`. Evidencia: `mutacion-M8-concurrencia.txt`.

## Lo que no se mutó y por qué

- `harness/reporting.py` (gates 007 · 3.1 y 3.3) es propiedad de P5. Los tests
  nuevos pasan contra el código existente (`red-007-gates.txt`), pero la
  mutación de ese control queda a cargo de P5 para no pisar su archivo.
- `harness/audit.py` (P1) no se modificó. La prueba A10 se hizo sobre
  `AuditLog` de `contracts.py`, que es la ruta que usa `Harness.invoke`. Una
  prueba de estrés manual de `InMemoryAuditStore` con 500 escrituras concurrentes
  dio cadena válida en esta corrida, pero no es una garantía formal; P1 debe
  cubrir la concurrencia de la implementación SQLite en 002 · 3.4.
