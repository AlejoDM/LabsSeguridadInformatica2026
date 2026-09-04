# Informe — Laboratorio 05 · Reconocimiento

> Plantilla del entregable. Copiala a `entregas/lab05/grupoXX/informe.md` y
> completá cada sección. Borrá las instrucciones en cursiva antes de entregar.

**Grupo:** XX
**Integrantes:** *nombre — usuario GitHub* (uno por línea)
**Fecha:**

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
| 21 | | | | | | | |
| 80 | | | | | | | |
| 8080 | | | | | | | |
| 31337 | | | | | | | |

*Evidencia de respaldo: pegá abajo las salidas de comando que sostienen la tabla
(el `nmap -sV -p-`, los banners, los headers). Guardá los archivos completos en
`/loot`.*

```
(evidencia: nmap -sV -p- phantomcorp)
```

---

## 3. Preguntas de análisis

**P1 — El puerto que el escaneo default se perdió.**
*¿Por qué `-p-` lo encontró y el escaneo común no? ¿Qué regla operativa sacás?*

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
