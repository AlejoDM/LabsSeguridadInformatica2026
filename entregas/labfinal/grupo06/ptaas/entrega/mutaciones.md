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
| M10 (P5) | Parámetros que cambian el objetivo (`run_parametrized`, `harness/poc/catalog.py`) | No llamar a `_check_target_params` | `test_path_que_cambia_el_objetivo_se_rechaza` (6 casos), `test_param_name_con_caracteres_especiales_se_rechaza` (6 casos) | 12 tests fallaron |
| M11 (P5) | Aprobación humana del catálogo (`validate_entries`) | Desactivar el chequeo de `AGENT_APPROVERS` | `test_entrada_aprobada_por_un_agente_se_rechaza` (7 casos) | 7 tests fallaron |
| M12 (P5) | Recorrido de rutas (`_check_target_params`) | Quitar el rechazo de segmentos `..` | `test_path_que_cambia_el_objetivo_se_rechaza[/../../etc/passwd]` y `[/a/../../b]` | 2 tests fallaron |
| M13 (P5) | Segunda barrera de host (`SandboxSender._lab_host`, `harness/sandbox.py`) | `if not ok:` → `if False:` | `test_objetivo_fuera_del_lab_se_rechaza_antes_del_contenedor`, `test_esquema_o_url_no_permitidos` (gopher, ftp) | 3 tests fallaron |
| M14 (P5) | Destrucción del contenedor (`SandboxAdapter.run`) | `finally:` → `except ZeroDivisionError:` | `test_verificacion_finalizada_destruye_el_contenedor`, `test_fallo_del_runtime_destruye_igual_y_no_valida`, `test_evaluador_que_falla_...`, `test_si_la_destruccion_falla_...`, `test_timeout_...` | 5 tests fallaron |
| M15 (P5) | Gate HITL por hallazgo (`ApprovalStore.is_approved`, `harness/validation.py`) | Devolver siempre `True` | `test_sin_aprobacion_queda_pendiente_y_no_envia`, `test_parametros_cambiados_...`, `test_otra_verificacion_...`, `test_token_vencido_...` | 4 tests fallaron |
| M16 (P5) | Ligadura de la aprobación a los parámetros (`is_approved`) | No comparar `approved_hash` | `test_parametros_cambiados_despues_de_aprobar` | 1 test falló |
| M17 (P5) | Consistencia entre intentos (`_validate_one`) | No detectar resultados distintos | `test_intentos_contradictorios_no_validan` | 1 test falló |

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

### M10 a M12 — Controles del catálogo (P5, change 006)

Se mutó `harness/poc/catalog.py` y se corrieron los tests del catálogo
(`-k 'path or param_name or entrada or parametros_validos or test_poc_catalog'`).
La línea base tiene 1 fallo esperado
(`test_entrada_agregada_al_archivo_durante_el_loop_no_se_usa`, que depende de
`harness.validation`, todavía no implementado); cada mutación suma los fallos de
la tabla. El archivo se restauró y se comprobó con `cmp` que quedó idéntico.
Evidencia: `mutacion-P5-catalogo.txt`.

### M13 a M17 — Sandbox y loop C (P5, change 006)

Se mutaron `harness/sandbox.py` y `harness/validation.py` y se corrió
`tests/test_sandbox_loop_c.py` completo. Línea base: `62 passed, 1 skipped`
(el salteado es la prueba con Docker real). Cada mutación rompió al menos un
test y los dos archivos se restauraron y se compararon con `cmp`.

En M13 fallan solo los casos que el Guard no frena por su cuenta (`example.com`
con un token que lo incluye a propósito, `gopher://` y `ftp://`): `file://`,
`http://` sin host y la URL sin esquema los bloquea también el Guard. Es la
defensa en profundidad prevista en `design.md` (decisión 2).
Evidencia: `mutacion-P5-sandbox-loopc.txt`.

## Lo que no se mutó y por qué

- `harness/reporting.py` (gates 007 · 3.1 y 3.3) es propiedad de P5. Los tests
  nuevos pasan contra el código existente (`red-007-gates.txt`), pero la
  mutación de ese control queda a cargo de P5 para no pisar su archivo.
- `harness/audit.py` (P1) no se modificó. La prueba A10 se hizo sobre
  `AuditLog` de `contracts.py`, que es la ruta que usa `Harness.invoke`. Una
  prueba de estrés manual de `InMemoryAuditStore` con 500 escrituras concurrentes
  dio cadena válida en esta corrida, pero no es una garantía formal; P1 debe
  cubrir la concurrencia de la implementación SQLite en 002 · 3.4.
