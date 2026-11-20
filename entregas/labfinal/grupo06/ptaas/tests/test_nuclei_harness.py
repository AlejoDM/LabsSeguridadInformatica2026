"""Change 005 · 3.3 (cierre por P5): Nuclei a través de Harness.invoke.

Regresión: el adaptador real `NucleiSafeTemplates` exigía una URL, pero el Guard del
harness evalúa un host. Con un host fallaba la validación de URL del adaptador; con
una URL el Guard la bloqueaba. Los tests del loop B usaban un adaptador falso y no lo
detectaban. El adaptador ahora recibe el host del lab y arma la URL, como ZAP.
"""
import time

import pytest

from harness.adapters.common import InvalidTarget
from harness.adapters.nuclei_adapter import NucleiSafeTemplates
from harness.contracts import (
    Action,
    AuditLog,
    Guard,
    Harness,
    KillSwitch,
    Phase,
    ScopeToken,
    ScopeViolation,
)
from harness.policy_loader import phase_allowlist

ENG = "p5-nuclei"


def token():
    now = time.time()
    return ScopeToken(ENG, ("10.99.0.0/24",), ("dvwa.lab.test", "juiceshop.lab.test"),
                      now - 5, now + 60, Phase.ANALYZE)


def harness(runner, approved=("dvwa.lab.test",)):
    guard = Guard(phase_allowlist(), engagement_id=ENG,
                  approvals={f"nuclei.safe_templates@{h}" for h in approved})
    return Harness(guard, AuditLog(), {"nuclei.safe_templates": NucleiSafeTemplates(runner)},
                   KillSwitch())


ACTION = Action("nuclei.safe_templates", Phase.ANALYZE, requires_human_approval=True)


def test_nuclei_corre_por_el_harness_con_un_host_del_lab():
    calls = []

    def runner(argv, timeout):
        calls.append(argv)
        return '{"template-id": "p4-security-header-csp", "host": "http://dvwa.lab.test/"}\n'

    h = harness(runner)
    out = h.invoke("analysis", ACTION, "dvwa.lab.test", token())
    assert out["tool"] == "nuclei" and len(out["lines"]) == 1
    assert calls[0][calls[0].index("-u") + 1] == "http://dvwa.lab.test/"
    assert calls[0][calls[0].index("-t") + 1] == "templates/allowlist"
    assert h.audit.entries[-1]["result"] == "OK"


def test_juice_shop_usa_su_puerto_del_lab():
    from harness.adapters.nuclei_adapter import target_url
    assert target_url("juiceshop.lab.test") == "http://juiceshop.lab.test:3000/"


def test_host_fuera_del_lab_no_construye_url():
    from harness.adapters.nuclei_adapter import target_url
    with pytest.raises(InvalidTarget):
        target_url("example.com")


def test_sin_aprobacion_humana_queda_pendiente_y_no_ejecuta():
    calls = []
    h = harness(lambda argv, t: calls.append(argv) or "", approved=())
    out = h.invoke("analysis", ACTION, "dvwa.lab.test", token())
    assert out["status"] == "PENDING_HITL" and calls == []


def test_host_fuera_de_alcance_lo_bloquea_el_guard():
    calls = []
    h = harness(lambda argv, t: calls.append(argv) or "", approved=("example.com",))
    with pytest.raises(ScopeViolation):
        h.invoke("analysis", ACTION, "example.com", token())
    assert calls == []
