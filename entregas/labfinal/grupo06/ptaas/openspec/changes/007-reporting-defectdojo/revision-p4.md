# Revisi?n cruzada ? Change 007

**Revisora:** Mar?a Bel?n Benito (P4)
**Fecha:** 2026-11-20
**Resultado:** Pide cambios

## Verificaciones

- 49 tests aprobados en tests/test_reporting_e2e.py.
- Revisi?n de design.md, report_builder.py,
  defectdojo_export.py y reporting.py.
- Se revisaron los controles de bit?cora,
  aprobaci?n de entrega y bloqueo DEMO.

## Observaci?n

En harness/report_builder.py, build_report() comprueba
datos sensibles en los campos originales del hallazgo
y en scope, pero no comprueba el campo reason
obtenido de validation.result.

El motivo podr?a incorporarse al informe Markdown
y a la exportaci?n a DefectDojo sin pasar por el filtro.

## Correcci?n solicitada

1. Validar reason antes de generar el informe.
2. Agregar un test con un token ficticio en reason.
3. Comprobar que se rechaza el informe.
4. Ejecutar nuevamente los tests de reporting.

La observaci?n surge de la revisi?n est?tica.
No se detect? una filtraci?n real.

**Estado:** pendiente de correcci?n y nueva revisi?n.
