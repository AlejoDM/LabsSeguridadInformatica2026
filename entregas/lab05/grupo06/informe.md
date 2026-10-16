# Informe — Laboratorio 05 · Reconocimiento

**Grupo:** 06
**Fecha:** 2026-10-16

| Nombre y apellido | Usuario de GitHub |
|---|---|
| Martín Beccereca | martinbeccereca |
| Belén Benito | belubenito01 |
| Alejo José De Miguel | AlejoDM |
| Tomás Giudici | TomasGiudici |
| Carolina Suppo | carosuppo |

---

## 0. Declaración de uso de IA

*Obligatorio. Si usaron un asistente de IA, declaren para qué y cómo validaron
la salida. "No se usó" también es una declaración válida. Ver `CONTRIBUTING.md`.*

---

## 1. Parte práctica — flags capturadas

*Pegá la salida de `./ctf status 05`. Deberían verse las 5 marcadas.*

```
(salida de ./ctf status 05)
```

---

## 2. Mapa de superficie de ataque

*Una fila por servicio descubierto. Completá TODAS las columnas o justificá por
qué una queda vacía.*

| Puerto | Servicio | Versión (evidencia) | ¿Cómo lo identificaste? | CVE relevante | CVSS | Criticidad | Justificación (contra ESTE caso) |
|---|---|---|---|---|---|---|---|
| 21 | FTP | ProFTPD 1.3.5 — banner `220 ProFTPD 1.3.5 Server (PhantomCorp FTP)`; nmap `-sV`: `21/tcp open ftp ProFTPD 1.3.5` | Banner grabbing con `ncat -w2 phantomcorp 21` y confirmado con `nmap -Pn -sV -p-` | CVE-2015-3306 (`mod_copy`, comandos `SITE CPFR`/`SITE CPTO`) | 9.8 (CVSS v3.x, NVD) | Crítica | El banner confirma la versión 1.3.5, que es la afectada por el CVE. Permite leer y escribir archivos arbitrarios sin autenticarse **si** `mod_copy` está cargado; en este recon no lo probamos, queda para el lab de explotación. Además el banner filtra el nombre de la empresa y una línea `214` que no debería estar. |
| 80 | | | | | | | |
| 8080 | | | | | | | |
| 31337 | Desconocido (nmap lo adivina como `Elite` por el número de puerto) | "PhantomCorp maintenance shell v0.1" — banner de `ncat -w2 phantomcorp 31337`; nmap `-sV`: `31337/tcp open Elite?` | `nmap -sV -p-` no lo reconoció; lo identificamos conectando con `ncat` y leyendo el banner | Ninguno identificado. No pude asociar este banner a un producto con CVE público | N/A | Alta | Es un shell de mantenimiento propio, expuesto a la red y en un puerto clásico de backdoors. Responde sin pedir credenciales y su banner dice "acceso no autorizado prohibido", lo que confirma que no debería estar expuesto. No determiné qué comandos acepta, así que no afirmo más que eso. |

*Evidencia de respaldo: pegá abajo las salidas de comando que sostienen la tabla
(el `nmap -sV -p-`, los banners, los headers). Guardá los archivos completos en
`/loot`.*

```
(evidencia: nmap -sV -p- phantomcorp)
```

---

## 3. Preguntas de análisis

**P1 — El puerto que el escaneo default se perdió.**
En nuestra corrida el escaneo default (`nmap -Pn phantomcorp`, 1000 puertos) y el
completo (`nmap -Pn -sV -p- phantomcorp`) encontraron los mismos cuatro puertos:
21, 80, 8080 y 31337. El 31337 aparece en el default porque nmap incluye en su
lista de los 1000 más frecuentes a ese puerto histórico de backdoors. Lo que el
default sí se perdió fue la **identificación**: sin `-sV` el puerto figuró como
`Elite` (un nombre que nmap deduce solo del número de puerto) y recién con `-sV`
vimos que ahí responde un "maintenance shell" de PhantomCorp. Entonces `-p-` no
nos sumó un puerto nuevo en este caso, pero la lección operativa es la misma:
el default cubre 1000 de 65535 puertos, así que cualquier servicio fuera de esa
lista pasa desapercibido, y un puerto abierto sin versión no es un hallazgo.
Para los próximos recon hacemos siempre `-p-` con `-sV`, y confiamos en la
columna VERSION y en el banner, no en la columna SERVICE.

**P2 — El servicio dev en producción.**
*¿Qué evidencia concreta te dice que no era para producción? ¿Por qué es un
problema aunque no tenga un CVE conocido?*

**P3 — La ironía de `robots.txt`.**
*¿Para qué se creó? ¿Por qué termina ayudando al atacante?*

**P4 — Pasivo vs. activo.**
*Diferenciá con algo que hiciste. ¿Cuál de tus acciones habría quedado en los
logs de PhantomCorp?*

**P5 — Ahora sos el defensor.**
*Elegí dos hallazgos y proponé, para cada uno, una medida concreta que reduzca
la superficie de ataque de PhantomCorp.*

---

## 4. Bitácora de comandos

*Los comandos clave que ejecutaste, en orden. Que otro pueda reproducir tu recon
leyendo esto. No hace falta pegar todo: los que importan.*

```bash
# ejemplo:
# nmap -Pn -sV -p- phantomcorp
```
