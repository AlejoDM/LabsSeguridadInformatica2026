# Informe — Laboratorio Extra 2: El repo que delata

**Grupo:** 06
**Fecha:** 2026-10-23

| Nombre y apellido | Usuario de GitHub |
|---|---|
| Martín Beccereca | martinbeccereca |
| Belén Benito | belubenito603 |
| Alejo José De Miguel | AlejoDM |
| Tomás Giudici | TomasGiudici |
| Carolina Suppo | carosuppo |

## 0. Declaración de uso de IA

**Herramienta:** Codex (OpenAI).

- **Finalidad y partes asistidas:** apoyo en la validación de R3 y redacción de respuestas.
- **Verificación:** Se contrastaron las indicaciones de la IA con los resultados obtenidos mediante comandos Git sobre el repositorio del caso. Para R3, se verificó la existencia de la rama abandonada, se inspeccionó su historial y se comprobó que contenía la información sensible identificada. Además, se revisaron las respuestas redactadas, contrastándolas con la evidencia recopilada y los conceptos explicados en la consigna del laboratorio.

**Herramienta:** Opencode.

- **Finalidad y partes asistidas:** apoyo para explicar la respuesta P2 sobre referencias y objetos de Git.
- **Verificación:** Se contrastó la explicación con la consigna y se reprodujeron los comandos `reflog`, `fsck` y `show` sobre el repositorio local del caso. Se revisaron las salidas crudas adjuntas y la aceptación del verificador; no se probó la credencial contra ningún servicio.

**Herramienta:** ChatGPT (OpenAI), aporte de Persona 5.

- **Finalidad:** asistencia para comprender y redactar los mecanismos preventivos de filtración de secretos en Git.
- **Parte asistida:** pregunta P5, sobre controles locales pre-commit y protección durante el push.
- **Verificación:** se revisó la coherencia de la respuesta con el enunciado y el alcance del laboratorio. La explicación es conceptual; no se instalaron ni ejecutaron herramientas de detección de secretos en el repositorio del caso.

**Herramienta:** Claude (Anthropic), vía Claude Code.

- **Finalidad y partes asistidas:** redacción del plan de remediación, y del research.md.
- **Verificación:** el plan de remediación se fundamentó contra la evidencia ya validada de R2/R3 y la línea de tiempo existente. Las afirmaciones técnicas sobre Gitleaks, git filter-repo y el secret scanning de GitHub se contrastaron contra sus repositorios/documentación oficial antes de incluirlas.

## 1. Línea de tiempo de la filtración

Fechas de autor y committer coinciden, con zona -03:00. No son fechas de publicación ni de descubrimiento: el caso se generó e investigó el 28/10/2026.

| Fecha registrada | Autor | Commit | Evento | Exposición / fuente |
|---|---|---|---|---|
| 2026-08-05 16:30 -03:00 | dev-jperez | 0abdf953b75b214af59d0cf31e55ccbf2c9873d8 | `wip: pasarela de pagos (falta todo)` agrega `.env.pasarela` y `pasarela.py` | Secreto de pagos en la rama; `r3-diff-introduccion.txt`. Fecha incoherente con su padre. |
| 2026-08-10 09:12 -03:00 | dev-jperez | de33a75843139302dfbe034cab11e8175881540e | Inicio de deploy-tool | Contexto legítimo según historial; `r3-historial.txt`. |
| 2026-08-10 18:47 -03:00 | dev-jperez | 9333f2b4a09f7a320cb66d621c3bd53b4f694941 | Configuración temporal del hotfix; padre del commit de pagos | R1 debe corroborar contenido y exposición del token; `r3-parentesco.txt`. |
| 2026-08-11 10:05 -03:00 | dev-jperez | eafb81c3ec5790ce4741629458e11ab5c1a690b8 | Mensaje de limpieza de credenciales | R1 debe documentar su diff; `r3-fechas.txt`. |
| 2026-08-12 14:22 -03:00 | dev-jperez | bc9d0dbe6aca41d639a515395cc983e139979102 | Commit de notas de investigación; luego `reset --hard` movió `main` a `eafb81c` | Incluyó una clave ficticia de staging en `notas_investigacion.txt`; quedó sin referencia de rama y fue recuperable localmente. `r2-reflog.txt`, `r2-reflog-fechas.txt`, `r2-fsck.txt`, `r2-objeto-recuperado.txt`. La fecha del reflog es local y no acredita publicación. |
| 2026-08-20 11:00 -03:00 | dev-jperez | fa714bda2ac9d31bf92774e901400be4a296c1e5 | Actualización documental, punta de `main` | Contexto; el secreto de pagos sigue en otra rama. |

**Inconsistencia temporal:** `git show -s --format=raw feature/pasarela-pagos` muestra que el padre de `0abdf95` es `9333f2b`, aunque la fecha del hijo es anterior. El orden topológico es inicial → hotfix → pagos, independientemente de esas fechas. No se corrige el caso ni se inventa una duración de exposición. La tabla ordena fechas declaradas, no demuestra el orden real de publicación. P2 aporta el evento del objeto no alcanzable; P1 aún debe integrar sus evidencias para completar la cronología del token.

## 2. Hallazgos

### R1 — Secreto en commit viejo


### R2 — Commit «perdido»

El reflog mostró el commit `bc9d0dbe6aca41d639a515395cc983e139979102` y el movimiento posterior `reset: moving to HEAD~1`, que dejó `main` en `eafb81c3ec5790ce4741629458e11ab5c1a690b8`. La búsqueda independiente con `git fsck --no-reflogs --unreachable --no-progress` identificó el mismo commit como `unreachable`. La captura con fechas registra ambos eventos del reflog a `2026-08-12 14:22:00 -0300`; esa hora es metadato local del reflog y no demuestra el instante real de publicación ni una exposición remota. Se inspeccionó el commit sin mover referencias:

```bash
git reflog show --all --format="%H %gd %gs"
git show bc9d0dbe6aca41d639a515395cc983e139979102
```

El commit, de autor y committer `dev-jperez <jperez@phantomcorp.example>` con fecha 12/08/2026 14:22:00 -03:00 y mensaje `wip: notas del cluster nuevo (no mergear todavia)`, añadió `notas_investigacion.txt`. El archivo contiene `staging_key: FLAG{git_reflog_rescata}` y la describe como llave del cluster de staging. Esto no demuestra que la clave fuera válida, qué permisos tenía ni que alguien la usara. Evidencias crudas: `evidencia/salidas/r2-reflog.txt`, `r2-fsck.txt` y `r2-objeto-recuperado.txt`.

La flag R2 fue aceptada. El intento inicial con `./ctf submit extra2 R2 ...` fue rechazado porque el manifiesto tiene finales CRLF y el hash esperado conserva el CR final. Para no modificar el manifiesto ni el verificador, `validar-r2-crlf.sh` reutiliza las funciones oficiales con una copia temporal del manifiesto normalizada; el verificador marcó R2 como resuelto. Se guardan ambos resultados en `r2-submit.txt` y `r2-submit-compatibilidad.txt`.

`reset --hard` actualiza `HEAD` y las referencias afectadas y ajusta el árbol de trabajo; no equivale a borrar inmediatamente los objetos almacenados. Un commit referencia un árbol, los árboles referencian blobs y otros árboles, y retirar una referencia no destruye de inmediato esa cadena de objetos. El reflog y los objetos no alcanzables son locales y temporales: su retención depende de la configuración y una recolección de basura puede eliminarlos. Hallarlos en una copia local no demuestra que hayan sido publicados ni distribuidos a otros clones.

### R3 — Rama abandonada

La pista del README menciona una integración de pagos. Primero se ejecutaron `git branch -a` y `git log --all --oneline --decorate`: apareció `feature/pasarela-pagos`. Su historial con `--format=fuller --name-status` identificó la incorporación de `.env.pasarela`. Luego `git show feature/pasarela-pagos:.env.pasarela` permitió leer el archivo sin cambiar de rama. Los comandos exactos, con rutas y contexto, están en `evidencia/comandos.txt`.

- **Referencia:** `refs/heads/feature/pasarela-pagos`.
- **Commit:** `0abdf953b75b214af59d0cf31e55ccbf2c9873d8`.
- **Autor y committer:** `dev-jperez <jperez@phantomcorp.example>`.
- **Fecha registrada:** 05/08/2026 16:30:00 -03:00, con la inconsistencia indicada arriba.
- **Archivo:** `.env.pasarela`.
- **Secreto ficticio:** `PAGOS_SECRET=FLAG{git_rama_abandonada}`.
- **Destino declarado:** `https://pagos.phantomcorp.example`; no se efectuaron conexiones ni pruebas con la credencial.

Contenido recuperado (salida íntegra en `evidencia/salidas/r3-rama-abandonada.txt`):

```text
# NO COMMITEAR ESTO (lo commitee igual, despues lo veo)
PAGOS_SECRET=FLAG{git_rama_abandonada}
PAGOS_ENDPOINT=https://pagos.phantomcorp.example
```

El diff contra `main` y su listado de archivos confirman que `.env.pasarela` y `pasarela.py` no están en su árbol actual. La rama sigue apuntando al commit que los incorpora: el secreto permanece alcanzable. Su nombre sugiere autenticación con una pasarela, pero la evidencia no demuestra permisos, vigencia, cargos posibles ni utilización externa. El código de integración es un esqueleto.

**Validación:** el primer `./ctf submit extra2 R3 ...` rechazó la flag. El campo hash del manifiesto tenía 65 caracteres, terminaba en CR (código 13) y coincidió con el SHA-256 de la flag al normalizar el final de línea. Esto se comprobó después de descubrir la flag en Git. Se reutilizaron las funciones oficiales con una copia temporal del manifiesto sin CR y sin `nounset` (el motor también usa variables locales en una misma declaración). No se editó el motor ni el manifiesto original. R3 fue aceptado y registrado por el verificador en `.progreso/extra2.done`. Se conservan el rechazo, el diagnóstico, el script de compatibilidad y la aceptación. El estado oficial posterior muestra **1/3, R3 resuelto**.

## 3. Evaluación de exposición

La publicación efectiva de cada referencia es decisiva. Si un bot recorre todas las ramas publicadas y busca nombres como `SECRET`, `.env.pasarela` es un candidato sencillo: está en la punta de una rama y no requiere recuperar objetos huérfanos. Un bot limitado al árbol actual de `main` lo omitiría. Un bot que recorra diffs históricos podría detectar el token de R1 aunque se haya borrado del árbol actual. R2 requiere que el objeto haya llegado a una copia accesible al bot; encontrarlo en el almacén local no prueba que se haya publicado ni que un clon común lo reciba.

**¿Cuál primero?** Bajo el supuesto de publicar cada commit alcanzable al crearlo y escanear sus cambios inmediatamente, R1 sería un candidato a detectarse antes de R3: su commit es ancestro del de pagos. Esto queda condicionado a la corroboración de P1 y a los tiempos de push desconocidos. Si se publica todo junto al final y se escanean primero las puntas de todas las ramas, R3 podría aparecer antes. No se puede establecer un ganador observado con estas evidencias; las fechas incoherentes tampoco permiten resolverlo.

**Tiempo estimado, como hipótesis:** con un escaneo cada minuto que cubra esa rama y reconozca el patrón, la detección podría ocurrir en el siguiente ciclo (aproximadamente 0–1 minuto más procesamiento). Con escaneo diario podría tardar hasta un día; sin cobertura podría no ocurrir. Son escenarios de planificación, no una medición ni una estadística del caso. Detectar tampoco implica utilizar: el uso depende de que la clave sea válida y de sus permisos. No hay telemetría de bots, accesos, publicación o revocación.

## 4. Plan de remediación (P4)

PhantomCorp ya publicó `deploy-tool` en GitHub y existen forks conocidos. El plan ordena las acciones por lo único que realmente contiene el riesgo primero, no por lo que resulta más cómodo de ejecutar en Git:

1. **Inventariar los tres secretos y su alcance real, sin reexponerlos.** El token de API identificado en la rama de hallazgos de R1 (commits de configuración del hotfix y de limpieza de credenciales ya ubicados en la línea de tiempo; evidencia detallada pendiente del responsable de R1), la clave de staging recuperada en R2 (`notas_investigacion.txt`, commit `bc9d0dbe6aca41d639a515395cc983e139979102`) y la credencial de la pasarela de pagos de R3 (`.env.pasarela`, rama `feature/pasarela-pagos`). Para cada una, determinar a qué sistema pertenece y qué permisos otorgaría si fuera válida, sin repetir su valor en tickets o mensajes amplios.
2. **Revocar o rotar de inmediato cada credencial confirmada, antes de tocar el historial de Git.** Es el único paso que cierra el riesgo independientemente de cuántas copias del repositorio existan. Priorizar la credencial de pagos, por el sistema al que declara dar acceso (`https://pagos.phantomcorp.example`), y el token de API, por ser de uso más genérico; la clave de staging, aun si su alcance es menor, se rota igual porque ya está confirmada como real dentro del caso.
3. **Investigar uso no autorizado antes de asumir que no pasó nada.** Revisar logs de autenticación y auditoría de los tres sistemas asociados en la ventana de exposición conocida. La investigación de R1–R3 solo demuestra que los secretos son recuperables desde esta copia local del repositorio; no demuestra ni descarta que alguien los haya usado.
4. **Comunicar el incidente a colaboradores, forks y clones conocidos.** Dado que el repositorio ya fue publicado y hay forks, cualquiera de ellos pudo haber obtenido una copia de los tres commits/ramas comprometidos antes de cualquier limpieza. Avisar permite que esos terceros también roten accesos que pudieran depender de las mismas credenciales y evita asumir que una limpieza posterior del repositorio "oficial" los alcanza.
5. **Sanear la historia recién después de rotar, de forma coordinada.** Reescribir con una herramienta como `git filter-repo` (ver `research.md`) exige que todos los colaboradores vuelvan a clonar, invalida los forks/PRs existentes contra los commits antiguos y requiere respaldo previo. Hacerlo antes de rotar da una falsa sensación de cierre: los objetos ya pudieron copiarse a cualquier clon o fork previo a la operación, y un force-push no los alcanza.
6. **Prevenir la recurrencia** con los controles pre-commit y server-side descriptos en la respuesta P5, para que un secreto nuevo no vuelva a ingresar al historial.

**Por qué reescribir la historia es la parte menos urgente:** un `force-push` o una limpieza con `filter-repo`/BFG actualiza las referencias del repositorio remoto propio, pero no revoca el secreto en el sistema que lo emitió ni elimina las copias que ya existen en clones y forks hechos antes de la operación —exactamente el mismo principio que R2 demostró a escala de un solo repositorio local: mover una referencia no destruye el objeto al que apuntaba—. Mientras la credencial original siga siendo válida, sigue siendo explotable sin importar que el historial "visible" ya no la muestre; rotarla es lo único que la invalida en origen, independientemente de cuántas copias del repositorio circulen.

**Vínculo con la evaluación de exposición (sección 3):** esa sección ya establece que la visibilidad de cada secreto depende de si su referencia llegó a publicarse y de cuántas copias existen, no solo de si está en `main`; este plan retoma ese criterio al tratar como comprometidos los tres secretos —incluido el de una rama nunca mergeada— y al no asumir alcance ni uso que la evidencia de R1–R3 no demuestra.

## 5. Preguntas P1–P5

P1: pendiente de su responsable.

### P5 — Mecanismos preventivos para evitar filtraciones en Git

Para prevenir la exposición de credenciales en un repositorio Git, proponemos implementar dos mecanismos complementarios, uno en la computadora del desarrollador antes de registrar los cambios y otro en la plataforma donde se aloja el repositorio.

**1. Control local antes del commit: hooks pre-commit con detección de secretos.**

Se puede configurar un hook `pre-commit` que ejecute una herramienta de detección de secretos, como Gitleaks, para analizar los archivos que el desarrollador está por incorporar al historial. Si identifica una contraseña, token o clave de API, puede impedir el commit y solicitar que se retire el secreto.

Este control permite detectar el problema antes de que la información quede registrada en el historial de Git. Es especialmente útil porque borrar posteriormente una credencial del código no elimina automáticamente las versiones anteriores que la contienen.

Su principal limitación es que los hooks locales pueden desactivarse o no estar instalados en todas las computadoras. Además, los detectores pueden producir falsos positivos o no identificar ciertos formatos de credenciales.

**2. Control del lado del servidor: escaneo de secretos y protección durante el push.**

Como segunda medida, se puede utilizar una funcionalidad como GitHub Push Protection, que examina los cambios que se intentan subir al repositorio y puede bloquear el push cuando detecta determinados secretos compatibles con sus patrones de identificación.

Esto incorpora una barrera adicional, incluso si un desarrollador no configuró correctamente los controles locales. La plataforma puede alertar sobre credenciales expuestas y permitir aplicar políticas de seguridad centralizadas.

Sin embargo, este mecanismo tampoco garantiza detectar todos los secretos: su cobertura depende de los tipos de credenciales reconocidos, la configuración disponible y las posibles excepciones autorizadas. Además, no reemplaza la revocación o rotación de las credenciales que ya fueron expuestas.

**Conclusión:** ambos controles deben utilizarse conjuntamente. El mecanismo local busca evitar que el secreto ingrese al historial, mientras que el control del servidor reduce el riesgo de que llegue al repositorio compartido. En caso de una filtración, la prioridad sigue siendo revocar o rotar la credencial afectada, porque eliminarla del código o reescribir el historial no garantiza que desaparezca de las copias existentes.

### P2 — Por qué `reset --hard` no necesariamente destruye objetos

`reset --hard` movió `main` de `bc9d0dbe6aca41d639a515395cc983e139979102` a `eafb81c3ec5790ce4741629458e11ab5c1a690b8`, y actualizó índice y árbol de trabajo. No borró inmediatamente el commit ni los objetos que forman su contenido: el commit apunta a un árbol, que a su vez referencia blobs. El reflog conservó el movimiento y el commit previo; `fsck` lo encontró como no alcanzable cuando se excluyeron los reflogs. `git show` permitió examinarlo sin recrear la rama ni alterar el repositorio. La salida recuperada contiene la flag `FLAG{git_reflog_rescata}` en `notas_investigacion.txt`.

La demostración consta de dos pasos: localizar el rastro en el reflog e inspeccionar el commit identificado, sin cambiar de rama ni mover referencias:

```bash
git reflog show --all --format="%H %gd %gs"
git show bc9d0dbe6aca41d639a515395cc983e139979102
```

Como corroboración independiente, `git fsck --no-reflogs --unreachable --no-progress` informó el commit como `unreachable`. El reflog y `fsck` son mecanismos de diagnóstico local, no prueba de que el objeto se haya publicado o distribuido a terceros. La retención del reflog y de objetos no alcanzables depende de la configuración y del momento de recolección de basura; no se debe afirmar que Git los conserva indefinidamente. Las salidas y el camino de descubrimiento están en `evidencia/salidas/r2-reflog.txt`, `r2-reflog-fechas.txt`, `r2-fsck.txt` y `r2-objeto-recuperado.txt`.

### P3 — Riesgo público frente a privado con 30 colaboradores

**Público:** si se publica la rama o sus objetos son accesibles, cualquier tercero con acceso a ellos puede leer el secreto mediante la interfaz, herramientas Git o escaneo automatizado. No hace falta integrar la rama en `main`. La cantidad potencial de copias no está limitada a colaboradores: pueden existir clones, forks y archivos descargados. Borrar la rama del servidor no invalida una credencial ya copiada.

**Privado con 30 colaboradores:** se restringe el acceso inicial a las cuentas y sistemas autorizados, pero la rama continúa siendo una vía de exposición. Quienes tengan lectura suficiente pueden recuperar su contenido; no implica que los treinta lo hayan hecho. Sus clones, respaldos, equipos, integraciones y trabajos CI pueden ampliar la distribución. Una cuenta comprometida, un equipo perdido, un permiso excesivo o una copia accidental pueden exponer la clave. Retirar el permiso del repositorio tampoco elimina las copias ni revoca la credencial de pagos.

La visibilidad privada reduce la audiencia inicial, pero el impacto depende de permisos, vigencia y alcance de la clave. En ambos escenarios corresponde tratar el secreto expuesto como comprometido a efectos de contención, revocarlo/rotarlo y revisar registros de uso antes de afirmar abuso. La investigación solo prueba accesibilidad en esta copia local; no prueba publicación, lectura de terceros ni operaciones de pago. Para establecerlas harían falta registros de la plataforma, de distribución y del proveedor.

### P4 — Plan de respuesta ante repositorio ya publicado con forks

El orden desarrollado en la sección 4 es: inventariar los tres secretos y su alcance → revocar/rotar cada credencial confirmada → investigar uso no autorizado en los sistemas asociados → comunicar a colaboradores, forks y clones conocidos → recién entonces sanear la historia de forma coordinada → prevenir la recurrencia.

Reescribir la historia queda en el último lugar porque, una vez que el repositorio fue publicado y existen forks, un force-push o una limpieza con `git filter-repo`/BFG solo cambia las referencias del repositorio remoto propio: no revoca el secreto en el sistema que lo emitió ni alcanza los objetos que un fork o un clon ya hechos conservan de manera independiente. El riesgo real —que la credencial siga siendo válida en otro lado— se cierra exclusivamente rotándola; la reescritura solo reduce la exposición de **nuevas** copias hacia adelante, no las que ya circulan.

## 6. Evidencia de progreso y preservación

- `evidencia/comandos.txt`: secuencia de P3 y P2, con contexto de terminal y ruta del caso.
- `evidencia/salidas/`: salidas de ramas, historial, comparación, reflog (incluidas las fechas registradas), fsck, commit recuperado, presentaciones de flags y estados.
- `evidencia/validar-r3-crlf.sh`: adaptación reproducible del verificador sin editar archivos oficiales.
- `evidencia/validar-r2-crlf.sh`: presentación de R2 reutilizando el verificador oficial con una copia temporal normalizada del manifiesto.
- `evidencia/salidas/status-extra2-final.txt`: captura anterior de P3, **1/3 con R3** marcado en esa ejecución. `status-extra2-p2.txt`: estado del checkout actual tras la presentación de P2, **1/3 con R2** marcado; no se modificó el aporte ni el estado de R3.
- Se generó el caso una sola vez con el comando oficial. Los avisos LF/CRLF de esa preparación corresponden al entorno Windows, no a una alteración maliciosa. Después se mantuvieron `HEAD`, referencias y árbol de trabajo del caso sin cambios.
- La rama externa ya era `labextra2-grupo06` y estaba limpia al inicio. No se cambió de rama, no se prepararon archivos para commit ni se hicieron commits, fetch, push o cambios remotos. El generador creó únicamente los commits ficticios internos del caso.

Fuentes locales: `CONTRIBUTING.md`, README raíz, `docs/INTRODUCCION.md`, README y plantilla/rúbrica de `labs/labextra2-git-forense/`, plan interno proporcionado por el usuario y evidencias adjuntas. El plan no se incorpora a la entrega. No se consultaron soluciones ni el contenido del generador para descubrir la flag.
