"""Change 003 · RoE y emisión de scope tokens.

Escenarios de `openspec/changes/003-roe-and-tokens/specs/authorization/spec.md`.
Estos tests se escribieron antes de `harness/roe.py` y `harness/tokens.py`: en
rojo por importación/atributos faltantes, no por fallas accidentales.
"""
from __future__ import annotations

import time
from pathlib import Path

import pytest
import yaml

from harness.contracts import (
    AuditLog,
    Guard,
    Harness,
    KillSwitch,
    Phase,
    Result,
    ScopeToken,
    ScopeViolation,
)
from harness.policy_loader import phase_allowlist
from harness.roe import RoEValidationError, load, parse
from harness.tokens import TokenIssuanceError, issue
from tests.conftest import FakeAdapter, act, make_token


def ts(value: str) -> float:
    from datetime import datetime
    return datetime.fromisoformat(value).timestamp()


def roe_dict(**overrides):
    base = {
        "engagement_id": "eng-lab-001",
        "approver": "Responsable del laboratorio",
        "approval_ref": "ticket-LAB-001",
        "signed_at": "2026-11-11T09:00:00-03:00",
        "window": {
            "start": "2026-11-11T09:00:00-03:00",
            "end": "2026-11-11T18:00:00-03:00",
        },
        "scope": {
            "cidrs": ["10.99.0.0/24"],
            "domains": ["dvwa.lab.test", "juiceshop.lab.test"],
        },
        "exclusions": {"cidrs": [], "domains": []},
        "emergency_contacts": ["responsable-lab@example.test"],
        "authorized_phases": ["recon", "correlate", "analyze"],
    }
    data = {**base, **overrides}
    for key in ("window", "scope", "exclusions"):
        if key in overrides:
            data[key] = {**base[key], **overrides[key]}
    return data


def valid_roe():
    return parse(roe_dict())


def test_load_lee_yaml_y_conserva_la_aprobacion(tmp_path):
    path = tmp_path / "roe.yaml"
    path.write_text(yaml.safe_dump(roe_dict()), encoding="utf-8")
    roe = load(path)
    assert roe.engagement_id == "eng-lab-001"
    assert roe.approval_hash
    assert roe.scope_cidrs == ("10.99.0.0/24",)


def test_load_de_archivo_inexistente_no_emite_token(tmp_path):
    with pytest.raises(RoEValidationError, match="leer"):
        load(tmp_path / "no-existe.yaml")


def _env(guard: Guard | None = None) -> tuple[Harness, AuditLog]:
    guard = guard or Guard(phase_allowlist())
    audit = AuditLog()
    adapters = {"httpx.probe": FakeAdapter("httpx.probe", (Phase.RECON,))}
    return Harness(guard, audit, adapters, KillSwitch()), audit


# --- Requisito: RoE completo y aprobado -------------------------------------


def test_roe_sin_alcance_se_rechaza():
    with pytest.raises(RoEValidationError, match="alcance"):
        parse(roe_dict(scope={"cidrs": [], "domains": []}))


def test_roe_sin_aprobador_se_rechaza():
    with pytest.raises(RoEValidationError, match="approver"):
        parse(roe_dict(approver=" "))


def test_roe_sin_contacto_de_emergencia_se_rechaza():
    with pytest.raises(RoEValidationError, match="emergency"):
        parse(roe_dict(emergency_contacts=[]))


# --- Requisito: alcance acotado al laboratorio ------------------------------


@pytest.mark.parametrize("cidr", ["0.0.0.0/0", "10.0.0.0/8", "8.8.8.0/24", "::/0", "10.99.0.0/16"])
def test_roe_con_cidr_publico_amplio_o_fuera_del_lab_se_rechaza(cidr):
    with pytest.raises(RoEValidationError, match="CIDR"):
        parse(roe_dict(scope={"cidrs": [cidr], "domains": []}))


def test_roe_con_dominio_fuera_del_lab_se_rechaza():
    with pytest.raises(RoEValidationError, match="dominio"):
        parse(roe_dict(scope={"cidrs": ["10.99.0.0/24"], "domains": ["example.com"]}))


# --- Requisito: ventana temporal en UTC ------------------------------------


def test_ventana_en_zonas_horarias_distintas_produce_el_mismo_epoch():
    local = parse(roe_dict())
    utc = parse(roe_dict(
        window={"start": "2026-11-11T12:00:00Z", "end": "2026-11-11T21:00:00Z"},
        signed_at="2026-11-11T12:00:00Z",
    ))
    assert local.window_start == utc.window_start
    assert local.window_end == utc.window_end


def test_ventana_invertida_se_rechaza():
    with pytest.raises(RoEValidationError, match="ventana"):
        parse(roe_dict(window={"start": "2026-11-11T18:00:00Z", "end": "2026-11-11T09:00:00Z"}))


def test_ventana_invertida_solo_al_comparar_en_utc_se_rechaza():
    # En hora local -03:00 parece 23:30 -> 00:30, pero en UTC es 02:30 -> 02:30.
    with pytest.raises(RoEValidationError, match="ventana"):
        parse(roe_dict(window={"start": "2026-11-11T23:30:00-03:00",
                               "end": "2026-11-12T02:30:00Z"}))


# --- Requisito: exclusiones prevalecen -------------------------------------


def test_exclusion_que_anula_todo_el_alcance_se_rechaza():
    with pytest.raises(RoEValidationError, match="exclusi"):
        parse(roe_dict(scope={"cidrs": ["10.99.0.0/24"], "domains": []},
                       exclusions={"cidrs": ["10.99.0.0/24"], "domains": []}))


def test_exclusion_de_host_prevalece_sobre_el_alcance():
    roe = parse(roe_dict(exclusions={"cidrs": ["10.99.0.10/32"], "domains": []}))
    token = issue(roe, Phase.RECON, now=ts("2026-11-11T10:00:00-03:00"))
    guard = Guard(phase_allowlist())
    assert guard.is_allowed(act("httpx.probe", Phase.RECON), "10.99.0.11", token)
    assert not guard.is_allowed(act("httpx.probe", Phase.RECON), "10.99.0.10", token)
    assert token.allowed_cidrs != ("10.99.0.0/24",)  # se restó el /32


def test_exclusion_de_dominio_cubre_subdominios():
    roe = parse(roe_dict(exclusions={"cidrs": [], "domains": ["admin.dvwa.lab.test"]}))
    token = issue(roe, Phase.RECON, now=ts("2026-11-11T10:00:00-03:00"))
    guard = Guard(phase_allowlist())
    assert guard.is_allowed(act("httpx.probe", Phase.RECON), "dvwa.lab.test", token)
    assert not guard.is_allowed(act("httpx.probe", Phase.RECON), "admin.dvwa.lab.test", token)


# --- Requisito: token por fase, TTL y sin renovación -----------------------


def test_roe_valido_emite_token_solo_de_la_fase_pedida():
    roe = valid_roe()
    token = issue(roe, Phase.RECON, now=ts("2026-11-11T10:00:00-03:00"))
    assert token.phase is Phase.RECON
    assert token.engagement_id == "eng-lab-001"
    with pytest.raises(TokenIssuanceError, match="fase"):
        issue(roe, Phase.VALIDATE, now=ts("2026-11-11T10:00:00-03:00"))


def test_token_vencido_no_se_renueva_solo():
    roe = valid_roe()
    now = ts("2026-11-11T10:00:00-03:00")
    token = issue(roe, Phase.RECON, now=now)
    assert token.window_end <= roe.window_end
    assert token.is_live(now + 1)
    assert not token.is_live(token.window_end + 1)
    with pytest.raises(TokenIssuanceError, match="ventana"):
        issue(roe, Phase.RECON, now=roe.window_end + 1)


def test_roe_revocado_no_emite():
    roe = parse(roe_dict(revoked_at="2026-11-11T10:30:00-03:00"))
    with pytest.raises(TokenIssuanceError, match="revoc"):
        issue(roe, Phase.RECON, now=ts("2026-11-11T11:00:00-03:00"))


# --- Requisito: emisión y rechazo registrados ------------------------------


def test_emision_y_rechazo_quedan_en_la_bitacora():
    audit = AuditLog()
    roe = valid_roe()
    issue(roe, Phase.RECON, now=ts("2026-11-11T10:00:00-03:00"), audit=audit)
    with pytest.raises(TokenIssuanceError):
        issue(roe, Phase.VALIDATE, now=ts("2026-11-11T10:00:00-03:00"), audit=audit)
    assert [e["result"] for e in audit.entries] == [Result.OK.value, Result.BLOCKED.value]
    assert {e["action"] for e in audit.entries} == {"scope.issue_token"}


# --- Requisito: token ligado a su engagement -------------------------------


def test_token_de_otro_engagement_se_bloquea_y_registra():
    guard = Guard(phase_allowlist(), engagement_id="eng-1")
    h, audit = _env(guard)
    token = make_token()
    ajeno = ScopeToken("eng-2", token.allowed_cidrs, token.allowed_domains,
                       time.time() - 5, time.time() + 600, Phase.RECON)
    with pytest.raises(ScopeViolation):
        h.invoke("recon", act("httpx.probe", Phase.RECON), "10.0.0.5", ajeno)
    assert audit.entries[-1]["result"] == Result.BLOCKED.value
    assert h.invoke("recon", act("httpx.probe", Phase.RECON), "10.0.0.5", token)["ok"]


# --- Requisito: una sola ruta crea ScopeToken ------------------------------


def test_solo_el_emisor_construye_scope_token_en_harness():
    raiz = Path(__file__).resolve().parent.parent / "harness"
    infractores = []
    for archivo in raiz.rglob("*.py"):
        if archivo.name == "tokens.py":
            continue
        if "ScopeToken(" in archivo.read_text(encoding="utf-8"):
            infractores.append(archivo.relative_to(raiz).as_posix())
    assert infractores == [], f"ScopeToken creado fuera del emisor: {infractores}"
