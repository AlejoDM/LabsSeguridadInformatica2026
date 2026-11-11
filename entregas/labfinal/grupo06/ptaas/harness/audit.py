"""Contrato de la bitácora persistente (change 002). Firma + fake en memoria.

Invariantes que este contrato expresa:
  - append-only: no existe operación para modificar ni borrar registros.
  - cada registro guarda el hash del anterior; el primero usa GENESIS.
  - verify informa si la cadena está íntegra; nunca repara nada.
  - un evento con credenciales o contenido del cliente se rechaza (no se redacta).

La implementación SQLite (tareas 2.2 a 2.4) debe cumplir esta misma firma.
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol

GENESIS = "GENESIS"

# Claves que nunca pueden entrar a la bitácora. La detección es por nombre de
# campo: no inspecciona valores, así que no reemplaza una revisión de los eventos.
CLAVES_SENSIBLES = frozenset({
    "password", "passwd", "pass", "secreto", "secret", "api_key", "credencial",
    "contenido", "contenido_evidencia",
})


class EventoSensible(ValueError):
    """Se intentó registrar una clave sensible; el registro se rechaza."""


@dataclass(frozen=True)
class Entry:
    seq: int
    prev: str
    hash: str
    data: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    motivo: str = ""
    indice: int | None = None


def hash_de(prev: str, data: Mapping[str, Any]) -> str:
    cuerpo = {"prev": prev, **data}
    return hashlib.sha256(json.dumps(cuerpo, sort_keys=True).encode()).hexdigest()


def validar_evento(data: Mapping[str, Any]) -> None:
    sensibles = sorted(k for k in data if k.lower() in CLAVES_SENSIBLES)
    if sensibles:
        raise EventoSensible(f"campos sensibles no permitidos en la bitácora: {sensibles}")


def verificar_cadena(entries: Sequence[Entry]) -> VerifyResult:
    prev = GENESIS
    for indice, entrada in enumerate(entries):
        if entrada.prev != prev:
            return VerifyResult(False, "eslabón roto: prev no coincide", indice)
        if hash_de(entrada.prev, entrada.data) != entrada.hash:
            return VerifyResult(False, "hash no coincide con el contenido", indice)
        prev = entrada.hash
    return VerifyResult(True)


class AuditStore(Protocol):
    """Firma que comparten la implementación en memoria y la SQLite."""

    def append(self, data: Mapping[str, Any]) -> Entry:
        """Agrega un registro al final. Nunca modifica ni borra los anteriores."""
        ...

    def verify(self) -> VerifyResult:
        """Verifica la cadena completa del almacén abierto."""
        ...


class InMemoryAuditStore:
    """Fake del contrato: sin disco, mismas reglas de cadena y de datos."""

    def __init__(self) -> None:
        self._entries: list[Entry] = []

    def append(self, data: Mapping[str, Any]) -> Entry:
        validar_evento(data)
        prev = self._entries[-1].hash if self._entries else GENESIS
        evento = dict(data)
        entrada = Entry(len(self._entries) + 1, prev, hash_de(prev, evento), evento)
        self._entries.append(entrada)
        return entrada

    def verify(self) -> VerifyResult:
        return verificar_cadena(self._entries)

    def entries(self) -> list[Entry]:
        return list(self._entries)
