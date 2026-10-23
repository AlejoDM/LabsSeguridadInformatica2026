# Mini-research — Laboratorio 08

**Tema elegido:** C. Gestión de secretos: riesgos de archivos `.env` legibles y alternativas de gestión segura.

## Desarrollo

Los secretos de una aplicación —contraseñas de base de datos, claves de API, certificados y tokens— requieren un ciclo de vida: creación, entrega, uso, auditoría, rotación, revocación y expiración. Un archivo `.env` puede separar la configuración del código, pero no protege automáticamente sus valores. Si el archivo queda incluido en una imagen, un backup, un volumen o una ruta legible por un usuario de servicio, cualquier proceso con ese acceso puede leer credenciales en texto claro.

El riesgo observado en R2 no es que el formato `.env` sea intrínsecamente inseguro. El problema es de control de acceso y de gestión: `operador`, un usuario limitado, pudo leer valores destinados a la aplicación. Además, las credenciales estáticas elevan el impacto de una filtración, porque permanecen útiles hasta que alguien las detecta, revoca y rota.

OWASP recomienda centralizar y estandarizar el almacenamiento, aprovisionamiento, auditoría y rotación de secretos, con controles de acceso acordes al principio de mínimo privilegio. Un gestor de secretos permite entregar a cada workload únicamente el valor y el período de uso necesarios, registrar quién o qué identidad lo solicitó y revocar rápidamente el acceso ante un incidente. En entornos donde la plataforma lo permita, es preferible usar identidad de workload y credenciales dinámicas o de corta vida antes que una contraseña estática compartida.

El enfoque Twelve-Factor distingue configuración de código y propone valores de despliegue en variables de entorno. Esto evita que una credencial termine hardcodeada o versionada por accidente, pero no elimina la necesidad de proteger el entorno de ejecución, los logs y las herramientas de diagnóstico. Por ello, una implementación madura combina inyección controlada en runtime, permisos restrictivos, secretos de corta duración, rotación automatizada y monitoreo de accesos. Para claves criptográficas, NIST subraya que la protección y el ciclo de vida del material de claves forman parte de la gestión de seguridad, no de un detalle opcional de configuración.

Aplicado a PhantomCorp, la respuesta inmediata es revocar y rotar las credenciales expuestas, reducir permisos de lectura sobre la configuración y revisar los accesos que ya pudieron usarla. Como corrección estructural, la aplicación debería recuperar el secreto desde un servicio de gestión autorizado para su identidad, no conservar una contraseña reutilizable en un archivo legible por cuentas locales.

## Fuentes

1. OWASP Foundation. *Secrets Management Cheat Sheet*, secciones “Introduction”, “Access Control” y “Secret Lifecycle”. https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
2. Wiggins, Adam. *The Twelve-Factor App*, “III. Config”. https://12factor.net/config
3. NIST. *SP 800-57 Part 1 Rev. 5: Recommendation for Key Management — Part 1: General* (mayo de 2020). https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final

## Reflexión

R2 mostró que separar secretos del código no alcanza si el archivo que los contiene es legible por una cuenta local limitada. La evidencia también obliga a pensar en el tiempo: una contraseña estática filtrada continúa siendo un problema hasta su revocación. Para el equipo, la mejora relevante es combinar mínimo privilegio, secretos de corta vida y registro de accesos, no solo mover el mismo valor a otro archivo.

