# Registro de errores de la IA

| Fecha | Persona | Herramienta/modelo | Qué hizo mal la IA | Cómo se detectó | Qué se cambió | Commit |
|---|---|---|---|---|---|---|
| 2026-11-11 | P2 | opencode / DeepSeek V4.1 Flash | Escribió el test A1 con el token por defecto (`lab.example.test`) pero el target era `dvwa.lab.test`; el test fallaba por fixture, no por el control | Al correr `test_a1_*` después de implementar la normalización, seguía en rojo | Se emitió el token con `domains=("dvwa.lab.test",)` en el test | 1b9392e |
| 2026-11-11 | P2 | opencode / DeepSeek V4.1 Flash | Usó `fd00:lab::/64` como IPv6 de prueba; `lab` no es un grupo hexadecimal válido | `ipaddress.ip_network` falló al correr el test | Se reemplazó por `fd00:abcd::/64` y `fd00:beef::5` | 1b9392e |
| 2026-11-11 | P2 | opencode / DeepSeek V4.1 Flash | El primer test de exclusión usaba el RoE por defecto sin exclusión y esperaba que el token la aplicara | El test falló con `allowed_cidrs` igual al /24 completo | Se construyó el RoE con `exclusions.cidrs=["10.99.0.10/32"]` | 1b9392e |
