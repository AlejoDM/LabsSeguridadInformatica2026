# Mini-research — Laboratorio 05

> Copiala a `entregas/lab05/grupoXX/research.md`. Elegí **un** tema y hacé una
> investigación breve pero real (media a una carilla). Fuentes verificables.

**Grupo:** 06
**Tema elegido:** *(marcá uno)*

- [ ] **A.** El CVE-2015-3306 de ProFTPD 1.3.5: qué es el `mod_copy`, cómo se
  explota el comando `SITE CPFR/CPTO`, y por qué un banner de versión alcanza
  para saber que un servidor es vulnerable.
- [ ] **B.** Tipos de escaneo de `nmap` (`-sS` vs `-sT` vs `-sU` vs `-sV`):
  cómo funciona cada uno a nivel de paquetes TCP/IP y qué huella deja en el
  objetivo.
- [x] **C.** OSINT y recon pasivo: qué información de una organización se puede
  reunir **sin tocar** sus sistemas (certificados, DNS, buscadores, filtraciones)
  y por qué es tan valiosa para un atacante.
- [ ] **D.** El estándar CVSS: cómo se arma un score (vector base), qué
  significan sus métricas, y por qué "criticidad" no es lo mismo que "score".

---

## Desarrollo

### OSINT y reconocimiento pasivo

OSINT (*Open Source Intelligence*) es una técnica que consiste en recopilar y analizar información disponible públicamente. En seguridad informática se utiliza durante la etapa de reconocimiento para conocer mejor a una organización antes de realizar pruebas sobre sus sistemas.

El reconocimiento pasivo permite obtener información sin interactuar directamente con los servidores del objetivo. Para esto se consultan fuentes externas, como registros de dominios, bases de datos públicas, buscadores y registros históricos.

Algunas de las fuentes más utilizadas son:

- **WHOIS y RDAP:** permiten consultar información sobre el registro de un dominio, como la empresa registradora, fechas de creación y vencimiento y servidores de nombres. Algunos datos del titular pueden estar protegidos por privacidad.
- **DNS:** permite obtener información sobre dominios, direcciones IP y servidores de correo. Los registros A, MX, NS y TXT pueden ayudar a identificar parte de la infraestructura y los servicios que utiliza una organización.
- **Certificados digitales:** mediante registros públicos de Certificate Transparency se pueden descubrir dominios y subdominios para los que se emitieron certificados.
- **Buscadores y sitios públicos:** pueden revelar documentos, direcciones de correo, tecnologías utilizadas o información que una empresa publicó sin considerar su importancia.
- **Filtraciones de información:** las bases públicas que registran incidentes anteriores pueden indicar que determinadas cuentas o credenciales estuvieron expuestas. Esta información debe consultarse de manera legal y responsable.

El reconocimiento pasivo resulta valioso porque permite reunir datos sin generar tráfico directo hacia los sistemas investigados. Sin embargo, las consultas realizadas a terceros pueden quedar registradas por esos servicios.

Para un atacante, esta información permite conocer mejor la organización y detectar posibles objetivos. Por ejemplo, identificar servidores de correo o tecnologías utilizadas podría facilitar la preparación de ataques posteriores.

Desde el punto de vista defensivo, OSINT también es útil porque permite descubrir qué información de nuestra organización está expuesta públicamente y tomar medidas para reducir los riesgos.

En el Laboratorio 05 trabajamos con PhantomCorp, donde se utilizaron herramientas como `nmap` y `curl` para identificar servicios y obtener información directamente de sus servidores. Esto corresponde al reconocimiento activo, a diferencia de las consultas de información pública que realizamos mediante `whois` y `dig` sobre un dominio de prueba.

## Fuentes

1. MITRE ATT&CK — Reconocimiento de información DNS: https://attack.mitre.org/techniques/T1590/002/
2. ICANN — Registration Data Access Protocol (RDAP): https://www.icann.org/rdap/
3. Google — Certificate Transparency: https://developers.google.com/public-key-infrastructure/faq/what-is-certificate-transparency
4. Cloudflare — Tipos de registros DNS: https://developers.cloudflare.com/dns/manage-dns-records/reference/dns-record-types/

## Reflexión

Esta investigación me permitió entender que no siempre es necesario acceder directamente a un sistema para obtener información importante sobre una organización. Muchas veces, los datos públicos permiten conocer parte de su infraestructura y detectar posibles riesgos. Al relacionarlo con el laboratorio, entendí mejor la diferencia entre reconocimiento pasivo y activo y la importancia de controlar qué información dejamos expuesta.
