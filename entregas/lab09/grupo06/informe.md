# Informe — Laboratorio 09 · Agentes de pentest

**Grupo:** 06
**Fecha:** 2026-10-23
**Proveedor usado:** mock

| Nombre y apellido | Usuario de GitHub |
|---|---|
| Martín Beccereca | martinbeccereca |
| Belén Benito | belubenito01 |
| Alejo José De Miguel | AlejoDM |
| Tomás Giudici | TomasGiudici |
| Carolina Suppo | carosuppo |

## 0. Declaración de uso de IA

**Herramienta:** Claude Code.

- **Finalidad del uso:** apoyo para correr el agente de referencia en modo `mock` contra `phantomcorp`, armar la estructura inicial de la entrega y redactar la fila de R1 en la tabla de flags, la auditoría de los pasos 1-2 del transcript y la respuesta a P1.
- **Partes asistidas:** estructura de `entregas/lab09/grupo06/`, fila "R1 — Recon inicial" en la tabla de flags, filas de los pasos 1-2 en la tabla de auditoría, y respuesta P1.
- **Verificación:** el agente de referencia (`agente_pentest.py`) se ejecutó sin modificar, con `LLM_PROVIDER=mock` y sin ninguna API key, dentro del contenedor `cyberlab-attacker`; el transcript completo se guardó sin editar en `evidencia/salidas/referencia-mock.txt`. No se tocó `herramientas.py` ni el guardrail de alcance. Se revisó el contenido antes de incorporarlo.

**Herramienta:** Codex (OpenAI).

- **Finalidad del uso:** apoyo para revisar la evidencia de R2, redactar la respuesta P2 y elaborar el mini-research sobre prompt injection indirecta.
- **Partes asistidas:** fila R2 de flags, pasos 3–4 de la auditoría, respuesta P2, `research.md` y la bitácora de comandos.
- **Verificación:** se contrastó cada afirmación de R2 con el transcript crudo. Las fuentes del research se abrieron y leyeron antes de citarlas. El equipo debe revisar el texto y conservar esta declaración si representa el uso real de herramientas de IA.


**Herramienta:** Codex (OpenAI), aporte P3.

- **Finalidad y partes asistidas:** documentación de R3 y del paso 5, síntesis de aciertos y errores P1–P3, ayuda en redacción de respuesta P3 y revisión cruzada de P1.
- **Verificación:** contraste con el transcript crudo existente y con `llm.py`, `herramientas.py` y el esqueleto públicos, sin leer el target ni soluciones. Se intentó presentar exclusivamente R3 al verificador oficial local y se guardó su rechazo sin alterarlo. No se probaron APIs externas ni se realizaron commits o acciones en GitHub.

## 1. Flags capturadas

*(salida de `./ctf status 09`, pendiente de completar cuando se resuelvan los 5 retos)*

| Reto | Estado | Evidencia |
|---|---|---|
| R1 — Recon inicial | Obtenida | [Transcript de referencia](evidencia/salidas/referencia-mock.txt) (pasos 1-2) y [envío de R1](evidencia/salidas/r1-submit.txt) |
| R2 — Pista en `robots.txt` | Observada; registro pendiente | [Transcript de referencia](evidencia/salidas/referencia-mock.txt) (pasos 3-4) y [resultado del verificador](evidencia/salidas/r2-submit-rechazado.txt). El target devolvió `FLAG{agente_ruta_oculta}`, pero el verificador oficial la rechazó; no se afirma que R2 haya quedado registrada. |
| R3 — API de debug expuesta | Obtenida | [Transcript del agente](evidencia/salidas/referencia-mock.txt), paso 5: `HTTP 200` y `FLAG{agente_api_expuesta}`. La flag fue aceptada mediante `./ctf submit 09 R3`. Ver [estado confirmado](evidencia/salidas/r3-status-confirmado.txt). |

## 2. Tu agente

*Pendiente del responsable de R5: adjuntar `src/agente_esqueleto.py` completado y su salida trayendo el flag R5.*

## 3. Auditoría crítica del agente

**Transcript:** *(pegar la corrida completa o remitir a `evidencia/salidas/referencia-mock.txt`)*

**Aciertos y errores:** *(decisión por decisión)*

| Paso | Acción solicitada | Resultado observado | Evaluación humana |
|---|---|---|---|
| 1 | `nmap_scan({'host': 'phantomcorp'})` | `error nmap: Command [...] timed out after 60 seconds` (ver `evidencia/salidas/referencia-mock.txt`, paso 1) | Insuficiente, pero razonable como primer intento: `nmap -sV` es una decisión de recon estándar y coherente con lo practicado en el Lab 05. El error es del entorno (timeout), no una decisión incorrecta del agente. Un operador humano habría reintentado con un escaneo más acotado (por ejemplo, menos puertos o sin `-sV`) en vez de abandonar la vía por completo; el agente, en cambio, pasó directamente a otra tool. |
| 2 | `http_get({'url': 'http://phantomcorp/'})` | `HTTP 200` con header `X-Recon-Flag: FLAG{agente_primer_recon}` y cuerpo "PhantomCorp Capstone. Auditame." (ver paso 2) | Adecuada: ante el fallo de `nmap_scan`, el agente cambió de tool en vez de insistir con la misma acción fallida, y la petición HTTP directa a la raíz del sitio es la alternativa obvia de recon cuando se sabe (de los labs anteriores) que el objetivo expone un servicio web. Encontró la flag en el primer intento con esa tool, sin pasos redundantes. |
| 3 | `http_get({'url': 'http://phantomcorp/robots.txt'})` | `HTTP 200` con `Disallow: /vault-interno-x7` (ver paso 3 del transcript). | Adecuada: `robots.txt` es una fuente de enumeración de bajo impacto y su directiva entregó una pista concreta. El archivo no impone control de acceso; solo comunica una preferencia a rastreadores. En un servicio real, la ruta puede no existir o estar protegida, por lo que aún era necesario confirmarla. |
| 4 | `http_get({'url': 'http://phantomcorp/vault-interno-x7'})` | `HTTP 200` y `Ruta interna. FLAG{agente_ruta_oculta}` (ver paso 4). | Adecuada y eficiente: el agente convirtió la pista observada en una única consulta de confirmación, sin ampliar el alcance ni adivinar rutas adicionales. El resultado demuestra acceso al recurso en este entorno, no que toda ruta listada en un `robots.txt` sea sensible o accesible en otros sistemas. |
| 5 | `http_get({'url': 'http://phantomcorp/api/debug'})` | `HTTP 200`, `Content-Type: application/json` y `{"debug": true, "flag": "FLAG{agente_api_expuesta}"}` (paso 5 del transcript crudo). | Adecuada para confirmar exposición: una sola consulta obtiene una respuesta de debug con una flag, sin repetir peticiones ni salir de `phantomcorp`. No demuestra descubrimiento adaptativo: `ClienteMock.PLAN` ya contiene `/api/debug` y los resultados anteriores no muestran una pista hacia esa API. Un humano debe distinguir esta comprobación de una enumeración que hubiera descubierto la ruta. |

### Síntesis de aciertos y errores P1–P3

- **Observaciones:** los pasos 1–5 contienen un timeout de nmap y cuatro GET exitosos. `robots.txt` expone una ruta que el paso 4 confirma; el paso 5 confirma una API de debug accesible en esta corrida. No hay peticiones repetidas entre esos cinco pasos. Se conservan intactos los hechos y el transcript aportados por P1 y P2.
- **Eficiencia y límites:** consultar la ruta publicada y comprobar debug con un GET por recurso es económico. El timeout consumió 60 segundos sin aportar servicios identificados. Su causa no está demostrada: podría requerir diagnóstico del entorno o del escaneo. La tool actual fija las opciones de nmap; cambiar puertos u opciones exigiría otro mecanismo autorizado, que no se implementó en este aporte.
- **Inferencia acotada:** que un GET suceda después de un timeout, o que una ruta coincida con una pista anterior, no demuestra que el motor haya reaccionado a esas observaciones. `ClienteMock.paso` ignora `resultados` y recorre `PLAN`; por ello tampoco prueba que el agente hubiera seguido una ruta distinta si cambiara la respuesta del target.
- **R3:** La respuesta HTTP 200 y el JSON obtenido en el paso 5 demuestran que la API de depuración estaba accesible y devolvió `FLAG{agente_api_expuesta}`. Aunque los primeros intentos de registrar la flag fueron rechazados por el verificador local, posteriormente `./ctf submit 09 R3` la aceptó correctamente. El archivo `evidencia/salidas/r3-status-confirmado.txt` confirma que R3 quedó registrado como resuelto. Esto no demuestra exposición de otros datos, privilegios adicionales ni razonamiento autónomo de un LLM real, ya que utilizamos el proveedor `mock`.

**Límite de esta auditoría:** la integración cubre los pasos 1–5 (R1–R3). R4 y R5 quedan a sus responsables. La corrida existente usa mock determinista; no se ensayaron proveedores externos.

### Revisión cruzada de P1 por P3

Revisión documental de los pasos 1–2 y P1, sin reescribir el aporte original:

| Afirmación revisada | Estado | Evidencia y corrección propuesta |
|---|---|---|
| Paso 1 con timeout y paso 2 con HTTP 200 y flag en header | Respaldada | Coincide con `evidencia/salidas/referencia-mock.txt`. |
| El error de nmap es del entorno | Parcial | El timeout está observado, pero su causa no. Presentarlo como causa por diagnosticar. |
| El agente cambió de tool por el fallo anterior y cada decisión depende de la observación | Requiere corrección | En `llm.py`, `ClienteMock.paso` ignora los resultados y avanza por `PLAN`. El loop entrega observaciones, pero este mock no las usa para decidir. P1 debería distinguir arquitectura del loop y comportamiento del motor ensayado. |
| Reintentar con menos puertos o sin detección de versión | Parcial | Es una alternativa humana posible, pero `nmap_scan(host)` no permite seleccionar esas opciones. No atribuir esa capacidad al agente actual. |
| Hay finalización y límite de pasos | Respaldada con límite | El transcript termina y el esqueleto declara `MAX_PASOS = 12`; la implementación y prueba del agente propio corresponden a P5. |

Las correcciones quedan señaladas para P1; su respuesta y sus filas originales se mantienen sin cambios.
**El guardrail (R4):** *(qué pasó y por qué importa; qué otros agregarían)*

## 4. Preguntas de análisis
**P1 — el loop de tool-use.**

El loop de tool-use tiene cuatro piezas que se repiten hasta una condición de corte: (1) el LLM (o, en modo `mock`, el motor determinista que lo reemplaza) decide una acción a partir del objetivo y de lo que ya observó; (2) el programa ejecuta únicamente una herramienta de la allowlist, nunca una acción arbitraria elegida libremente por el modelo; (3) el resultado de esa herramienta se devuelve al modelo como nueva observación; y (4) el ciclo vuelve al paso 1 hasta que el modelo decide finalizar o se alcanza un límite de pasos (`MAX_PASOS`).

En la corrida de referencia (`evidencia/salidas/referencia-mock.txt`) esto se ve en los pasos 1 y 2: en el paso 1 el agente decide `nmap_scan({'host': 'phantomcorp'})`, el programa ejecuta esa tool (no otra), el `nmap` falla por timeout y esa falla —no un éxito— es el resultado que se realimenta. En el paso 2, con esa observación disponible, el agente decide una acción distinta, `http_get` a la raíz del sitio, que sí devuelve la flag de R1. Eso es el loop funcionando: cada decisión se toma en función del resultado anterior, no de una secuencia fija escrita de antemano por una persona.

La condición de fin es la otra mitad del diseño: el loop tiene que poder terminar tanto porque el agente decide una acción "final" (como ocurre al cierre del transcript, con el mensaje "Fin: Auditoría simulada completa") como porque se agota `MAX_PASOS`, para que un modelo que nunca decide finalizar no deje el proceso corriendo indefinidamente. El motor `mock` usado en esta corrida no tiene razonamiento real —sus decisiones están prefijadas—, pero respeta exactamente esta misma estructura de loop, que es la pieza que sí se evalúa en R5 con el esqueleto propio del grupo.
**P2 — LLM vs. script fijo.**

Un LLM puede interpretar una observación nueva y elegir la siguiente acción sin que todas las bifurcaciones estén programadas de antemano. En el recorrido esperado, tras recibir de `robots.txt` la ruta `/vault-interno-x7`, puede decidir que esa ruta es una pista pertinente y consultar solo ese recurso. Esa adaptación es útil cuando el target devuelve rutas, parámetros, tecnologías o errores que no se conocían al escribir el programa. Con un proveedor real, además, la decisión puede variar según el contexto recibido; el modo `mock` del laboratorio imita la interfaz y el ciclo, pero usa un plan fijo y por ello no demuestra razonamiento generativo.

Un script fijo como `recolector.py` del Lab 08 hace mejor una tarea estrecha, conocida y repetitiva: recorre un rango definido, aplica la misma regla a cada respuesta, ofrece resultados predecibles y es más fácil de probar, auditar y acotar en costo. No interpreta una pista nueva por sí mismo; habría que programar explícitamente que lea `robots.txt`, extraiga una directiva y consulte la ruta. Por eso la elección no es entre “LLM bueno” y “script obsoleto”: el LLM aporta adaptación bajo controles, mientras que el script aporta determinismo cuando el flujo ya está definido.

En ambos casos, la salida del modelo o el contenido recibido del target no debe convertirse directamente en una acción. En este lab, `ejecutar_tool` y la validación de alcance son la barrera que evita que una decisión —razonable, errónea o manipulada— alcance otro host.
**P3 — ventaja del diseño agnóstico.**

La ventaja concreta es poder usar el mismo loop con un mock local sin credenciales o con Claude/OpenAI cambiando `LLM_PROVIDER`, sin reescribir el despacho de herramientas ni el control de alcance. Esto permite desarrollar y verificar el flujo sin costo de API y luego sustituir el motor. No implica que los proveedores produzcan decisiones idénticas ni que el mock valide su razonamiento.

El agente se acopla al contrato común de `llm.py`: crea el cliente con `crear_cliente(SYSTEM, TOOLS)` y llama a `cliente.paso(resultados)`. Recibe una acción normalizada de tool (`tipo`, `nombre`, `argumentos`, `id`) o de fin (`tipo`, `texto`); devuelve los resultados como una lista de diccionarios con `id` y `output`. No necesita conocer los formatos particulares de mensajes HTTP de cada proveedor.

Los adaptadores `ClienteClaude` y `ClienteOpenAI` traducen el registro `TOOLS` al esquema de su API y las respuestas al contrato común; `crear_cliente` selecciona la implementación. Por ejemplo, el resultado interno con `id` y `output` se representa como `tool_result` con `tool_use_id` en Claude y como mensaje `tool` con `tool_call_id` en OpenAI. Esa traducción queda fuera del loop. Un proveedor nuevo requeriría implementar el contrato y agregarlo a la fábrica, conservando `ejecutar_tool` y la validación de alcance.

**Límite comprobado en el código:** los adaptadores actuales exponen una sola acción por llamada y no resuelven de forma general respuestas con múltiples llamadas simultáneas. El desacoplamiento es el que ofrece esta interfaz concreta, no compatibilidad universal con cualquier comportamiento de API. Solo se verificó localmente el código y la evidencia mock existente; no se probaron servicios externos.

**P4 — dos riesgos y su guardrail.**
**P5 — por qué los labs 05–08 eran requisito.**
