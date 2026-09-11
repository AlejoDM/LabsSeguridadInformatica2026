# Mini-research — Laboratorio 02

**Tema elegido:** C — Derivación de claves desde contraseñas (PBKDF2, bcrypt,
scrypt, Argon2): por qué un `sha256(password)` no alcanza.

## Desarrollo

Un hash criptográfico como SHA-256 es determinístico y muy rápido: en
hardware moderno (GPU, o directamente ASICs dedicados) se pueden calcular
miles de millones de hashes SHA-256 por segundo. Esa velocidad es una
virtud cuando el objetivo es verificar la integridad de un archivo (Lab 01),
pero es exactamente lo que **no** se quiere cuando el objetivo es proteger
una contraseña: si un atacante obtiene una base de `sha256(password)`
filtrada, puede probar diccionarios completos de contraseñas comunes en
minutos. El caso Adobe de la Parte A de este mismo informe es un recordatorio
de lo que pasa cuando ni siquiera se hashea, sino que se cifra de forma
reversible, pero el error de fondo que trata este mini-research es el
siguiente escalón: **incluso hasheando correctamente**, usar una función
rápida como SHA-256 sigue siendo un error, porque no le cuesta nada al
atacante repetir el cálculo miles de millones de veces.

La respuesta de la criptografía aplicada fue diseñar funciones de derivación
de claves (KDF) **deliberadamente costosas**, con tres generaciones
principales:

- **bcrypt (1999).** Propuesto por Niels Provos y David Mazières en
  *"A Future-Adaptable Password Scheme"* (USENIX Annual Technical
  Conference, 1999), se basa en un cifrado Blowfish con un programa de
  claves (*key schedule*) deliberadamente costoso. Su "factor de trabajo"
  duplica el costo de cómputo por cada incremento, lo que en teoría permite
  adaptarse a hardware futuro más rápido. Su límite conocido: solo usa los
  primeros 72 bytes de la contraseña de entrada, y no tiene un parámetro de
  memoria configurable, es decir, es costoso en tiempo de CPU, pero no en memoria.
- **scrypt (2009).** Colin Percival, en *"Stronger Key Derivation via
  Sequential Memory-Hard Functions"* (BSDCan, 2009), introduce el concepto
  de función **memory-hard**: una KDF que no solo consume tiempo de CPU,
  sino una cantidad configurable y significativa de memoria RAM por cada
  intento. Esto encarece mucho más la construcción de hardware
  especializado (ASICs/FPGAs) para atacar por fuerza bruta, porque replicar
  memoria en silicio dedicado es mucho más caro que replicar solo lógica de
  cómputo.
- **Argon2 (2015).** Diseñado por Alex Biryukov, Daniel Dinu y Dmitry
  Khovratovich, ganó la *Password Hashing Competition* (PHC) en julio de
  2015 entre 24 propuestas, y quedó estandarizado en el **RFC 9106**
  (*"Argon2 Memory-Hard Function for Password Hashing and Proof-of-Work
  Applications"*). Su variante **Argon2id** combina resistencia a ataques de
  canal lateral con resistencia a ataques de memoria/GPU, y se configura con
  tres parámetros: memoria mínima (`m`), número de iteraciones (`t`) y
  grado de paralelismo (`p`).

La guía vigente de OWASP (*Password Storage Cheat Sheet*) es explícita sobre
el orden de preferencia: **Argon2id** es la primera opción cuando está
disponible (con configuraciones de referencia como `m=19456` (19 MiB),
`t=2`, `p=1`), **scrypt** como alternativa si Argon2id no está disponible
(por ejemplo `N=2^17`, `r=8`, `p=1`), y **bcrypt** solo para sistemas
legacy que no puedan migrar, con un factor de trabajo mínimo de 10 y la
limitación ya mencionada de 72 bytes de entrada.

El hilo común entre las tres es el mismo: convertir el cálculo del hash en
algo **deliberadamente lento y/o hambriento de memoria**, de modo que el
costo que paga el servidor legítimo (una vez por login) sea aceptable, pero
el costo que paga un atacante que prueba miles de millones de candidatos
offline se vuelva prohibitivo. Es la misma lógica de las iteraciones de
PBKDF2 (Lab 03 de esta cursada), llevada un paso más allá al incorporar
también el costo de memoria, no solo el de cómputo.

## Fuentes (mín. 3, verificables)

1. Provos, N. y Mazières, D. (1999). *A Future-Adaptable Password Scheme*.
   USENIX Annual Technical Conference.
   https://www.usenix.org/legacy/event/usenix99/provos/provos.pdf
2. Percival, C. (2009). *Stronger Key Derivation via Sequential Memory-Hard
   Functions*. BSDCan 2009. https://www.tarsnap.com/scrypt/scrypt.pdf
3. Biryukov, A., Dinu, D., Khovratovich, D. y Josefsson, S. (2021). *RFC
   9106 — Argon2 Memory-Hard Function for Password Hashing and
   Proof-of-Work Applications*. IETF.
   https://www.rfc-editor.org/info/rfc9106/
4. OWASP Cheat Sheet Series. (s.f.). *Password Storage Cheat Sheet*. OWASP
   Foundation.
   https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

## Reflexión (3-5 líneas)

Ninguna de estas KDFs resuelve el problema de fondo, solo lo encarece: si el
factor de trabajo no se ajusta periódicamente al hardware disponible (como ya le pasó a bcrypt frente a scrypt y Argon2), la protección se degrada con
el tiempo, no es un arreglo de una sola vez, sino un parámetro que hay que
revisar cada pocos años. Y ninguna protege contra una contraseña
intrínsecamente débil o reusada, solo hacen más caro el ataque offline
después de una brecha, no evitan la brecha en sí ni el reuso de
contraseñas (Parte A de este informe, y el caso de *credential stuffing*
visto en el Lab 03).
