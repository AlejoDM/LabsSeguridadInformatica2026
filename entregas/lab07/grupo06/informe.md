# Informe — Laboratorio 07 · Explotación

**Grupo:** 06
**Fecha:** 2026-10-23

| Nombre y apellido | Usuario de GitHub |
|---|---|
| Martín Beccereca | martinbeccereca |
| Belén Benito | belubenito01 |
| Alejo José De Miguel | AlejoDM |
| Tomás Giudici | TomasGiudici |
| Carolina Suppo | carosuppo |

## 0. Declaración de uso de IA

*Pendiente de completar por el grupo.*

## 1. Flags capturadas

*(salida de `./ctf status 07`, pendiente de completar cuando se resuelvan los 5 retos)*

## 2. Tabla de explotación

| Vuln | Payload usado | Consulta/comando/ruta resultante | Impacto | Defensa concreta |
|---|---|---|---|---|
| SQLi auth (R1) | | | | |
| SQLi UNION (R2) | | | | |
| Command injection (R3) | | | | |
| Path traversal (R4) | | | | |
| IDOR (R5) | | | | |

## 3. Preguntas de análisis
**P1 — por qué funciona el bypass (con la query).**
**P2 — por qué el UNION necesita igual número de columnas.**
**P3 — qué sigue después del RCE.**
**P4 — por qué parametrizar mata la SQLi.**
**P5 — dónde va el control de acceso (IDOR).**

## 4. Bitácora de comandos
```bash
# curl -s -X POST http://phantomcorp/login --data-urlencode "user=..." ...
```
