# Red team del guard — A1 a A10

Alcance: solo el laboratorio del kit y las estructuras deterministas del
harness. No se ejecutó ninguna prueba contra un sistema real ni fuera de
`lab/`. Cada intento es un test en `tests/test_redteam_guard.py`.

- Commit con los tests en rojo: `98e85f4` (`red team · A1-A10: tests adversariales en rojo`).
- Commit con las correcciones: `1b9392e` (`003 · 2.2-2.5: parser de RoE, emisor de tokens y controles A1-A10 del guard`).
- Ese segundo commit también corrige dos errores de fixture del primer intento
  (dominio del token en A1 y literal IPv6 inválido en A3); se detectaron al
  correr los tests, no ajustando el test para que pasara el código.

| # | Intento | ¿Bypass real? | Test | Corrección |
|---|---|---|---|---|
| A1 | Hostname con mayúsculas, punto final o espacios | **Sí**: `"  dvwa.lab.test  "` no se normalizaba y quedaba bloqueado/ambiguo | `test_a1_hostname_se_normaliza_antes_de_decidir` | `Guard._normalize` hace `strip().lower().rstrip(".")`; también en `validate_target` |
| A2 | Sufijo engañoso (`evil-lab.example.test`) | No: ya estaba cubierto | `test_a2_sufijo_enganoso_se_bloquea` (4 casos) | Sin cambio de código; se extendió el test |
| A3 | IPv6 e IPv4 mapeadas a IPv6 | **Sí**: `::ffff:10.0.0.5` se comparaba como IPv6 y no contra `10.0.0.0/24` | `test_a3_*` | `_as_ip` usa `ipv4_mapped`; IPv6 se compara contra su propio CIDR |
| A4 | Hostname autorizado que resuelve fuera de alcance | **Sí, por ausencia de control**: no se resolvía el nombre | `test_a4_*` (3 casos) | `Guard(resolver=...)` revalida **todas** las direcciones antes de actuar; falla cerrado si no hay respuesta |
| A5 | Redirección HTTP a otro host | **Brecha preventiva**: no había adaptador HTTP ni política de redirección | `test_a5_*` | `RedirectPolicy` rechaza otro host, credenciales embebidas y esquemas distintos; el adaptador HTTP del change 004 debe usarla |
| A6 | Token reutilizado en otra fase o engagement | **Sí, en engagement**: la fase ya se comparaba, pero no había ligadura al engagement | `test_a6_*` (2 casos) | `Guard(engagement_id=...)` bloquea tokens de otro engagement y registra `BLOCKED` |
| A7 | Ventana con zonas horarias distintas | **Control nuevo**: no existía parser de RoE | `test_a7_*` (2 casos) | El parser convierte todo a epoch UTC; una ventana que parece válida en local pero se invierte en UTC se rechaza |
| A8 | CIDR demasiado amplio (`/8`, `0.0.0.0/0`) | **Control nuevo**: no existía parser que lo rechazara | `test_a8_cidr_amplio_o_publico_se_rechaza` (5 casos) | `roe._red` exige prefijo mínimo /24 (v4) o /64 (v6) y subred de `targets.lab_only_cidrs` |
| A9 | Argumentos inyectados por target o `parameters` | **Parcial**: el target ya se validaba; `parameters` no tenía validador | `test_a9_*` (11 casos) | `validate_parameters` rechaza flags, espacios y metacaracteres antes de construir argv |
| A10 | Escritura concurrente en la bitácora | **Sí bajo interleaving**: sin lock, dos hilos pueden tomar el mismo `prev` | `test_a10_escritura_concurrente_conserva_la_cadena` | `AuditLog.record_decision` serializa lectura de `prev` + append con un lock |

## Evidencia de los bypass

- A1, A3, A4, A6, A9 y A10: la salida del commit en rojo y las mutaciones
  M1, M4, M5, M7 y M8 de `entrega/mutaciones.md` muestran el fallo y la
  restauración en verde.
- A4 y A5 no se pueden probar contra el laboratorio todavía porque el adaptador
  HTTP es del change 004. Se probaron con resolver y política inyectados, que es
  el punto de control que el adaptador deberá usar.
- A10 se probó con 10 hilos × 25 registros. El test de estrés no siempre falla
  por scheduling; la mutación M8 (sin lock + pausa de 1 ms) reproduce la
  bifurcación de forma determinista.

## Lo que no se hizo

- No se atacó ningún host fuera del laboratorio.
- No se generaron exploits ni se amplió el catálogo de PoCs.
- No se aprobó ningún gate HITL.
- La decisión de si cada bypass es "real" y si la corrección alcanza queda
  pendiente de revisión humana (P2 + otro integrante), según la sección 9 del
  plan.
