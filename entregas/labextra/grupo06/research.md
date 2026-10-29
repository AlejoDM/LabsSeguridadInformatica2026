# Research — Laboratorio Extra SSRF

**Grupo:** 06
**Fecha:** 2026-10-29
**Opción elegida:** A — Caso real (Capital One, 2019)

**Declaración de uso de IA:** (pendiente de completar por el grupo antes de entregar — ver indicación aparte)

## 1. El caso: Capital One (2019)

### 1.1 Qué funcionalidad era vulnerable

Capital One tenía su infraestructura alojada en AWS, con un **Web Application Firewall (WAF)** basado en ModSecurity desplegado delante de su aplicación web. Según la reconstrucción técnica más citada del incidente (Krebs on Security, con el análisis original de Evan Johnson, de Cloudflare), ese WAF estaba mal configurado: podía ser inducido a realizar peticiones HTTP hacia destinos elegidos por quien lo consultaba, en lugar de restringirse exclusivamente a inspeccionar tráfico hacia la aplicación protegida. Esa es la misma clase de funcionalidad que el grupo explotó en `/preview` durante R1 y R3: un componente del lado servidor que **acepta un destino y lo consulta por cuenta del usuario**.

### 1.2 Qué pidió el atacante a través del servidor

La acusada, Paige A. Thompson, aprovechó esa mala configuración del WAF para que el propio firewall —que corría sobre una instancia EC2 de AWS— realizara una petición hacia el **servicio de metadatos de instancia** de AWS (`169.254.169.254`). Ese servicio, cuando no está protegido con las medidas que se describen más abajo, responde sin autenticación adicional a cualquier proceso que corra en la instancia, y en este caso le entregó al WAF comprometido las **credenciales temporales de IAM** asociadas al rol que tenía asignado la instancia. El WAF, entonces, terminó pidiéndole al servicio de metadatos algo que el atacante no podía solicitar directamente desde fuera: el mismo patrón "el servidor lo pide por vos" que el grupo documentó en R1 (panel en `127.0.0.1:9000`) y R3 (`phantomcorp-intra`).

### 1.3 Qué obtuvo y cuál fue el impacto

El rol IAM asignado a esa instancia tenía permisos excesivos para su función: entre otros, podía listar y leer el contenido de buckets de Amazon S3. Con las credenciales temporales obtenidas vía el servicio de metadatos, Thompson pudo acceder y copiar información de aproximadamente **100 millones de personas en Estados Unidos y 6 millones en Canadá** —datos de solicitudes de crédito, puntajes, ingresos, y en una porción de los casos números de Seguro Social y de cuenta bancaria—, según consta en el caso judicial seguido ante el Tribunal de Distrito de EE. UU. para el Distrito Oeste de Washington (*United States v. Paige Thompson*). El incidente se descubrió el 17 de julio de 2019, cuando una usuaria de GitHub reportó públicamente evidencia vinculada a la intrusión; Capital One notificó al FBI dos días después.

El paralelo con el laboratorio es directo en magnitud de mecanismo, no de escala: así como `/preview` devolvió el backup de clientes de la intranet (R3) porque el servidor —no el atacante— tenía conectividad hacia `phantomcorp-intra`, el WAF de Capital One devolvió credenciales reales porque él —no la atacante— corría dentro de la red de AWS y tenía acceso al servicio de metadatos de su propia instancia.

### 1.4 Qué mitigación lo habría impedido

Las medidas que, de haber estado vigentes, habrían cortado la cadena son las mismas familias de control que el grupo propuso para `/preview` en la pregunta P4 de este informe:

- **Privilegio mínimo en el rol IAM del WAF:** si la instancia del WAF no hubiera tenido permiso para listar ni leer el contenido de los buckets, las credenciales filtradas habrían sido inútiles para exfiltrar esos datos.
- **Restricción de egreso hacia el servicio de metadatos** desde el componente expuesto a tráfico de terceros (el WAF), de forma análoga a impedir que `/preview` alcance la intranet.
- **IMDSv2:** la versión 2 del servicio de metadatos de AWS exige una sesión autenticada mediante un token obtenido primero con una petición `PUT`, con un número de saltos de red limitado (`hop limit`), en lugar de responder a cualquier `GET` simple. Esto no elimina el SSRF, pero dificulta sensiblemente que una petición SSRF "básica" (una sola solicitud GET reenviada, como la que usó el grupo en R1/R3) alcance a completar el intercambio de dos pasos que exige IMDSv2, según documenta la guía oficial de Amazon EC2 sobre la transición a esta versión.

## 2. Pregunta de cierre — SSRF vs. inyección de comandos

**Similitud:** en ambos casos, el atacante no ejecuta la acción directamente; se la delega a un componente del lado servidor que tiene una posición de red, una identidad o unos privilegios que el atacante no posee. "El servidor pide por vos" (SSRF) y "el servidor ejecuta por vos" (inyección de comandos, Lab 07) son variantes del mismo problema de fondo: una entrada no confiable termina controlando una acción que el servidor realiza con **su propia** autoridad.

**Diferencia:** la inyección de comandos le da al atacante ejecución arbitraria en el sistema operativo del servidor —puede leer, escribir, instalar persistencia, pivotear a otros procesos o, según privilegios, comprometer el host completo—. El SSRF, en cambio, limita al atacante a lo que el servidor puede *pedir por HTTP (u otro protocolo soportado)*: su alcance depende por completo de qué destinos son alcanzables desde la red del servidor y qué devuelven esos destinos. Por eso, en el laboratorio, el grupo demostró lectura de dos recursos internos (R1 y R3) pero no ejecución de código ni control del host.

**Cuál es más peligrosa, en un contexto definido:** tomada en abstracto, la inyección de comandos es estrictamente más poderosa, porque la ejecución arbitraria subsume cualquier otra capacidad, incluida la de hacer peticiones de red. Sin embargo, el caso Capital One muestra que, **en un contexto cloud con servicios de metadatos e IAM**, un SSRF puede alcanzar un impacto equivalente o mayor al de muchas inyecciones de comandos acotadas: convierte una simple petición HTTP en el robo de credenciales con los mismos privilegios que tenía el servidor, sin necesidad de ejecutar una sola línea de código en el host. El criterio correcto no es "cuál es peor en general", sino qué privilegios e información son alcanzables desde el componente comprometido en ese entorno particular; en una nube mal configurada, esa superficie puede volver al SSRF tan o más dañino que una inyección de comandos limitada.

## 3. Fuentes

1. U.S. Attorney's Office, Western District of Washington — Departamento de Justicia de EE. UU. *United States v. Paige Thompson* (resumen del caso y enlaces a los comunicados de cargos e indictment). https://www.justice.gov/usao-wdwa/united-states-v-paige-thompson
2. Krebs, Brian. *What We Can Learn from the Capital One Hack*, KrebsOnSecurity (agosto de 2019). https://krebsonsecurity.com/2019/08/what-we-can-learn-from-the-capital-one-hack/
3. TechTarget. *Capital One hack highlights SSRF concerns for AWS* (2019). https://www.techtarget.com/searchsecurity/news/252467901/Capital-One-hack-highlights-SSRF-concerns-for-AWS
4. Amazon Web Services. *Transition to using Instance Metadata Service Version 2 (IMDSv2)* — AWS EC2 User Guide. https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-metadata-transition-to-version-2.html
