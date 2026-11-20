# Revisión cruzada — Change 007

**Revisora:** María Belén Benito (P4)
**Fecha:** 2026-11-20
**Resultado:** Pide cambios

## Verificaciones

- 49 tests aprobados en tests/test_reporting_e2e.py.
- Revisión de design.md, report_builder.py,
  defectdojo_export.py y reporting.py.
- Se revisaron los controles de bitácora,
  aprobación de entrega y bloqueo DEMO.

## Observación

En harness/report_builder.py, build_report() comprueba
datos sensibles en los campos originales del hallazgo
y en scope, pero no comprueba el campo reason
obtenido de validation.result.

El motivo podría incorporarse al informe Markdown
y a la exportación a DefectDojo sin pasar por el filtro.

## Corrección solicitada

1. Validar reason antes de generar el informe.
2. Agregar un test con un token ficticio en reason.
3. Comprobar que se rechaza el informe.
4. Ejecutar nuevamente los tests de reporting.

La observación surge de la revisión estática.
No se detect? una filtración real.

**Estado:** pendiente de corrección y nueva revisión.
