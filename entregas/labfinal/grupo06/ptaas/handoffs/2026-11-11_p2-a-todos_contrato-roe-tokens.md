# Traspaso · P2 → P3/P4/P5 · 2026-11-11 · contrato de RoE, tokens y guard

**Task:** 003 · 2.2–2.5 y red team A1–A10
**PR / commit:** `1b9392e` (implementación), `98e85f4` (tests en rojo)

## Qué entrego

- `harness/roe.py`: `load(path) -> RoE` y `parse(mapping) -> RoE`.
- `harness/tokens.py`: `issue(roe, phase, *, now=None, audit=None) -> ScopeToken`.
- `harness/contracts.py`:
  - `ScopeToken` acepta `excluded_domains` al final (default `()`), compatible
    con las construcciones posicionales existentes.
  - `Guard(phase_allowlist, approvals=None, engagement_id=None, resolver=None)`.
  - `AuditLog.record_decision(...)` para eventos sin token (emisión/rechazo).
- `harness/adapters/common.py`: `validate_parameters(...)` y `RedirectPolicy`.

## Cómo se usa

```python
from harness.roe import load
from harness.tokens import issue
from harness.contracts import Phase

roe = load("roe.yaml")                       # lanza RoEValidationError si es inválido
token = issue(roe, Phase.RECON, audit=audit) # TTL de policy.yaml, dentro de la ventana
```

- El token solo sirve para `token.phase`; no se renueva solo.
- Las exclusiones del RoE ya vienen restadas del token (CIDR) o en
  `token.excluded_domains` (dominios y subdominios).
- Para A4, configurar `Guard(..., resolver=socket.getaddrinfo_wrapper)` en el
  runtime real; en tests se inyecta un fake. Sin resolver configurado no se
  resuelve DNS (comportamiento backward-compatible).
- Para A5, el adaptador HTTP del change 004 debe llamar
  `RedirectPolicy(allowed_domains).check(base, location)` antes de cada salto.
- Para A9, llamar `validate_parameters(params)` antes de construir argv.

## Qué todavía no funciona

- No hay adaptador HTTP real; `RedirectPolicy` está probada de forma aislada.
- No hay integración con la bitácora SQLite de P1: `issue(..., audit=...)` acepta
  `AuditLog` o cualquier sink con `append(dict)`.
- La revisión cruzada del delta 003 · 1.3 sigue pendiente.
- Las mutaciones de `reporting.py` (007 · 3.1/3.3) quedan para P5.

## Qué tenés que confirmar antes de usarlo

- Que el `engagement_id` del `Guard` coincida con el del RoE en el runtime.
- Que el adaptador HTTP use `follow_redirects=False` y consulte `RedirectPolicy`.
- Que P1 acepte el formato de evento `scope.issue_token` en la bitácora
  persistente.
- Que el laboratorio siga usando `10.99.0.0/24` y los dominios de
  `profiles.yaml`; el parser rechaza cualquier otro alcance.

**Revisó (persona):** pendiente — no lo completa el agente.
