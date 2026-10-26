# Mini-research — Laboratorio 06

**Tema elegido:** B. Wordlists de enumeración

## Desarrollo

Las wordlists son listas de palabras, nombres de archivos o rutas que se utilizan en herramientas de enumeración para buscar recursos que no se encuentran visibles directamente desde una página web. Por ejemplo, una wordlist puede contener nombres como `admin`, `backup`, `config` o `login`, que luego se prueban contra un servidor para identificar si existen esos recursos.

Una de las colecciones más conocidas es **SecLists**, un proyecto de código abierto que reúne listas utilizadas en pruebas de seguridad. Incluye diccionarios de usuarios, contraseñas, directorios, archivos y otros elementos. Para la enumeración web, ofrece listas específicas que pueden utilizarse con herramientas como Gobuster.

La elección de la wordlist es importante porque determina qué rutas se van a probar. Si utilizamos una lista demasiado pequeña o que no contiene nombres relacionados con la aplicación, podemos pasar por alto recursos existentes. En cambio, una lista muy extensa puede generar una gran cantidad de peticiones innecesarias y aumentar el tiempo de ejecución.

Por eso, antes de realizar una enumeración, conviene analizar qué tipo de aplicación estamos evaluando, qué tecnologías utiliza y qué recursos podrían existir. También es importante interpretar correctamente las respuestas HTTP. Por ejemplo, un código `200` indica que se obtuvo una respuesta exitosa, mientras que un `403` puede indicar que el recurso existe, pero su acceso está prohibido.

En nuestro Laboratorio 06 utilizamos `dirb` para enumerar directorios del servidor PhantomCorp. Como resultado, encontramos la ruta `/admin`, que devolvió `403`, y `/backup`, que respondió `200`. Posteriormente se confirmó que `/backup` mostraba nombres de archivos de respaldo y configuración.

Este ejemplo demuestra que la enumeración permite descubrir información que no necesariamente aparece enlazada desde la página principal. También muestra por qué una wordlist no garantiza encontrar todos los recursos: los resultados dependen de las palabras incluidas y de cómo responde el servidor.

En definitiva, la herramienta utilizada es importante, pero también lo son la selección de la wordlist, el análisis de las respuestas y la interpretación de los hallazgos. La enumeración debe realizarse únicamente sobre sistemas autorizados y sus resultados tienen que documentarse con evidencia.

## Fuentes

1. **SecLists — Repositorio oficial de GitHub.** Colección de wordlists utilizadas en evaluaciones de seguridad, incluyendo enumeración de recursos web.
   https://github.com/danielmiessler/SecLists

2. **OWASP — Web Security Testing Guide.** Sección sobre archivos antiguos, respaldos y recursos no referenciados que pueden exponer información sensible.
   https://owasp.github.io/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management/04-Review_Old_Backup_and_Unreferenced_Files_for_Sensitive_Information

3. **PortSwigger — Content Discovery.** Documentación sobre descubrimiento de contenido mediante búsqueda de nombres, navegación y patrones de rutas.
   https://portswigger.net/burp/documentation/desktop/tools/engagement-tools/content-discovery

## Reflexión

Esta investigación nos permitió comprender que enumerar no consiste solamente en ejecutar una herramienta y observar los resultados. Aprendimos que elegir correctamente una wordlist influye directamente en los recursos que podemos descubrir. También relacionamos estos conceptos con el laboratorio, donde encontramos directorios que no estaban visibles desde la página principal. Consideramos importante complementar las herramientas automáticas con verificaciones manuales para interpretar correctamente cada hallazgo.