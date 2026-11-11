"""Change 002 · contrato de la bitácora: cadena, datos sensibles y ausencia de borrado."""
import pytest

from harness.audit import GENESIS, Entry, EventoSensible, InMemoryAuditStore, verificar_cadena


def _llenar(store: InMemoryAuditStore, n: int = 3) -> None:
    for i in range(n):
        store.append({"engagement": "eng-1", "action": f"a{i}", "target": "10.0.0.5",
                      "result": "OK"})


def test_primer_registro_usa_genesis_y_cadena_integra():
    store = InMemoryAuditStore()
    _llenar(store)
    primero = store.entries()[0]
    assert primero.prev == GENESIS
    assert store.verify().ok


def test_alterar_un_campo_intermedio_hace_fallar_la_verificacion():
    store = InMemoryAuditStore()
    _llenar(store)
    lista = store.entries()
    viejo = lista[1]
    lista[1] = Entry(viejo.seq, viejo.prev, viejo.hash, {**viejo.data, "target": "10.9.9.9"})
    resultado = verificar_cadena(lista)
    assert not resultado.ok
    assert resultado.indice == 1


def test_borrar_un_registro_intermedio_hace_fallar_la_verificacion():
    store = InMemoryAuditStore()
    _llenar(store, 4)
    lista = store.entries()
    del lista[1]
    assert not verificar_cadena(lista).ok


def test_evento_con_credencial_se_rechaza_y_no_deja_registro():
    store = InMemoryAuditStore()
    with pytest.raises(EventoSensible):
        store.append({"engagement": "eng-1", "action": "login", "password": "x"})
    assert store.entries() == []


def test_el_contrato_no_expone_operaciones_de_modificacion_ni_borrado():
    for prohibida in ("update", "delete", "remove", "set", "clear"):
        assert not hasattr(InMemoryAuditStore, prohibida)
