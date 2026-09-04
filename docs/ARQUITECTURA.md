# Arquitectura del motor

> Cómo funciona por dentro el sistema de laboratorios. Para docentes y para quien
> quiera extenderlo.

## Componentes

```
ctf                       Punto de entrada autodescubrible (CLI en bash)
Makefile                  Orquestación Docker (setup / lab / shell / down)
bin/
  ctf... (via ./ctf)      list · lab · status · submit
  lib/ui.sh               colores, cajas, barras de progreso
  lib/banner.sh           arte ASCII
  lib/check.sh            verificación de flags por SHA-256
  nueva-flag.sh           helper de autor: genera la línea del manifest
entorno/
  docker-compose.yml      compose BASE: la consola del atacante
  attacker/               imagen del atacante (nmap, dirb, sqlmap, ...)
labs/
  _plantilla/             molde para labs nuevos
  labNN-tema/
    README.md             el enunciado (anatomía de 4 partes)
    entorno/              target(s) Docker del lab + target.compose.yml
    retos.manifest        flags del lab (hasheadas)
    start.sh              genérico: deriva número/tema del nombre del dir
    src/                  código a completar (si aplica)
    docs/                 entregable, research, rúbrica
    solucion.md           SOLO DOCENTE
```

## Cómo se levanta un entorno

`make lab N=NN` combina dos archivos compose con `docker compose`:

```
docker compose --project-directory . \
  -f entorno/docker-compose.yml \                 # la consola del atacante
  -f labs/labNN-*/entorno/target.compose.yml \    # el/los target(s) del lab
  up -d --build
```

El `--project-directory .` fijo hace que **todas las rutas relativas se resuelvan
desde la raíz del repo**, de forma determinística (un detalle importante de
Docker Compose v2 al combinar múltiples `-f`).

La consola del atacante y los targets comparten una red (`labnet`). El alumno
opera desde la consola (`make shell`) y alcanza los targets por su hostname
(`phantomcorp`). Los puertos **no** se publican al host: más realista y no expone
nada en la máquina del alumno.

El Lab 08 agrega una segunda red **`internalnet`** (`internal: true`) para enseñar
**pivoting**: el host víctima está en las dos redes, el host interno solo en la
interna, y la consola del atacante no llega a la interna. Segmentación real.

## Cómo funcionan las flags

- Cada flag se esconde en el **comportamiento** del target (un banner, un header,
  una respuesta), **ofuscada en base64** en el código del target para que un
  vistazo casual al source no la regale.
- El `retos.manifest` de cada lab guarda solo el **SHA-256** de cada flag
  (`id|título|hash`), nunca la flag en claro.
- `./ctf submit` hashea lo que entrega el alumno y lo compara. El progreso se
  guarda en `.progreso/` (gitignored).
- Las flags en claro viven únicamente en `solucion.md` (solo docente).

## Por qué esta arquitectura

- **Reproducible.** Mismo lab en cualquier SO con Docker. Se destruye y recrea.
- **Aislada.** La máquina del alumno queda limpia; todo vive en contenedores.
- **Autodescubrible.** `./ctf` guía; los banners y barras de progreso orientan.
- **Extensible.** Un lab nuevo es copiar la plantilla y rellenar.
- **Segura por diseño.** Los targets no se exponen al host; el Lab 09 tiene
  guardrails de alcance en el código del agente.
