# Informe — Laboratorio 06 · Enumeración

**Grupo:** 06
**Integrantes:**

| Nombre y apellido    | Usuario de GitHub |
| -------------------- | ----------------- |
| Martín Beccereca     | martinbeccereca   |
| Belén Benito         | belubenito01      |
| Alejo José De Miguel | AlejoDM           |
| Tomás Giudici        | TomasGiudici      |
| Carolina Suppo       | carosuppo         |

**Fecha:** 21/10/2026

## 0. Declaración de uso de IA

**Herramienta:** Codex.

- **Finalidad del uso:** apoyo para interpretar la consigna, planificar el reparto de tareas y elaborar el borrador inicial de este informe.
- **Partes asistidas:** planificación del Lab 06; bitácora y organización de sus evidencias.
- **Verificación:** la enumeración y la confirmación se ejecutaron contra el contenedor `phantomcorp` provisto por la cátedra. Las salidas originales de `dirb`, `curl`, el envío de la flag y el estado del motor se conservaron en `evidencias/`. El grupo debe revisar y poder explicar todo el contenido antes de entregar.

## 1. Flags capturadas

| Reto                                 | Estado    | Evidencia                                                                                                |
| ------------------------------------ | --------- | -------------------------------------------------------------------------------------------------------- |
| R1 — Enumeración de directorios      | Resuelto  | [Envío de R1](evidencias/lab06-r1-submit.txt) y [estado posterior](evidencias/lab06-status-after-r1.txt) |
| R2 — Repositorio Git expuesto        | Pendiente | —                                                                                                        |
| R3 — Métodos HTTP peligrosos         | Pendiente | —                                                                                                        |
| R4 — Enumeración de usuarios vía API | Pendiente | —                                                                                                        |
| R5 — Fingerprinting de tecnología    | Pendiente | —                                                                                                        |

La salida de estado posterior al R1 registra 1 de 5 retos resueltos. El archivo [progreso-06.done](evidencias/progreso-06.done) es una copia del estado local del motor y complementa, pero no reemplaza, la salida legible de `./ctf status 06`.

## 2. Inventario de enumeración

| Hallazgo                                            | Ruta/Método | Técnica                                                               | Evidencia                                                                                                                                                                                                               | Riesgo                                                                                                                                                                                                                     | ¿Qué habilita para el Lab 07?                                                                                                                                                                                                    |
| --------------------------------------------------- | ----------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Directorio de respaldos accesible sin autenticación | `/backup`   | Enumeración de directorios con `dirb`; confirmación manual con `curl` | `dirb` reportó `/backup` con `200`; la respuesta HTTP lista `respaldo-db-2024.sql.gz` y `config.old`. Ver [salida de dirb](evidencias/lab06-r1-dirb.txt) y [confirmación de `/backup`](evidencias/lab06-r1-backup.txt). | Un tercero con acceso al servicio puede consultar el índice observado. Los nombres de archivos son indicios de datos y configuraciones potencialmente sensibles; no se descargó ni verificó el contenido de esos archivos. | Orienta el análisis posterior hacia respaldos y configuraciones expuestos. Si alguno fuera accesible y contuviera datos o credenciales, podría habilitar nuevas hipótesis de explotación; esa condición no fue verificada en R1. |

### Evidencia del R1

Extracto de la enumeración:

```text
+ http://phantomcorp/admin (CODE:403|SIZE:65)
+ http://phantomcorp/backup (CODE:200|SIZE:249)
```

La respuesta `403` de `/admin` indica que la ruta existe, pero no demuestra que su contenido sea accesible. La respuesta `200` de `/backup` permitió confirmar un directorio accesible y observar su listado. Las salidas completas se conservan en los enlaces de la tabla.

## 3. Preguntas de análisis

### P1 — Enumeración vs. recon

En el Lab 05 realizamos reconocimiento para construir un mapa amplio de la superficie de PhantomCorp. Con `nmap -Pn -sV -p- phantomcorp` identificamos cuatro servicios expuestos: FTP en 21, HTTP en 80, HTTP/API en 8080 y un servicio no identificado en 31337. También usamos headers HTTP y `robots.txt` para reunir indicios iniciales sobre el servicio web. El resultado fue conocer qué servicios estaban disponibles y cuáles requerían análisis posterior.

En el Lab 06 realizamos enumeración sobre el servicio web identificado. Ejecutamos `dirb http://phantomcorp/`, que encontró `/admin` con código `403` y `/backup` con código `200`. Luego confirmamos este último recurso con `curl -sS -i http://phantomcorp/backup`; la respuesta mostró un listado que incluye `respaldo-db-2024.sql.gz` y `config.old`. Estas observaciones están respaldadas por las salidas de R1 enlazadas en el inventario.

Por lo tanto, el reconocimiento respondió qué servicios existían y dónde estaban; la enumeración profundizó dentro de uno de esos servicios para identificar recursos no enlazados, su nivel de acceso y sus consecuencias potenciales. El Lab 05 produjo el mapa inicial y el Lab 06 comienza a construir el inventario detallado que orientará hipótesis para el Lab 07.

### P2 — El `.git` expuesto

_Pendiente de completar con la evidencia de R2._

### P3 — El método `PUT`

_Pendiente de completar con la evidencia de R3. No realizar cargas al target._

### P4 — Enumeración de usuarios

_Pendiente de completar con la evidencia de R4._

### P5 — Rol defensor (3 mitigaciones)

_Pendiente de completar una vez documentados al menos tres hallazgos._

## 4. Bitácora de comandos

Los siguientes comandos se ejecutaron contra el contenedor autorizado `phantomcorp`, desde `cyberlab-attacker`:

```bash
dirb http://phantomcorp/ -S
curl -sS -i http://phantomcorp/backup
```

Desde la raíz del repositorio se registró la flag observada y se verificó el estado:

```bash
./ctf submit 06 R1 'FLAG{dir_enumeration_backup}'
./ctf status 06
```

Las salidas completas se preservan en `evidencias/`. Las operaciones se limitaron al target del Lab 06 provisto por la cátedra.
