# Mini-research — Lab 01

**Grupo:** 06
**Tema elegido:** Tema 3 — La disponibilidad, la propiedad descuidada de la tríada
**Título:** La disponibilidad como propiedad crítica de la seguridad: economía del ransomware, métricas de continuidad y límites reales de recuperación
**Cantidad de palabras:** 906 (sin bibliografía ni declaraciones)

---

## Planteo

Al estudiar la tríada de seguridad (confidencialidad, integridad y disponibilidad), salta a la vista que la confidencialidad siempre recibió la mayor parte de la atención, del presupuesto y del contenido académico [4]. Esta preferencia histórica viene de la época militar en la que se crearon los primeros modelos formales (como Bell-LaPadula), pensados para evitar la fuga de secretos de Estado mediante jerarquías de acceso. En ese marco, se asumía que la integridad y la disponibilidad eran consecuencias de tener hardware confiable o temas a resolver por el equipo de infraestructura.

En las organizaciones actuales la realidad es otra: quedarse sin sistemas suele provocar un daño económico y operativo más inmediato y severo que una filtración de datos. Considerar la disponibilidad como un simple asunto de mantenimiento de servidores deja desprotegidas las funciones críticas ante ataques dirigidos que buscan paralizar las operaciones para extorsionar a la empresa.

---

## Desarrollo

### Separación entre seguridad e infraestructura

La idea de que la disponibilidad no es un tema central de seguridad causó una división en los equipos tecnológicos. Tradicionalmente, ciberseguridad se enfocó en el cifrado, permisos y prevención de intrusiones, mientras que la disponibilidad se delegó a administradores de sistemas y redes [4]. Esto llevó a gestionar la disponibilidad solo con acuerdos de nivel de servicio (SLA) pensados para fallas comunes de hardware o caídas de conectividad, ignorando qué ocurre ante ataques intencionales.

En los modelos iniciales dominó el principio de "necesidad de saber" (need-to-know), descuidando la necesidad de operar en forma continua. Así, durante décadas la disponibilidad fue la propiedad menos comprendida de la tríada, confundiéndose la redundancia clásica de servidores con la capacidad real de resistir un ataque coordinado.

### La economía del ransomware y el costo de la inactividad

El crecimiento del cibercrimen organizado cambió el escenario mediante el ransomware. Cuando un atacante roba datos confidenciales, monetizarlos es complejo: debe buscar compradores en mercados clandestinos, pagar intermediarios y afrontar precios inestables. En cambio, al bloquear el acceso a sistemas productivos, el atacante cobra directamente por el tiempo que la víctima pasa sin operar [3].

Los grupos delictivos fijan sus rescates analizando cuánto cuesta cada hora de inactividad. Si una empresa detiene sus líneas de producción o cobranzas, las pérdidas por facturación caída, penalizaciones contractuales y daño reputacional superan rápido la cifra exigida. Diversos estudios económicos y reportes de incidentes [5] señalan que los costos totales de recuperación suelen triplicar el rescate pedido. Esto convierte a la disponibilidad secuestrada en el modelo de ataque más rentable de la actualidad.

| Aspecto | Filtración de confidencialidad | Ataque de ransomware (Disponibilidad) |
|---|---|---|
| **Acción del atacante** | Exfiltración no autorizada de datos | Cifrado masivo y parálisis operativa |
| **Tiempo de impacto** | Costos diferidos (juicios, multas) | Inmediato (corte total de ingresos) |
| **Origen del costo principal** | Cantidad y tipo de registros filtrados | Horas de inactividad y lucro cesante |
| **Métricas clave** | Tiempo de detección y contención | RTO (tiempo límite) y RPO (pérdida máxima) |

### Métricas de continuidad: BIA, RTO y RPO

Para responder a estos riesgos se aplican metodologías formales de continuidad. El estándar NIST SP 800-34 Rev. 1 [2] define el Análisis de Impacto en el Negocio (BIA), un proceso para identificar funciones críticas y establecer dos métricas clave:

1. **RTO (Recovery Time Objective):** Tiempo máximo admisible con los sistemas caídos antes de que la interrupción cause un daño irreparable.
2. **RPO (Recovery Point Objective):** Pérdida máxima tolerable de datos en el tiempo, lo que define la frecuencia requerida de las copias de seguridad.

Como indican las guías de CISA y el FBI [1], para cumplir estos objetivos hoy no basta con backups convencionales. Es necesario implementar copias inmutables que no puedan borrarse desde la red (como almacenamiento WORM o copias fuera de línea), restringir privilegios y probar periódicamente la restauración integral bajo condiciones de estrés.

---

## Tensión / límites

Al aplicar estos marcos surgen discrepancias entre la teoría documental y las restricciones técnicas reales:

1. **Límite físico de la red frente al RTO:** Fijar en un plan que un sistema se recuperará en 4 horas es irreal si hay que restaurar decenas de terabytes desde la nube con un enlace de comunicaciones estándar. La velocidad de transferencia y la latencia imponen días de descarga, invalidando el RTO acordado con la dirección.
2. **La trampa de la replicación sincrónica:** Replicar bases de datos en tiempo real entre dos centros de datos para lograr un RPO cercano a cero tiene un riesgo grave: si un ransomware cifra la base primaria, el cambio se replica al instante a la sede secundaria, destruyendo la disponibilidad de ambos sitios a la vez.
3. **Sabotaje de backups y doble extorsión:** Los atacantes modernos obtienen persistencia previa para localizar y destruir las copias de seguridad antes de cifrar los datos [1]. Además, con la doble extorsión (roban datos antes de cifrarlos), aunque la organización restaure sus sistemas desde backups sanos, persiste la extorsión sobre la confidencialidad.

---

## Cierre

La disponibilidad debe integrarse desde el inicio en el diseño de arquitecturas seguras. No es una tarea periférica de soporte, sino un requisito de subsistencia que demanda copias inmutables, segmentación defensiva y planes de contingencia probados en la práctica. Diseñar plataformas que resguarden la privacidad pero queden inutilizadas ante un ataque frustra el fin principal de la tecnología: asegurar que la organización y las personas sigan funcionando sin interrupciones.

---

## Bibliografía

1. [PRIMARIA] Cybersecurity and Infrastructure Security Agency, & Federal Bureau of Investigation. (2023). *#StopRansomware Guide*. CISA. https://www.cisa.gov/sites/default/files/2023-05/StopRansomware_Guide_508c%20(1).pdf
2. [PRIMARIA] National Institute of Standards and Technology. (2010). *Contingency Planning Guide for Federal Information Systems* (NIST Special Publication 800-34, Rev. 1). U.S. Department of Commerce. https://doi.org/10.6028/NIST.SP.800-34r1
3. [ARBITRADA] Cartwright, A., Cartwright, E., & Webb, J. (2020). An economic analysis of ransomware and its welfare consequences. *Royal Society Open Science*, 7(3), 190023. https://doi.org/10.1098/rsos.190023
4. [ARBITRADA] Samonas, S., & Coss, D. (2014). The CIA strikes back: Redefining confidentiality, integrity and availability in security. *Journal of Information System Security*, 10(3), 21-45. https://www.researchgate.net/publication/317011931_The_CIA_strikes_back_Redefining_confidentiality_integrity_and_availability_in_security
5. [SECUNDARIA] IBM Security. (2024). *Cost of a Data Breach Report 2024*. IBM. https://www.ibm.com/reports/data-breach

---

## Declaración de uso de asistentes de IA

**¿Se usaron asistentes de IA en este trabajo?** Sí

| Herramienta | Para qué | Qué partes afectó | Cómo se verificó |
|---|---|---|---|
| Gemini 3.7 Flash / Gemini Deep Research | Búsqueda inicial de fuentes y asistencia en la organización del texto | Planteo, Desarrollo, Tensión/límites y Cierre | Se revisaron y leyeron de forma directa los documentos citados (guías NIST y CISA, y los artículos de Samonas y Cartwright) para corroborar cada dato y afirmación. |

**Verificación de fuentes:** el grupo declara haber accedido y verificado individualmente cada una de las referencias citadas.
