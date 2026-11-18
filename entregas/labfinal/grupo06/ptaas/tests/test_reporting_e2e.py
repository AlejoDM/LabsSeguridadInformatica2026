"""Scenarios del change 007 (P5): informe desde la bitácora, versionado, entrega con
aprobación registrada, datos sensibles, exportación a DefectDojo y procedencia.

Delta: openspec/changes/007-reporting-defectdojo/specs/reporting/spec.md
Diseño: openspec/changes/007-reporting-defectdojo/design.md

Los registros `validation.result` que arma `log_validation` imitan lo que escribe el
loop C (harness/validation.py); `test_informe_desde_una_corrida_real_del_loop_c`
usa el loop C de verdad. Las aprobaciones son precondiciones simuladas de cada
Scenario: prueban el control, no representan una aprobación humana real.
"""
import importlib
import json
from dataclasses import replace

import pytest

from harness.audit import InMemoryAuditStore
from harness.reporting import DeliveryNotApproved, Finding

ENG = "p5-test"
LOW = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N"
HIGH = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N"
REAL = {"recon": "real", "analysis": "real", "validation": "real"}
SCOPE = {"assets": "dvwa.lab.test", "window": "2026-11-18 09:00–18:00 UTC",
         "exclusions": "ninguna", "roe_ref": "RoE-lab-001",
         "disclosure": {"recipient": "Responsable del lab", "channel": "correo interno"}}


def api(module):
    return importlib.import_module("harness." + module)


def finding(fid="F1", *, title="Falta de protección contra clickjacking", asset="dvwa.lab.test",
            cwe="CWE-1021", vector=LOW, remediation="Enviar X-Frame-Options: DENY",
            status="not_validated", refs=(), epss=None):
    return Finding(fid, title, asset, cwe, vector, remediation, status, tuple(refs), epss)


def log_validation(ev, fid, status, *, poc_id="POC-HDR-001", reason=""):
    """Registro con el mismo formato que escribe el loop C (validation.result)."""
    return ev.append({"event": "validation.result", "engagement": ENG, "finding_id": fid,
                      "poc_id": poc_id, "poc_version": "1.0.0", "catalog_version": "0.1.0",
                      "params_hash": "h-" + fid, "status": status, "reason": reason,
                      "attempts": 2})


def build(findings, ev, *, stages=REAL, previous=None, scope=SCOPE):
    return api("report_builder").build_report(ENG, findings, evidence=ev, scope=scope,
                                               stages=stages, previous=previous)


def approvals(tmp_path, ev):
    return api("validation").ApprovalStore(tmp_path / "approvals.json", audit=ev)


def approve_delivery(store, report):
    store.approve_delivery(ENG, report.report_hash, reviewer="Ana Revisora",
                           reason="precondición del Scenario")


def by_id(report, fid):
    return next(f for f in report.findings if f.id == fid)


# ---- Requirement: estado de validación respaldado por la bitácora -------------


def test_hallazgo_validado_en_la_bitacora():
    ev = InMemoryAuditStore()
    entry = log_validation(ev, "F1", "validated")
    report = build([finding("F1", status="validated")], ev)
    f = by_id(report, "F1")
    assert f.status == "validated"
    assert f.status_label == "validado en sandbox"
    assert f.poc_id == "POC-HDR-001" and f.poc_version == "1.0.0"
    assert entry.hash in f.evidence_refs
    assert "validado en sandbox" in report.markdown


def test_estado_sale_de_la_bitacora_y_no_del_hallazgo():
    ev = InMemoryAuditStore()
    log_validation(ev, "F1", "validated")
    report = build([finding("F1", status="not_validated")], ev)
    assert by_id(report, "F1").status == "validated"


def test_validado_declarado_sin_respaldo_falla():
    rb = api("report_builder")
    ev = InMemoryAuditStore()
    with pytest.raises(rb.ReportError, match="F1"):
        build([finding("F1", status="validated")], ev)


def test_validado_declarado_con_resultado_negativo_en_bitacora_falla():
    rb = api("report_builder")
    ev = InMemoryAuditStore()
    log_validation(ev, "F1", "not_validated", reason="no se observó la debilidad")
    with pytest.raises(rb.ReportError, match="F1"):
        build([finding("F1", status="validated")], ev)


@pytest.mark.parametrize("status,reason", [("PENDING_HITL", "esperando aprobación del Reviewer"),
                                           ("not_validated", "sin aprobación")])
def test_hallazgo_pendiente_figura_sin_aprobacion(status, reason):
    ev = InMemoryAuditStore()
    log_validation(ev, "F1", status, reason=reason)
    f = by_id(build([finding("F1")], ev), "F1")
    assert f.status == "not_validated"
    assert f.status_label == "no validado (sin aprobación)"


def test_hallazgo_sin_ningun_registro_figura_sin_aprobacion():
    f = by_id(build([finding("F1")], InMemoryAuditStore()), "F1")
    assert f.status_label == "no validado (sin aprobación)"


def test_no_validado_de_impacto_alto_se_lista_y_se_destaca():
    ev = InMemoryAuditStore()
    log_validation(ev, "F9", "not_validated", reason="timeout")
    report = build([finding("F9", vector=HIGH), finding("F1")], ev)
    assert {f.id for f in report.findings} == {"F9", "F1"}
    resumen = report.markdown.split("## Alcance")[0]
    assert "requiere validación" in resumen and "F9" in resumen
    assert "F1" not in resumen


# ---- Requirement: referencias a la evidencia verificables ---------------------


def test_referencia_inexistente_falla():
    rb = api("report_builder")
    ev = InMemoryAuditStore()
    with pytest.raises(rb.ReportError, match="deadbeef"):
        build([finding("F1", refs=("deadbeef",))], ev)


def test_bitacora_alterada_no_genera_informe():
    rb = api("report_builder")
    ev = InMemoryAuditStore()
    log_validation(ev, "F1", "validated")
    log_validation(ev, "F2", "not_validated")
    original = ev._entries[0]
    ev._entries[0] = replace(original, data={**original.data, "status": "not_validated"})
    with pytest.raises(rb.ReportError, match="bitácora"):
        build([finding("F1")], ev)


def test_referencias_validas_y_cabeza_de_bitacora():
    ev = InMemoryAuditStore()
    previa = ev.append({"event": "sandbox.response", "engagement": ENG, "finding_id": "F1",
                        "poc_id": "POC-HDR-001", "body_sha256": "0" * 64, "body_len": 0,
                        "truncated": False, "http_status": 200})
    log_validation(ev, "F1", "validated")
    report = build([finding("F1", status="validated", refs=(previa.hash,))], ev)
    assert previa.hash in by_id(report, "F1").evidence_refs
    assert report.audit_head == ev.entries()[-1].hash
    assert report.audit_head in report.markdown


# ---- Requirement: informe versionado e identificado por su hash ---------------


def test_mismas_entradas_mismo_hash():
    ev = InMemoryAuditStore()
    log_validation(ev, "F1", "validated")
    a = build([finding("F1", status="validated")], ev)
    b = build([finding("F1", status="validated")], ev)
    assert a.report_hash == b.report_hash
    assert a.version == b.version == 1


def test_hallazgo_modificado_genera_version_nueva():
    ev = InMemoryAuditStore()
    v1 = build([finding("F1")], ev)
    v2 = build([finding("F1", remediation="Usar CSP frame-ancestors 'none'")], ev, previous=v1)
    assert v2.version == 2
    assert v2.report_hash != v1.report_hash
    assert v1.version == 1


# ---- Requirement: entrega con aprobación registrada y ligada al hash ----------


def test_entrega_sin_aprobacion_queda_en_report(tmp_path):
    rb = api("report_builder")
    ev = InMemoryAuditStore()
    report = build([finding("F1")], ev)
    with pytest.raises(DeliveryNotApproved):
        rb.deliver_report(report, approvals=approvals(tmp_path, ev), evidence=ev)
    assert report.delivered is False
    ultimo = dict(ev.entries()[-1].data)
    assert ultimo["event"] == "report.delivery" and ultimo["result"] == "PENDING_HITL"
    assert ultimo["report_hash"] == report.report_hash


def test_aprobacion_de_otra_version_se_rechaza(tmp_path):
    rb = api("report_builder")
    ev = InMemoryAuditStore()
    store = approvals(tmp_path, ev)
    v1 = build([finding("F1")], ev)
    approve_delivery(store, v1)
    v2 = build([finding("F1", remediation="otra")], ev, previous=v1)
    with pytest.raises(DeliveryNotApproved):
        rb.deliver_report(v2, approvals=store, evidence=ev)


def test_entrega_aprobada_queda_en_bitacora(tmp_path):
    rb = api("report_builder")
    ev = InMemoryAuditStore()
    store = approvals(tmp_path, ev)
    report = build([finding("F1")], ev)
    approve_delivery(store, report)
    entregado = rb.deliver_report(report, approvals=store, evidence=ev)
    assert entregado.delivered is True
    registro = [dict(e.data) for e in ev.entries() if dict(e.data).get("event") == "report.delivery"][-1]
    assert registro["result"] == "DELIVERED"
    assert registro["report_hash"] == report.report_hash
    assert registro["reviewer"] == "Ana Revisora" and registro["reason"]
    assert ev.verify().ok


def cli(argv, **kw):
    try:
        return api("validation_cli").main(argv, **kw)
    except SystemExit as e:
        return e.code


def test_cli_approve_delivery_sin_motivo_falla(tmp_path):
    ev = InMemoryAuditStore()
    report = build([finding("F1")], ev)
    path = tmp_path / "approvals.json"
    rc = cli(["--store", str(path), "approve-delivery", ENG, "--report-hash", report.report_hash,
              "--reviewer", "Ana"], audit=ev)
    assert rc != 0
    store = api("validation").ApprovalStore(path, audit=ev)
    assert not store.delivery_approved(ENG, report.report_hash)


def test_cli_approve_delivery_registra_la_aprobacion(tmp_path):
    ev = InMemoryAuditStore()
    report = build([finding("F1")], ev)
    path = tmp_path / "approvals.json"
    rc = cli(["--store", str(path), "approve-delivery", ENG, "--report-hash", report.report_hash,
              "--reviewer", "Ana", "--reason", "revisado"], audit=ev)
    assert rc == 0
    assert api("validation").ApprovalStore(path, audit=ev).delivery_approved(
        ENG, report.report_hash)


def test_deliver_con_booleano_no_alcanza_para_el_gate_registrado(tmp_path):
    """El `deliver(report, True)` heredado no deja aprobación registrada para el hash."""
    from harness.reporting import deliver
    rb = api("report_builder")
    ev = InMemoryAuditStore()
    report = build([finding("F1")], ev)
    deliver({"engagement_id": ENG, "delivered": False}, True)
    with pytest.raises(DeliveryNotApproved):
        rb.deliver_report(report, approvals=approvals(tmp_path, ev), evidence=ev)


# ---- Requirement: sin datos sensibles en el informe ---------------------------


@pytest.mark.parametrize("campo,valor,patron", [
    ("title", "Cookie PHPSESSID=abc123 sin HttpOnly", "cookie de sesión"),
    ("remediation", "Rotar eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.c2lnbmF0dXJh", "token JWT"),
    ("remediation", "Authorization: Bearer abc.def", "Authorization"),
    ("remediation", "Cambiar password=admin123", "contraseña"),
    ("title", "-----BEGIN RSA PRIVATE KEY----- expuesta", "clave privada"),
    ("title", "Reflejo de ptaas1a2b3c4d en la respuesta", "canario"),
])
def test_dato_sensible_falla_indicando_patron_y_hallazgo(campo, valor, patron):
    rb = api("report_builder")
    f = replace(finding("F7"), **{campo: valor})
    with pytest.raises(rb.SensitiveDataError) as exc:
        build([f], InMemoryAuditStore())
    assert patron in str(exc.value) and "F7" in str(exc.value)


def test_informe_sin_datos_sensibles_se_genera():
    report = build([finding("F1"), finding("F2", cwe="CWE-693", title="Sin CSP")],
                   InMemoryAuditStore())
    assert len(report.findings) == 2


# ---- Requirement: exportación al formato de importación de DefectDojo ---------


def delivered_report(tmp_path, ev, findings):
    rb = api("report_builder")
    store = approvals(tmp_path, ev)
    report = build(findings, ev)
    approve_delivery(store, report)
    return rb.deliver_report(report, approvals=store, evidence=ev)


def test_exportar_un_informe_no_entregado_se_rechaza(tmp_path):
    ev = InMemoryAuditStore()
    report = build([finding("F1")], ev)
    out = tmp_path / "dd.json"
    with pytest.raises(DeliveryNotApproved):
        api("defectdojo_export").export(report, out)
    assert not out.exists()


def test_contenido_exportado(tmp_path):
    ev = InMemoryAuditStore()
    ev.append({"event": "sandbox.response", "engagement": ENG, "finding_id": "F1",
               "poc_id": "POC-HDR-001", "body_sha256": "a" * 64, "body_len": 10,
               "truncated": False, "http_status": 200})
    entry = log_validation(ev, "F1", "validated")
    report = delivered_report(tmp_path, ev, [finding("F1", status="validated", epss=0.25)])
    out = tmp_path / "dd.json"
    api("defectdojo_export").export(report, out)
    data = json.loads(out.read_text(encoding="utf-8"))
    (f,) = data["findings"]
    assert f["title"] == "Falta de protección contra clickjacking"
    assert f["cwe"] == 1021
    assert f["mitigation"] == "Enviar X-Frame-Options: DENY"
    assert f["unique_id_from_tool"] == by_id(report, "F1").stable_id
    assert f["verified"] is True
    for texto in ("dvwa.lab.test", LOW, "25%", "validado en sandbox", entry.hash):
        assert texto in f["description"]
    crudo = out.read_text(encoding="utf-8")
    for prohibido in ("Ana Revisora", "body_sha256", "set_cookies", "canary", "PHPSESSID"):
        assert prohibido not in crudo


def test_severidad_desconocida_no_se_inventa(tmp_path):
    ev = InMemoryAuditStore()
    report = delivered_report(tmp_path, ev, [finding("F1")])
    out = tmp_path / "dd.json"
    api("defectdojo_export").export(report, out)
    (f,) = json.loads(out.read_text(encoding="utf-8"))["findings"]
    assert "severity-unknown" in f["tags"]
    assert "no fue calculada" in f["description"]


def test_hallazgos_duplicados_se_unen(tmp_path):
    ev = InMemoryAuditStore()
    a = log_validation(ev, "F1", "not_validated", reason="no se observó la debilidad")
    b = log_validation(ev, "F2", "not_validated", reason="no se observó la debilidad")
    report = build([finding("F1"), finding("F2")], ev)
    assert len(report.findings) == 1
    (f,) = report.findings
    assert {a.hash, b.hash} <= set(f.evidence_refs)
    entregado = delivered_report(tmp_path, ev, [finding("F1"), finding("F2")])
    out = tmp_path / "dd.json"
    api("defectdojo_export").export(entregado, out)
    ids = [x["unique_id_from_tool"] for x in json.loads(out.read_text(encoding="utf-8"))["findings"]]
    assert len(ids) == len(set(ids)) == 1


def test_identificador_estable_entre_corridas():
    ev1, ev2 = InMemoryAuditStore(), InMemoryAuditStore()
    a = by_id(build([finding("F1")], ev1), "F1").stable_id
    b = by_id(build([finding("F1")], ev2), "F1").stable_id
    c = by_id(build([finding("F1", asset="juiceshop.lab.test")], ev2), "F1").stable_id
    assert a == b != c


# ---- Requirement: procedencia declarada de cada etapa ---------------------------


def test_etapa_simulada_marca_demo():
    stages = {"recon": "real", "analysis": "fixture", "validation": "real"}
    report = build([finding("F1")], InMemoryAuditStore(), stages=stages)
    assert report.demo is True
    encabezado = report.markdown.split("## Resumen ejecutivo")[0]
    assert "DEMO" in encabezado and "analysis" in encabezado


def test_procedencia_invalida_se_rechaza():
    rb = api("report_builder")
    with pytest.raises(rb.ReportError):
        build([finding("F1")], InMemoryAuditStore(), stages={"recon": "casi real"})


def test_informe_demo_no_se_entrega_ni_exporta(tmp_path):
    rb = api("report_builder")
    ev = InMemoryAuditStore()
    store = approvals(tmp_path, ev)
    report = build([finding("F1")], ev, stages={"recon": "real", "analysis": "fixture"})
    approve_delivery(store, report)
    with pytest.raises(rb.DemoReport, match="simulad"):
        rb.deliver_report(report, approvals=store, evidence=ev)
    with pytest.raises(rb.DemoReport):
        api("defectdojo_export").export(replace(report, delivered=True), tmp_path / "dd.json")
    assert not (tmp_path / "dd.json").exists()


def test_informe_real_no_es_demo():
    assert build([finding("F1")], InMemoryAuditStore()).demo is False


# ---- Requirement: sección de divulgación --------------------------------------


def test_divulgacion_con_datos_ausentes_usa_unknown():
    report = build([finding("F1")], InMemoryAuditStore())
    seccion = report.markdown.split("## Divulgación")[1]
    assert "Responsable del lab" in seccion
    assert "Plazo de remediación: unknown" in seccion


def test_divulgacion_sin_datos_en_el_roe():
    scope = {k: v for k, v in SCOPE.items() if k != "disclosure"}
    seccion = build([finding("F1")], InMemoryAuditStore(), scope=scope).markdown.split(
        "## Divulgación")[1]
    assert seccion.count("unknown") >= 4


# ---- Integración con el loop C real (change 006) --------------------------------


def test_informe_desde_una_corrida_real_del_loop_c(tmp_path):
    from tests.test_sandbox_loop_c import (FakeRuntime, approved_store, ok_response, request,
                                           run_loop, setup)
    _, h, tok, sender, _, ev = setup(FakeRuntime(ok_response(headers={})))
    req = request("F1", "POC-HDR-001")
    run_loop(h, tok, sender, [req], approved_store(tmp_path, req, evidence=ev), ev)
    report = build([finding("F1")], ev)
    f = by_id(report, "F1")
    assert f.status == "validated"
    respuestas = [e.hash for e in ev.entries() if dict(e.data).get("event") == "sandbox.response"]
    assert respuestas and set(respuestas) <= set(f.evidence_refs)
