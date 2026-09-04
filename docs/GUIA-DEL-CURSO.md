# Guía del curso — Laboratorios de Seguridad Informática

> Documento oficial. Panorama del práctico: qué es, cómo está organizado y cómo
> se trabaja. Para el detalle de cada laboratorio, entrá a su `README.md`.

## Qué es este práctico

Un recorrido **práctico y progresivo** por la seguridad ofensiva, de las
herramientas básicas a los agentes autónomos. No se aprende leyendo: se aprende
**haciendo**, operando herramientas reales contra objetivos deliberadamente
vulnerables que **se levantan solos en Docker**, dentro de tu propia máquina.

Dos tipos de laboratorio:

- **Labs de código (Unidades 1–4).** Fundamentos: la tríada CIA, hashing,
  criptografía, marcos normativos. Se resuelven en **Python** (biblioteca
  estándar).
- **Labs ofensivos (Unidades 5–9).** Pentesting hands-on. Corren en **Docker** y
  todas las herramientas vienen dentro de una "consola del atacante": no instalás
  nada. La dificultad y la autonomía crecen lab a lab.

## La filosofía

1. **Conceptos antes que código.** Cada lab explica el *porqué* antes de tocar una
   herramienta. Primero entendés, después ejecutás.
2. **A mano antes que automático.** Recon, enumeración, explotación y
   post-explotación se hacen **manualmente** primero. Recién al final (Unidad 9)
   aparecen los agentes de IA. Porque **no podés dirigir un agente que hace lo que
   vos no sabés hacer.**
3. **La IA es una herramienta; el humano dirige.** El agente acelera; no reemplaza
   tu criterio.
4. **Sin atajos.** El aprendizaje real lleva esfuerzo.

## El arco ofensivo (Unidades 5–9)

Un mismo hilo narrativo — la auditoría de la empresa ficticia **PhantomCorp** —
atraviesa las cinco unidades. Cada una continúa donde terminó la anterior:

| Unidad | Lab | Qué aprendés |
|---|---|---|
| 5 | **Reconocimiento** | Mapear la superficie: puertos, servicios, versiones |
| 6 | **Enumeración** | Sacarle todo a cada servicio: rutas, `.git`, APIs, métodos |
| 7 | **Explotación** | SQLi, inyección de comandos, path traversal, IDOR |
| 8 | **Post-explotación** | Escalar a root, pivotear a la red interna, automatizar |
| 9 | **Agentes** | Construir y dirigir un agente de IA que orquesta todo |

## Cómo se juega

Todo arranca con un comando autodescubrible desde la raíz del repo:

```bash
./ctf                 # muestra el plan de labs y tu progreso
./ctf lab 05          # arranca un lab: levanta su entorno y abre la guía
make shell            # entrás a la consola del atacante (todas las tools adentro)
```

Cada lab ofensivo esconde **flags** (`FLAG{...}`) en los servicios del objetivo.
Las descubrís operando las herramientas y las entregás:

```bash
./ctf submit 05 R1 'FLAG{...}'
./ctf status 05
```

> **Las flags te enganchan; el informe es lo que evalúa la rúbrica.** Capturar una
> flag demuestra que *pudiste*. El informe demuestra que *entendiste*.

## Cómo se entrega

Todo por **fork + Pull Request**, en grupos de 4 a 5, dentro de
`entregas/labNN/grupoXX/`. El procedimiento completo está en
[`../CONTRIBUTING.md`](../CONTRIBUTING.md). Cada lab tiene su rúbrica en
`labs/labNN-*/docs/rubrica.md` — **leela antes de empezar.**

## Requisitos

- **Docker** y **Docker Compose** (para los labs ofensivos).
- **Python 3.10+** (para los labs de código).
- **Git** y una cuenta de **GitHub** por integrante.
- Para el Lab 09 (opcional): una API key de Claude u OpenAI. Sin key, el lab corre
  con un motor `mock` offline.

## Uso responsable

Todo se practica **exclusivamente** contra los contenedores de la cátedra, en tu
máquina. Estas técnicas contra sistemas de terceros son **delito** en Argentina
(Ley 26.388). Ver [`../CONTRIBUTING.md`](../CONTRIBUTING.md) § Uso responsable.
