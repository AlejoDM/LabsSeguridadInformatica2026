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

## 1. Línea de tiempo de la filtración

Aporte de P3 para integrar en la cronología del grupo. Fechas de autor y committer coinciden, con zona -03:00. No son fechas de publicación ni de descubrimiento: el caso se generó e investigó el 28/10/2026.

| Fecha registrada | Autor | Commit | Evento | Exposición / fuente |
|---|---|---|---|---|
| 2026-08-05 16:30 -03:00 | dev-jperez | 0abdf953b75b214af59d0cf31e55ccbf2c9873d8 | `wip: pasarela de pagos (falta todo)` agrega `.env.pasarela` y `pasarela.py` | Secreto de pagos en la rama; `r3-diff-introduccion.txt`. Fecha incoherente con su padre. |
| 2026-08-10 09:12 -03:00 | dev-jperez | de33a75843139302dfbe034cab11e8175881540e | Inicio de deploy-tool | Contexto legítimo según historial; `r3-historial.txt`. |
| 2026-08-10 18:47 -03:00 | dev-jperez | 9333f2b4a09f7a320cb66d621c3bd53b4f694941 | Configuración temporal del hotfix; padre del commit de pagos | R1 debe corroborar contenido y exposición del token; `r3-parentesco.txt`. |
| 2026-08-11 10:05 -03:00 | dev-jperez | eafb81c3ec5790ce4741629458e11ab5c1a690b8 | Mensaje de limpieza de credenciales | R1 debe documentar su diff; `r3-fechas.txt`. |
| 2026-08-20 11:00 -03:00 | dev-jperez | fa714bda2ac9d31bf92774e901400be4a296c1e5 | Actualización documental, punta de `main` | Contexto; el secreto de pagos sigue en otra rama. |

**Inconsistencia temporal:** `git show -s --format=raw feature/pasarela-pagos` muestra que el padre de `0abdf95` es `9333f2b`, aunque la fecha del hijo es anterior. El orden topológico es inicial → hotfix → pagos, independientemente de esas fechas. No se corrige el caso ni se inventa una duración de exposición. La tabla ordena fechas declaradas, no demuestra el orden real de publicación. P1/P2 deben incorporar sus evidencias, incluido el objeto no alcanzable, para completar la cronología general.

## 2. Hallazgos

### R1 — Secreto en commit viejo
Pendiente del aporte de P1; no resuelto en esta contribución.

### R2 — Commit «perdido»
Pendiente del aporte de P2; no resuelto en esta contribución.

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

Pendiente del responsable P4. **Revisión cruzada de P3:** todavía no existe su aporte ni `research.md`, por lo que no es posible aprobar su coherencia. Al integrarlo, comprobar que inventaría el token API (R1), el secreto del objeto recuperado (R2, tipo por confirmar con su evidencia) y la clave de pagos (R3); que prioriza revocación/rotación antes de limpiar historia; que contempla ramas, forks y clones; y que distingue exposición potencial de uso probado. Esta lista no sustituye la respuesta de P4 ni afirma una revisión realizada.

## 5. Preguntas P1–P5

P1 y P2: pendientes de sus responsables.

### P3 — Riesgo público frente a privado con 30 colaboradores

**Público:** si se publica la rama o sus objetos son accesibles, cualquier tercero con acceso a ellos puede leer el secreto mediante la interfaz, herramientas Git o escaneo automatizado. No hace falta integrar la rama en `main`. La cantidad potencial de copias no está limitada a colaboradores: pueden existir clones, forks y archivos descargados. Borrar la rama del servidor no invalida una credencial ya copiada.

**Privado con 30 colaboradores:** se restringe el acceso inicial a las cuentas y sistemas autorizados, pero la rama continúa siendo una vía de exposición. Quienes tengan lectura suficiente pueden recuperar su contenido; no implica que los treinta lo hayan hecho. Sus clones, respaldos, equipos, integraciones y trabajos CI pueden ampliar la distribución. Una cuenta comprometida, un equipo perdido, un permiso excesivo o una copia accidental pueden exponer la clave. Retirar el permiso del repositorio tampoco elimina las copias ni revoca la credencial de pagos.

La visibilidad privada reduce la audiencia inicial, pero el impacto depende de permisos, vigencia y alcance de la clave. En ambos escenarios corresponde tratar el secreto expuesto como comprometido a efectos de contención, revocarlo/rotarlo y revisar registros de uso antes de afirmar abuso. La investigación solo prueba accesibilidad en esta copia local; no prueba publicación, lectura de terceros ni operaciones de pago. Para establecerlas harían falta registros de la plataforma, de distribución y del proveedor.

P4 y P5: pendientes de sus responsables.

## 6. Evidencia de progreso y preservación

- `evidencia/comandos.txt`: secuencia de investigación y comprobaciones, incluidos intentos fallidos de acceso por propiedad del directorio.
- `evidencia/salidas/`: ramas, historial, contenido, comparación, parentesco, fechas y verificación.
- `evidencia/validar-r3-crlf.sh`: adaptación reproducible del verificador sin editar archivos oficiales.
- `evidencia/salidas/status-extra2-final.txt`: estado oficial **1/3**. R1 y R2 pendientes, coherente con el alcance P3.
- Se generó el caso una sola vez con el comando oficial. Los avisos LF/CRLF de esa preparación corresponden al entorno Windows, no a una alteración maliciosa. Después se mantuvieron `HEAD`, referencias y árbol de trabajo del caso sin cambios.
- La rama externa ya era `labextra2-grupo06` y estaba limpia al inicio. No se cambió de rama, no se prepararon archivos para commit ni se hicieron commits, fetch, push o cambios remotos. El generador creó únicamente los commits ficticios internos del caso.

Fuentes locales: `CONTRIBUTING.md`, README raíz, `docs/INTRODUCCION.md`, README y plantilla/rúbrica de `labs/labextra2-git-forense/`, plan interno proporcionado por el usuario y evidencias adjuntas. El plan no se incorpora a la entrega. No se consultaron soluciones ni el contenido del generador para descubrir la flag.
