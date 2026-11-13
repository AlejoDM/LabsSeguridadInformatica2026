# Retrospectiva de IA — P2

Estos casos salen de `ia-errores.md` y de la revisión posterior del harness.
Los commits originales de P2 vuelven a estar en la historia de la rama local;
no se hizo push. Los casos 4–6 se corrigieron después con un nuevo par de
commits de prueba roja y corrección.

## 1. El test A1 fallaba por el fixture, no por la normalización

- **Error:** el test usaba el token de ejemplo (`lab.example.test`) pero probaba
  `dvwa.lab.test`; por eso seguía en rojo incluso con la normalización correcta.
- **Detección:** al ejecutar A1 después de implementar la normalización, el test
  todavía fallaba.
- **Corrección:** emitir el token con `domains=("dvwa.lab.test",)`.
- **Aprendizaje:** comprobar que el target del test está dentro del token antes
  de atribuir un fallo al código bajo prueba.
- **Referencia histórica:** `1b9392e`.

## 2. Literal IPv6 inválido en el caso A3

- **Error:** se escribió `fd00:lab::/64`; `lab` no es un grupo hexadecimal IPv6.
- **Detección:** `ipaddress.ip_network` rechazó el literal antes de probar el
  comportamiento del Guard.
- **Corrección:** usar `fd00:abcd::/64` y `fd00:beef::5`.
- **Aprendizaje:** validar datos de prueba con el parser estándar antes de
  interpretar el resultado como un defecto del control.
- **Referencia histórica:** `1b9392e`.

## 3. Test de exclusión sin exclusión en el RoE

- **Error:** el test esperaba que el token aplicara una exclusión que no había
  incluido en su fixture.
- **Detección:** el token conservó correctamente `10.99.0.0/24` completo y el
  test no produjo la condición esperada.
- **Corrección:** incluir `10.99.0.10/32` en `exclusions.cidrs`.
- **Aprendizaje:** revisar el arreglo de condiciones del escenario (RoE,
  alcance y exclusiones), no solo la aserción.
- **Referencia histórica:** `1b9392e`.

## 4. El token seguía vivo en el instante exacto de expiración

- **Error:** la comparación de vigencia incluía `window_end`; un token todavía
  se consideraba válido en el límite de expiración.
- **Detección:** un test fijó el reloj exactamente en `window_end` y observó que
  `is_live()` devolvía verdadero.
- **Corrección:** usar un intervalo semiabierto `[window_start, window_end)` y
  comprobar que `Harness.invoke` bloquea y registra `BLOCKED` en ese límite.
- **Aprendizaje:** probar límites exactos de tiempo, además de instantes antes y
  después.
- **Test rojo:** `9a76691`. **Corrección:** `937a234`.

## 5. El hash no cubría todas las restricciones y se escapaba un alcance vacío

- **Error:** `approval_hash` omitía exclusiones y fases. Además, la validación
  del alcance revisaba CIDR y dominios por separado, no el caso donde ambos
  grupos quedaban vacíos a la vez.
- **Detección:** tests nuevos cambiaron una exclusión/fase sin cambiar el hash y
  combinaron exclusiones que anulaban CIDR y dominios sin obtener rechazo.
- **Corrección:** incluir las restricciones completas del RoE en el hash y
  rechazar cuando el conjunto combinado de destinos restantes está vacío.
- **Aprendizaje:** el hash debe cubrir todo dato que altere autorización y la
  validación debe evaluar el resultado combinado, no ramas independientes.
- **Test rojo:** `9a76691`. **Corrección:** `937a234`.

## 6. Se podían emitir tokens sin registrar la emisión

- **Error:** `audit` era opcional en `tokens.issue()`, de modo que una llamada
  normal podía devolver un token y no dejar registro.
- **Detección:** el test nuevo llamó al emisor sin sink y confirmó que recibía
  un token sin auditoría.
- **Corrección:** `audit` ahora es argumento obligatorio; sin sink, el emisor no
  entrega un token. Se actualizó la nota de traspaso para que los consumidores
  conozcan el contrato.
- **Aprendizaje:** una propiedad descrita en una spec debe estar forzada por la
  interfaz, no depender de que cada consumidor recuerde un parámetro opcional.
- **Test rojo:** `9a76691`. **Corrección:** `937a234`.
