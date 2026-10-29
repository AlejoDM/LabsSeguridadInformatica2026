# Research — Lab Extra 2: El repo que delata

**Grupo:** 06
**Fecha:** 2026-10-29
**Opción elegida:** A — Herramientas reales (detección y limpieza de secretos en Git)

**Declaración de uso de IA:** (pendiente de completar por el grupo antes de entregar — ver indicación aparte)

## 1. Detección: Gitleaks

Gitleaks es un escáner de línea de comandos, de código abierto, que busca contraseñas, claves de API y otras credenciales tanto en el árbol de trabajo actual como en **toda la historia de Git** de un repositorio. Trabaja por reglas: compara el contenido contra expresiones regulares conocidas (claves de AWS, tokens de GitHub, cadenas de conexión, etc.) y permite escribir reglas propias en TOML, además de mantener una lista de permitidos para falsos positivos ya revisados.

**Cómo se usaría en un pipeline de CI:** el comando `gitleaks detect` se ejecuta sobre el repositorio clonado en cada pull request o push, y puede integrarse como paso de un workflow de CI o como GitHub Action; además existe `gitleaks protect`, pensado para correr como hook `pre-commit` local y revisar únicamente los cambios que el desarrollador está por confirmar, antes de que lleguen al historial. En el caso de este laboratorio, un escaneo con `gitleaks detect --log-opts="--all"` sobre `repo-delata` habría señalado los tres secretos de R1, R2 y R3, porque recorre commits accesibles por cualquier referencia, no solo la punta de `main`.

**Qué no resuelve:** Gitleaks encuentra secretos, pero no los elimina ni los invalida. Si corre solo sobre el árbol actual (sin `--log-opts="--all"` o el flag equivalente), no ve lo que quedó en ramas no fusionadas como `feature/pasarela-pagos` del caso, ni objetos colgantes como el que R2 recuperó del reflog. Sus reglas son patrones conocidos: una credencial con un formato atípico, o un valor que no coincide con ninguna firma reconocida, puede pasar inadvertido. Y, sobre todo, detectar un secreto no lo rota: si ya se filtró, Gitleaks no hace nada por sí solo para revocarlo.

## 2. Limpieza: `git filter-repo`

`git filter-repo` es la herramienta que el propio proyecto Git recomienda hoy para reescribir historia, en reemplazo del antiguo `git filter-branch` (lento y propenso a errores) y como alternativa más mantenida a BFG Repo-Cleaner. Permite, entre otras operaciones, eliminar un archivo de todos los commits en los que aparece, o reemplazar cadenas de texto específicas (por ejemplo, el valor de una credencial) en toda la historia.

**Cómo se usaría en una respuesta a incidente:** sobre una copia nueva y exclusiva del repositorio (el propio proyecto recomienda operar sobre un clon fresco, no sobre el checkout de trabajo diario), se ejecutaría algo equivalente a `git filter-repo --path .env.pasarela --invert-paths` para purgar el archivo comprometido de R3 de todos los commits que lo contienen, o `git filter-repo --replace-text secretos.txt` para sustituir el valor expuesto en cualquier blob donde aparezca. Tras la reescritura, hay que forzar el push de las referencias afectadas y coordinar que **todos** los colaboradores descarten sus clones viejos y vuelvan a clonar, porque los hashes de cada commit reescrito cambian.

**Qué no resuelve:** `git filter-repo` actúa únicamente sobre las copias del repositorio a las que se le aplique; no toca clones locales de otros colaboradores, forks ya existentes en GitHub, ni copias cacheadas por la propia plataforma (por ejemplo, un commit todavía accesible por su hash directo aunque ninguna rama lo referencie). Tampoco es una herramienta de CI que corra automáticamente en cada push: es una operación puntual, coordinada y disruptiva, pensada para una remediación concreta, no para prevención continua. Y, igual que con la detección, reescribir la historia **no revoca** el secreto: si la credencial seguía siendo válida, sigue siéndolo después de la limpieza, exactamente el punto que el plan de la sección 4 de este informe prioriza (rotar antes de reescribir).

## 3. Pregunta de cierre — por qué el secret scanning de GitHub no alcanza

GitHub escanea los *pushes* públicos en busca de patrones de secretos conocidos (GitHub Secret Scanning) y, para ciertos proveedores asociados, notifica directamente para que se revoque la credencial; además, Push Protection puede bloquear un push antes de que el secreto llegue siquiera al repositorio. Aun así, quedan ventanas de exposición abiertas:

1. **El intervalo entre publicación, detección y revocación efectiva.** El escaneo no es instantáneo ni infalible para todo tipo de secreto (depende de los patrones que reconoce, igual que Gitleaks); y aunque notifique al proveedor, la revocación real depende de que ese proveedor actúe y de que el equipo afectado complete la rotación. Durante ese lapso —que puede ir de minutos a mucho más, según el caso— la credencial sigue siendo válida y explotable, tal como advierte el propio README del laboratorio sobre el tiempo mediano entre filtración y uso.
2. **Las copias hechas antes de cualquier aviso.** Push Protection bloquea el push que intenta introducir el secreto, pero no hace nada frente a un secreto que ya estaba en la historia antes de habilitarse, ni frente a clones y forks que un tercero ya haya realizado antes de que GitHub emitiera cualquier alerta. Exactamente el escenario de este laboratorio: el secreto de R3 vive en una rama nunca fusionada y el de R2 en un commit sin referencias; ninguno de los dos pasa por un push nuevo que Push Protection pudiera interceptar, y ambos dependen de que alguien los busque deliberadamente (como hizo el grupo) o de un escaneo retroactivo de toda la historia, no de uno automático sobre el último cambio.

Por eso el escaneo de GitHub y la notificación a proveedores reducen el riesgo, pero no sustituyen la disciplina de revisar toda la historia accesible (no solo el último commit) y de tratar cualquier secreto que haya pasado por un repositorio —aunque ya no esté en `main`— como comprometido hasta que se rote.

## 4. Fuentes

1. Gitleaks — repositorio oficial y documentación de uso (`gitleaks detect`, `gitleaks protect`, integración como hook y como acción de CI). https://github.com/gitleaks/gitleaks
2. `git filter-repo` — repositorio oficial de Elijah Newren, recomendado por el proyecto Git en reemplazo de `git filter-branch`. https://github.com/newren/git-filter-repo
3. GitHub Docs. *Working with secret scanning and push protection*. https://docs.github.com/en/code-security/secret-scanning/working-with-secret-scanning-and-push-protection
