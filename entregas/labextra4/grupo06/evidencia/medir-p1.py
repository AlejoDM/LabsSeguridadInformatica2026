#!/usr/bin/env python3
"""Valida hash_de() y mide tasas locales para el aporte P1.

Usa los salts y hashes del caso solo para comprobar el contrato de hash. Las
mediciones calculan candidatos sintéticos con hash_de(), sin buscar secretos.
"""
import importlib.util
import platform
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CRACKER = ROOT / "entregas/labextra4/grupo06/cracker.py"
SOMBRA = ROOT / "labs/labextra4-cracking/caso/sombra.txt"
DICCIONARIO = ROOT / "labs/labextra4-cracking/caso/diccionario.txt"
MUESTRAS = {"md5": 100, "sha256": 100, "pbkdf2": 20}


def cargar_modulo():
    spec = importlib.util.spec_from_file_location("cracker_p1", CRACKER)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def cargar_registros():
    registros = {}
    with SOMBRA.open(encoding="utf-8-sig") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea and not linea.startswith("#"):
                usuario, algoritmo, salt, hash_hex = linea.split(":")
                registros[algoritmo] = (usuario, salt, hash_hex)
    return registros


def candidatos_diccionario():
    with DICCIONARIO.open(encoding="utf-8-sig") as archivo:
        return sum(bool(linea.strip()) and not linea.lstrip().startswith("#")
                   for linea in archivo)


def main():
    cracker = cargar_modulo()
    registros = cargar_registros()
    print(f"Python: {platform.python_version()}")
    print(f"Sistema: {platform.platform()}")
    print(f"Procesador: {platform.processor() or 'no informado'}")
    print(f"Candidatos del diccionario: {candidatos_diccionario()}")

    for algoritmo, (_usuario, salt, esperado) in registros.items():
        obtenido = cracker.hash_de(algoritmo, salt, "p1-control")
        print(f"Contrato {algoritmo}: salida hexadecimal de {len(obtenido)} caracteres")
        if algoritmo != "pbkdf2":
            assert obtenido != esperado, "El candidato de control no debe coincidir"

    for algoritmo, cantidad in MUESTRAS.items():
        _usuario, salt, _esperado = registros[algoritmo]
        inicio = time.perf_counter()
        for indice in range(cantidad):
            cracker.hash_de(algoritmo, salt, f"p1-medicion-{indice:03d}")
        segundos = time.perf_counter() - inicio
        tasa = cantidad / segundos
        print(
            f"Medicion {algoritmo}: {cantidad} intentos, {segundos:.6f} s, "
            f"{tasa:.2f} intentos/s, estimacion 49 candidatos: {49 / tasa:.6f} s"
        )

    try:
        cracker.hash_de("invalido", "00", "x")
    except ValueError as error:
        print(f"Algoritmo invalido: {error}")
    else:
        raise AssertionError("Se esperaba ValueError para un algoritmo invalido")


if __name__ == "__main__":
    main()
