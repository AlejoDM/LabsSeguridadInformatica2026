# Informe — Laboratorio 04 · Marcos normativos y gestión

**Grupo:** 06 · **Integrantes:** 

| Nombre y apellido | Usuario de GitHub |
|---|---|
| Martín Beccereca | martinbeccereca |
| Belén Benito | belubenito01 |
| Alejo José De Miguel | AlejoDM |
| Tomás Giudici | TomasGiudici |
| Carolina Suppo | carosuppo |


## 0. Declaración de uso de IA

**Herramienta: Claude Code**
- **Finalidad del uso:** Apoyo en la redacción del informe. 
- **Partes generadas o asistidas:** Sección 1 — A.1 y A.2.
- **Verificación:** Las fuentes citadas fueron visitadas y verificadas antes de citarla.

## 1. Parte A — Marco aplicado

### A.1 — Marco elegido y por qué

Elegimos el **NIST Cybersecurity Framework (CSF)**, en su versión vigente
**CSF 2.0** (publicada en febrero de 2024). Dos razones concretas para este
escenario:

1. **Es de acceso libre y gratuito.** ISO/IEC 27001 es un estándar que hay
   que comprar para leer el texto completo del Anexo A; el NIST CSF se
   publica y actualiza en `nist.gov/cyberframework` sin costo, lo que importa
   para una PyME como PhantomCorp que recién está armando su gestión de
   seguridad y no tiene presupuesto para certificarse.
2. **Su estructura por funciones es más rápida de aplicar a un diagnóstico
   inicial que un sistema de gestión completo.** ISO 27001 exige construir
   un SGSI (Sistema de Gestión de Seguridad de la Información) con
   políticas, alcance y auditoría formal, lo que representa un proceso de gestión, no un diagnóstico puntual. El NIST CSF, en cambio, organiza los resultados de
   ciberseguridad en funciones de alto nivel pensadas para razonar rápido
   sobre "qué le falta a esta organización", que es exactamente lo que pide
   este ejercicio.

CSF 2.0 define **seis** funciones: **Gobernar (Govern)**, **Identificar
(Identify)**, **Proteger (Protect)**, **Detectar (Detect)**, **Responder
(Respond)** y **Recuperar (Recover)**.

La función **Govern** es la incorporación nueva de la versión 2.0 respecto de la 1.1, y organiza la
estrategia y las políticas de seguridad que orientan a las otras cinco.
Para el mapeo de A.2 usamos las cinco funciones operativas que menciona el
propio enunciado (Identify/Protect/Detect/Respond/Recover); lo señalamos
porque **Govern** también aplicaría acá, ya que la ausencia de una política de
contraseñas formal es, en rigor, tanto un problema de *Protect* como de
*Govern*. Sin embargo, mantuvimos el mapeo uno a uno para no forzar una sexta
debilidad que el enunciado no pide.

### A.2 — Mapeo de cinco debilidades a funciones del NIST CSF

| # | Debilidad del escenario | Función NIST CSF | Por qué esta función |
|---|---|---|---|
| 1 | No hay inventario ni clasificación formal de los datos sensibles que maneja (nombres, DNI, números de tarjeta) | **Identify** | *Identify* es la función que cubre entender los activos, los datos y el contexto de riesgo de la organización. Sin saber con precisión qué dato crítico se tiene y dónde vive, no se puede priorizar ninguna otra medida, ya que es la base de la que dependen las demás cuatro. |
| 2 | No tiene MFA ni política de contraseñas para el acceso remoto de empleados | **Protect** | *Protect* cubre las salvaguardas que reducen la probabilidad de que un evento de ciberseguridad ocurra, y el control de acceso e identidad es el ejemplo canónico de esta función. |
| 3 | El servidor web público y los accesos remotos no muestran evidencia de monitoreo o registro de actividad | **Detect** | *Detect* es identificar eventos de ciberseguridad cuando ocurren. Sin logging ni monitoreo sobre los dos puntos de entrada más expuestos (el servidor público y el acceso remoto), un atacante podría estar adentro sin que nadie se entere. |
| 4 | No tiene un plan de respuesta a incidentes | **Respond** | *Respond* cubre las acciones a tomar durante y después de un incidente detectado. Sin un plan, aun si *Detect* funcionara, la organización improvisaría en el peor momento posible. |
| 5 | Los backups están en un único disco físico en la oficina, sin redundancia ni copia externa | **Recover** | *Recover* cubre restaurar capacidades y servicios después de un incidente. Un backup en un solo disco en el mismo edificio es un punto único de fallo: un incendio, un robo o un ransomware que cifre también ese disco deja a PhantomCorp sin forma de recuperarse. |

Fuente: National Institute of Standards and Technology. (2024). *The NIST
Cybersecurity Framework (CSF) 2.0* (NIST CSWP 29).
https://doi.org/10.6028/NIST.CSWP.29, documento oficial disponible también en
https://www.nist.gov/cyberframework.

---

### A.3 — Respuesta al riesgo
## 2. Parte B — Riesgo cuantitativo (ranking por ALE; ROI del control #1; un riesgo a aceptar/transferir)
## 3. Anexo — tu riesgos.json

```json
[
  {
    "nombre": "Compromiso de credenciales de empleados por falta de MFA y política de contraseñas débiles en acceso remoto",
    "sle": 30000.0,
    "aro": 1.2
  },
  {
    "nombre": "Exfiltración masiva de datos sensibles de clientes (nombres, DNI, tarjetas) vía vulnerabilidad en servidor web público",
    "sle": 80000.0,
    "aro": 0.35
  },
  {
    "nombre": "Intrusión persistente y movimiento lateral no detectado por ausencia de logging y monitoreo centralizado",
    "sle": 45000.0,
    "aro": 0.5
  },
  {
    "nombre": "Pérdida irrecuperable de datos por Ransomware o siniestro físico debido a backup único en disco local sin copia externa",
    "sle": 100000.0,
    "aro": 0.15
  },
  {
    "nombre": "Interrupción operativa prolongada e improvisación ante incidentes por falta de un plan formal de respuesta",
    "sle": 15000.0,
    "aro": 0.6
  }
]
```
