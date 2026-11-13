# Retrospectiva de IA — P2

En esta retrospectiva se registran los errores de IA detectados durante el
trabajo y los defectos adicionales encontrados al revisar el harness. Los
commits se conservaron en la historia local de la rama; todavía no se hizo push.
Para los casos 4–6 también se conservó el par separado de test rojo y corrección.

## 1. El test A1 fallaba por el fixture, no por la normalización

- **Error:** el test utilizaba el token de ejemplo (`lab.example.test`) pero probaba
  `dvwa.lab.test`; por eso seguía en rojo incluso con la normalización correcta.
- **Detección:** al ejecutar A1 después de implementar la normalización, el test
  todavía fallaba.
- **Corrección:** se emitió el token con `domains=("dvwa.lab.test",)`.
- **Aprendizaje:** se debe comprobar que el target del test esté dentro del token antes
  de atribuir un fallo al código bajo prueba.
- **Referencia histórica:** `1b9392e`.

## 2. Literal IPv6 inválido en el caso A3

- **Error:** se utilizó `fd00:lab::/64`; `lab` no es un grupo hexadecimal IPv6.
- **Detección:** `ipaddress.ip_network` rechazó el literal antes de probar el
  comportamiento del Guard.
- **Corrección:** se reemplazó el literal por `fd00:abcd::/64` y `fd00:beef::5`.
- **Aprendizaje:** los datos de prueba deben validarse con el parser estándar antes de
  interpretar el resultado como un defecto del control.
- **Referencia histórica:** `1b9392e`.

## 3. Test de exclusión sin exclusión en el RoE

- **Error:** el test esperaba que el token aplicara una exclusión que no se había
  incluido en su fixture.
- **Detección:** el token conservó correctamente `10.99.0.0/24` completo y el
  test no produjo la condición esperada.
- **Corrección:** se agregó `10.99.0.10/32` a `exclusions.cidrs`.
- **Aprendizaje:** se debe revisar el conjunto de condiciones del escenario (RoE,
  alcance y exclusiones), no solo la aserción.
- **Referencia histórica:** `1b9392e`.

## 4. El token seguía vivo en el instante exacto de expiración

- **Error:** la comparación de vigencia incluía `window_end`; un token todavía
  se consideraba válido en el límite de expiración.
- **Detección:** un test fijó el reloj exactamente en `window_end` y `is_live()`
  devolvió verdadero.
- **Corrección:** se cambió a un intervalo semiabierto `[window_start, window_end)`
  y se verificó que `Harness.invoke` bloquee y registre `BLOCKED` en ese límite.
- **Aprendizaje:** se incorporaron pruebas para los límites exactos de tiempo, además
  de instantes anteriores y posteriores.
- **Test rojo:** `9a76691`. **Corrección:** `937a234`.

## 5. El hash no cubría todas las restricciones y se escapaba un alcance vacío

- **Error:** `approval_hash` se calculaba sin exclusiones ni fases. Además, la validación
  del alcance revisaba CIDR y dominios por separado, no el caso donde ambos
  grupos quedaban vacíos a la vez.
- **Detección:** tests nuevos cambiaron una exclusión o fase sin cambiar el hash y
  combinaron exclusiones que anulaban CIDR y dominios sin obtener rechazo.
- **Corrección:** se incluyeron todas las restricciones del RoE en el hash y se
  agregó el rechazo cuando el conjunto combinado de destinos restantes quedó vacío.
- **Aprendizaje:** el hash debe cubrir todo dato que altere la autorización y la
  validación debe evaluar el resultado combinado, no ramas independientes.
- **Test rojo:** `9a76691`. **Corrección:** `937a234`.

## 6. Se podían emitir tokens sin registrar la emisión

- **Error:** `audit` era opcional en `tokens.issue()`, de modo que una llamada
  normal podía devolver un token y no dejar registro.
- **Detección:** un test llamó al emisor sin sink y confirmó que se recibía
  un token sin auditoría.
- **Corrección:** `audit` se hizo obligatorio; sin sink, el emisor no
  entrega un token. Se actualizó la nota de traspaso para que los consumidores
  conozcan el contrato.
- **Aprendizaje:** las propiedades de la spec deben quedar forzadas por la
  interfaz, en vez de depender de que cada consumidor recuerde un parámetro opcional.
- **Test rojo:** `9a76691`. **Corrección:** `937a234`.
