# Cómo crear un laboratorio nuevo

Todo lab ofensivo hereda de esta plantilla. Pasos:

## 1. Copiar la plantilla

```bash
cp -r labs/_plantilla labs/lab06-enumeracion-de-servicios
```

El número y el tema se derivan **solos** del nombre del directorio
(`labNN-tema-con-guiones`). No hay que editar `start.sh`.

## 2. Armar el target vulnerable

En `entorno/target/` va el/los servicio(s) a reconocer/explotar. Puede ser:
- Un `server.py` propio (como en lab05), o
- Una imagen conocida deliberadamente vulnerable (DVWA, Juice Shop, etc.)
  referenciada en `entorno/target.compose.yml`.

Todos los servicios van en la red `labnet` con un `hostname` claro. **No
publiques puertos al host**: el alumno escanea desde la consola por la red interna.

## 3. Definir las flags

Escondé cada flag en el comportamiento del target (un banner, un header, una
respuesta). Después generá la línea del manifest:

```bash
bin/nueva-flag.sh R1 "Titulo del reto" 'FLAG{lo_que_sea}'   >> labs/lab06-.../retos.manifest
```

Guardá **solo el hash** en `retos.manifest` (nunca la flag en claro). En
`solucion.md` (solo docente) va la flag en claro y el camino para obtenerla.

Tip: ofuscá las flags en el código del target (base64) para que un vistazo casual
al source no las regale.

## 4. Escribir la guía

Completá `README.md` respetando la anatomía Teoría → Ejemplos → Tools → Práctica.
Avanzá la narrativa de PhantomCorp desde donde la dejó el lab anterior.

## 5. Rúbrica y entregables

Adaptá `docs/rubrica.md`, `docs/entregable.md` y `docs/research.md`. Mantené el
total en 100 y las causales de rechazo (uso responsable, IA no declarada).

## 6. Probar de punta a punta

```bash
make setup && ./ctf lab 06 && make shell
# ... obtené cada flag como lo haría el alumno ...
./ctf submit 06 R1 'FLAG{...}'
./ctf status 06
make down
```

Si una flag no se puede obtener con las tools tal como la guía lo indica, el lab
no está listo. Probalo vos antes que ellos.
