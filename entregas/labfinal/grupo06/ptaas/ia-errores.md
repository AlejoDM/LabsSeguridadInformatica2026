# Registro de errores de la IA

| Fecha | Persona | Herramienta/modelo | Qué hizo mal la IA | Cómo se detectó | Qué se cambió | Commit |
|---|---|---|---|---|---|---|
| 2026-11-11 | P2 | opencode / DeepSeek V4.1 Flash | Escribió el test A1 con el token por defecto (`lab.example.test`) pero el target era `dvwa.lab.test`; el test fallaba por fixture, no por el control | Al correr `test_a1_*` después de implementar la normalización, seguía en rojo | Se corrigió el fixture para emitir el token con `domains=("dvwa.lab.test",)` | 1b9392e |
| 2026-11-11 | P2 | opencode / DeepSeek V4.1 Flash | Usó `fd00:lab::/64` como IPv6 de prueba; `lab` no es un grupo hexadecimal válido | `ipaddress.ip_network` falló al correr el test | Se reemplazó el literal por `fd00:abcd::/64` y `fd00:beef::5` | 1b9392e |
| 2026-11-11 | P2 | opencode / DeepSeek V4.1 Flash | El primer test de exclusión usaba el RoE por defecto sin exclusión y esperaba que el token la aplicara | El test falló con `allowed_cidrs` igual al /24 completo | Se corrigió el fixture para incluir `exclusions.cidrs=["10.99.0.10/32"]` | 1b9392e |
| 2026-11-13 | P2 | opencode / GPT-6 Luna | Dejó `ScopeToken.is_live()` inclusivo en `window_end`, por lo que el token era válido en el instante exacto de expiración | Test de borde nuevo: fijar el reloj a `window_end` mantenía `is_live()` en verdadero | Se cambió a un intervalo semiabierto y se verificó que `Harness.invoke` registre `BLOCKED` | 9a76691 (test rojo) → 937a234 (corrección) |
| 2026-11-13 | P2 | opencode / GPT-6 Luna | Calculó `approval_hash` sin incluir exclusiones/fases y no detectaba el caso donde exclusiones separadas vaciaban CIDR y dominios a la vez | Tests nuevos de hash y de exclusiones combinadas fallaron antes de la corrección | Se incluyeron todas las restricciones del RoE en el hash y se validó conjuntamente el alcance restante | 9a76691 (test rojo) → 937a234 (corrección) |
| 2026-11-13 | P2 | opencode / GPT-6 Luna | Dejó opcional el sink de auditoría en `tokens.issue()`, permitiendo devolver tokens sin registrar la emisión | Un test de contrato mostró que `issue(roe, phase)` devolvía un token sin auditoría | Se hizo obligatorio `audit` y se actualizaron los usos y el handoff | 9a76691 (test rojo) → 937a234 (corrección) |

Los commits de tests en rojo y correcciones se conservaron en esta rama local;
todavía no se hizo push.
