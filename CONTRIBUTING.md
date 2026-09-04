# Cómo entregar un laboratorio

Este documento describe el flujo de entrega. Vale para **todos** los
laboratorios de la asignatura. Si algo del enunciado particular contradice
esto, manda el enunciado.

El mecanismo es **fork + Pull Request**. No es un capricho: es el flujo real
con el que se colabora en cualquier proyecto de software serio. Aprenderlo es
parte de la materia.

---

## 0. Antes de empezar: armá el grupo

- **4 a 5 integrantes.** Ni 3 ni 6.
- Designen **un integrante responsable del fork**. Ese fork es el espacio de
  trabajo del grupo; los demás integrantes colaboran sobre él.
- Elijan el número de grupo que les asignó la cátedra. Va a usarse en el
  nombre del directorio y de la rama.

---

## 1. Fork del repositorio

Entrá a https://github.com/fboiero/LabsSeguridadInformatica2026 y hacé clic en
**Fork** (arriba a la derecha). Eso crea una copia bajo tu cuenta.

Cloná tu fork:

```bash
git clone https://github.com/TU-USUARIO/LabsSeguridadInformatica2026.git
cd LabsSeguridadInformatica2026
```

Agregá el repositorio original como remoto `upstream`. Esto te permite traer
las actualizaciones que publique la cátedra:

```bash
git remote add upstream https://github.com/fboiero/LabsSeguridadInformatica2026.git
git remote -v
```

Deberías ver cuatro líneas: `origin` (tu fork) y `upstream` (el de la
cátedra), cada uno en modo `fetch` y `push`.

---

## 2. Sumar a los compañeros al fork

El integrante responsable va a **Settings → Collaborators** en su fork y
agrega a los demás integrantes del grupo. Así todos pueden pushear a la misma
rama y el historial refleja el trabajo real de cada uno.

> **Esto importa para la nota.** Un laboratorio con commits de una sola cuenta
> se considera no entregado por el grupo. Ver la rúbrica de cada lab.

---

## 3. Sincronizar antes de empezar

Cada vez que arranques a trabajar, traé lo último de la cátedra:

```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

---

## 4. Crear la rama de trabajo

Una rama por laboratorio, con este nombre exacto:

```bash
git checkout -b lab01-grupo07
```

Formato: `labNN-grupoXX`. Con dos dígitos en ambos números.

---

## 5. Trabajar

Creá el directorio de tu grupo y trabajá **solamente ahí dentro**:

```bash
mkdir -p entregas/lab01/grupo07
```

**Qué NO tocar, nunca:**

- Nada dentro de `labs/`. El enunciado y el esqueleto son de solo lectura.
- Nada dentro de `entregas/labNN/grupoYY/` de otro grupo.
- `README.md`, `CONTRIBUTING.md`, `.github/` en la raíz.

Si tocás algo de eso, el Pull Request va a generar conflictos con los de tus
compañeros y se te va a pedir que lo rehagas.

El esqueleto de código se **copia** a tu directorio antes de completarlo:

```bash
cp -r labs/lab01-introduccion/src entregas/lab01/grupo07/src
```

---

## 6. Commits

Hacé commits **chicos y frecuentes**, con mensajes que digan qué cambió y por
qué. Un único commit gigante llamado `entrega` no describe nada y se penaliza
en el criterio de proceso.

```bash
git add entregas/lab01/grupo07/src/integridad.py
git commit -m "lab01: implementar subcomando generar del manifiesto"
```

Buenos mensajes:

- `lab01: implementar recorrido recursivo en generar`
- `lab01: corregir clasificacion de archivos NUEVO en verificar`
- `lab01: agregar analisis CIA del caso WannaCry`

Malos mensajes:

- `cambios`
- `arreglos varios`
- `.`

**Cada integrante commitea desde su propia cuenta.** Verificá que tu identidad
de Git esté bien configurada:

```bash
git config user.name "Nombre Apellido"
git config user.email "tu-email-de-github@ejemplo.com"
```

Si el email no coincide con el de tu cuenta de GitHub, tus commits no se te
van a atribuir y va a parecer que no trabajaste.

---

## 7. Push y Pull Request

```bash
git push origin lab01-grupo07
```

GitHub te va a ofrecer un botón **Compare & pull request**. Hacé clic.

- **Base repository:** `fboiero/LabsSeguridadInformatica2026`, rama `main`
- **Head repository:** tu fork, rama `lab01-grupo07`
- **Título:** `Lab 01 — Grupo 07`
- **Descripción:** completá la plantilla que aparece automáticamente. No la
  borres.

Después de abrir el PR podés seguir haciendo commits: se agregan solos al
mismo PR. Lo que cuenta es el estado al momento del cierre de la entrega.

---

## 8. Correcciones

El docente revisa el PR y deja comentarios. Si hay pedidos de corrección:

1. Corregí en tu rama local.
2. Commiteá y pusheá a la misma rama.
3. Respondé el comentario en GitHub indicando qué cambiaste.

El PR se actualiza solo. **No abras un PR nuevo.**

---

## Uso responsable — leé esto

Esta asignatura enseña técnicas que, aplicadas fuera de contexto, constituyen
delito. En la República Argentina, la **Ley 26.388** incorporó al Código Penal
las figuras de acceso indebido a sistemas informáticos, daño informático y
otras conductas relacionadas.

Reglas no negociables:

1. **Solo practicás sobre lo que es tuyo o sobre lo que la cátedra provee.**
   Tu propia máquina, tu propia máquina virtual, o los entornos deliberadamente
   vulnerables que se indiquen en cada enunciado.
2. **Nunca** contra sistemas de la Facultad, de la Universidad, de compañeros,
   de empresas, ni de ningún tercero.
3. Una autorización verbal **no es** autorización. En el mundo profesional, un
   pentest sin contrato firmado y alcance escrito es un delito con más pasos.
4. Si en el desarrollo de un lab encontrás por accidente una vulnerabilidad
   real en un sistema de terceros: **no la explores, no la explotes**.
   Informala al docente y detenete ahí.

El incumplimiento de estas reglas implica la desaprobación de la asignatura,
sin perjuicio de las acciones institucionales y legales que correspondan.

---

## Declaración de uso de IA

En todos los entregables hay una sección obligatoria de declaración de uso de
asistentes de IA (ChatGPT, Claude, Copilot, Gemini, etc.).

**No está prohibido usarlos.** Lo que se evalúa es que entiendas lo que
entregás. Lo que sí está prohibido es no declararlo.

En la declaración indicá, como mínimo:

- Qué herramienta usaste.
- Para qué la usaste (redacción, depuración, explicación de un concepto,
  generación de código).
- Qué partes del entregable se originaron o modificaron con esa asistencia.
- Cómo verificaste que lo que te devolvió era correcto.

Una declaración honesta no baja la nota. Una declaración omitida es causal de
rechazo automático de la entrega.

---

## Preguntas frecuentes

**¿Puedo entregar fuera de término?**
Consultá el régimen de cursado de la cátedra. La fecha límite de cada lab está
en su enunciado.

**Se me llenó el PR de conflictos, ¿qué hago?**
Casi siempre es porque tocaste archivos fuera de tu directorio de grupo.
Sincronizá con `upstream` (paso 3), revisá qué archivos modificaste con
`git status`, y revertí los que no te corresponden.

**¿Puedo ver la entrega de otro grupo?**
Sí, el repositorio es público y los PR también. Mirar cómo resuelve otro está
bien y es parte de aprender. **Copiar sin atribución no.** Si te inspiraste en
la solución de otro grupo, citalo en tu entregable — como citarías cualquier
otra fuente.

**¿Puedo usar bibliotecas externas?**
En los **labs de código** (Unidades 1 a 4), salvo que el enunciado lo autorice,
no: están diseñados para resolverse con la biblioteca estándar de Python. Esa
restricción es pedagógica: si `pip install` te resuelve el ejercicio, no
aprendiste el ejercicio.

**¿Y en los labs ofensivos (Unidad 5 en adelante)? ¿Tengo que instalar nmap, Kali, etc.?**
No. Esos labs corren en **Docker** y todas las herramientas ya vienen dentro de
una "consola del atacante" que se levanta sola. Tu máquina queda limpia: solo
necesitás Docker. El flujo es `make setup` (una vez) y después `./ctf lab NN`.
El enunciado de cada lab te guía. **Regla que no cambia:** esas herramientas se
usan **exclusivamente** contra los contenedores que provee la cátedra — ver
*Uso responsable* más arriba.
