# P1 → P2: portal confirmado y contexto de continuidad

R1 resuelto. Objetivo: `http://phantomcorp/portal-rrhh`, accesible desde la consola Docker, sin credenciales. La URL no se presupone resoluble desde Windows.

## Cómo continuar

Desde la raíz del repositorio, abrir la consola:

```powershell
docker exec -it cyberlab-attacker bash
```

Dentro de ella, reproducir la línea base:

```bash
curl -sS -i --max-time 10 http://phantomcorp/portal-rrhh
```

Observado: HTTP 200, formulario `method=post`, `action=/portal/login`, campo `user` y campo `pass` de tipo password. P1 no envió el formulario ni obtuvo sesión. P2 puede comenzar estableciendo su línea base de autenticación y formular hipótesis a partir de respuestas reales. No se presupone el mecanismo de acceso.

## Evidencias y descubrimiento

`/` → consulta dirigida `/robots.txt` → línea Disallow `/portal-rrhh` → GET de esa ruta → portal confirmado. Salidas originales en `../salidas/p1-inicio.txt`, `p1-robots.txt`, `p1-r1-portal.txt` y `p1-control.txt`. La ruta de control respondió 404. Flag R1 validada; estado 1/4.

## Entorno entregado

Contenedores `cyberlab-attacker` y `cyberlab-phantomcorp` activos; se dejan encendidos para P2. Ningún otro contenedor se inició ni modificó. El montaje `/repo` del atacante es de solo lectura; `/loot` corresponde a `.loot/` del host. Guardar salidas propias con prefijo p2 y copiarlas después a `entregas/final/grupo06/evidencia/salidas/`; no sobrescribir evidencia P1.

Si el entorno se apagó, desde raíz:

```powershell
docker compose -p cyberlab --project-directory . -f entorno/docker-compose.yml -f labs/labfinal-practico-integrador/entorno/target.compose.yml up -d
```

No es necesario reconstruirlo para empezar. No ejecutar otros labs sobre el mismo nombre de contenedor mientras se trabaja en el integrador.

## Límites y revisión

Solo se reconoció el HTTP del objetivo autorizado. No hay acceso demostrado ni puntaje CVSS autónomo para R1. Metodología detallada en sección 2 del informe.

La revisión cruzada de otra sección se realizará cuando exista un aporte ajeno; no se afirma efectuada.
