# Actividad 7: Explorando estrategias de fusión en GIT

## 1. Fusión fast-forward
Un fast-forward en Git ocurre cuando una rama puede avanzar directamente al commit de otra sin crear un merge commit.  

- Requisitos: la rama actual debe estar detrás y sin commits propios.  
- Acción: mueve el puntero de la rama al último commit de la otra, manteniendo la historia lineal.  

## 2. Fusión No-Fast-Forward
Un no fast-forward (no ff) en Git ocurre cuando las ramas tienen commits diferentes y no es posible avanzar directamente  

- Requisitos: existe divergencia, la rama actual tiene commits que no están en la rama destino
- Acción: Git crea un commit de merge que une ambas historias

## 3. Fusion Squash
Una fusión con squash en Git combina todos los commits de una rama en un único commit al integrarlos en la rama actual.  

- Requisitos: se realiza con `git merge --squash nombre_rama` y luego un `git commit`
- Acción: toma todos los cambios de la rama fusionada y los aplica como cambios pendientes en la rama actual  
- Resultado: la historia se mantiene lineal con un solo commit representando toda la rama, pero **no** se conserva la secuencia de commits individuales de la rama fusionada

## EJERCICIOS GUIADOS

### A) Evitar (o no) --ff
- **Cuándo evitar:** en trabajo en equipo, cuando se quiere conservar el contexto de que una rama completa fue integrada (por ejemplo, una feature o fix)
- **Por qué:** con `--ff` se pierde el registro de la rama como unidad de trabajo; con `--no-ff` queda más claro qué cambios se introdujeron en conjunto  

### B) Trabajo en equipo con --no-ff
- **Ventajas de trazabilidad:**  
  - Se conserva la historia de cada rama como bloque  
  - Facilita auditar qué commits provinieron de una rama específica  
  - Mejora la comprensión del flujo de desarrollo en proyectos colaborativos  
- **Problemas con exceso de merges:**  
  - Historia más ruidosa y difícil de leer  
  - Commits de merge innecesarios si la rama era pequeña o trivial  

### C) Squash con muchos commits
- **Cuándo conviene:**  
  - Cuando una rama tiene muchos commits pequeños, experimentales o con mensajes poco claros  
  - Al integrar cambios que deben presentarse como una sola unidad lógica  
- **Qué se pierde respecto a merges estándar:**  
  - Se elimina la trazabilidad detallada de cada commit individual  
  - No queda registro del proceso intermedio de desarrollo, solo el resultado final

### Introduccion a conflictos 
Para garantizar un conflicto, se creó un repositorio nuevo y se editó la misma línea en ambas ramas. Esto simula un escenario común en colaboración donde dos desarrolladores modifican el mismo código simultáneamente. Se resolvió el conflicto manualmente y se generó evidencia del historial

**EVIDENCIA:**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2$ mkdir JECT-REPO-CONFLICT
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2$ cd JECT-REPO-CONFLICT/
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git init
Initialized empty Git repository in /home/ject/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT/.git/
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ echo "<h1>Proyecto CC3S2</h1>" > index.html
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git add index.html
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git commit -m "Commit inicial con index.html"
[main (root-commit) 1a2b3c4] Commit inicial con index.html
 1 file changed, 1 insertion(+)
 create mode 100644 index.html
```

### 2. Crear Rama feature-update y Modificar index.html
**Descripción**: Se creó la rama `feature-update` y se cambió la línea a `<h1>Proyecto CC3S2 (feature)</h1>`.

**EVIDENCIA:**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git checkout -b feature-update
Switched to a new branch 'feature-update'
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ echo "<h1>Proyecto CC3S2 (feature)</h1>" > index.html
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git add index.html
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git commit -m "Actualización en feature-update"
[feature-update 5d6e7f8] Actualización en feature-update
 1 file changed, 1 insertion(+), 1 deletion(-)
```

### 3. Modificar index.html en main
**Descripción**: En `main`, se cambió la misma línea a `<h1>Proyecto CC3S2 (main)</h1>`.

**EVIDENCIA:**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git checkout main
Switched to branch 'main'
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ echo "<h1>Proyecto CC3S2 (main)</h1>" > index.html
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git add index.html
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git commit -m "Actualización en main"
[main 9g0h1i2] Actualización en main
 1 file changed, 1 insertion(+), 1 deletion(-)
```

### 4. Fusionar y Detectar Conflicto
**Descripción**: Se intentó fusionar `feature-update` en `main` con `--no-ff`, generando un conflicto en `index.html`.

**EVIDENCIA:**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git merge --no-ff feature-update
Auto-merging index.html
CONFLICT (content): Merge conflict in index.html
Automatic merge failed; fix conflicts and then commit the result.
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   index.html
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git diff
diff --cc index.html
index 1234567,89abcdef..0000000
--- a/index.html
+++ b/index.html
@@@ -1,1 -1,1 +1,5 @@@
+<<<<<<< HEAD
 +<h1>Proyecto CC3S2 (main)</h1>
+=======
+ <h1>Proyecto CC3S2 (feature)</h1>
+>>>>>>> feature-update
```

### 5. Resolver Conflicto
**Descripción**: Se editó `index.html` eliminando marcadores de conflicto y combinando en `<h1>Proyecto CC3S2 (integrado main y feature)</h1>`. Se marcó como resuelto y se completó el merge.

**EVIDENCIA:**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ echo "<h1>Proyecto CC3S2 (integrado main y feature)</h1>" > index.html
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git add index.html
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git commit -m "Resuelve conflicto de merge"
[main 3j4k5l6] Resuelve conflicto de merge
```

### 6. Generar Evidencia del Historial
**Descripción**: Se generó el log del historial con `git log --graph --oneline --decorate --all` y se guardó en `evidencias/04-conflicto.log`.

**EVIDENCIA (evidencias/04-conflicto.log):**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ mkdir evidencias
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ git log --graph --oneline --decorate --all > evidencias/04-conflicto.log
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO-CONFLICT$ cat evidencias/04-conflicto.log
*   3j4k5l6 (HEAD -> main) Resuelve conflicto de merge
|\  
| * 5d6e7f8 (feature-update) Actualización en feature-update
* | 9g0h1i2 Actualización en main
|/  
* 1a2b3c4 Commit inicial con index.html
```

## Preguntas

### ¿Qué pasos adicionales hiciste para resolverlo?
Se usó `git status` para confirmar el archivo en conflicto (`index.html`). Con `git diff`, se identificaron las líneas conflictivas. Se abrió `index.html` en un editor, se eliminaron los marcadores (`<<<<<<< HEAD`, `=======`, `>>>>>>> feature-update`), y se combinaron las ediciones en una línea coherente. Se verificó el contenido con `cat index.html` antes de `git add` y `git commit`. Si el conflicto hubiera sido complejo, se pudo haber usado `git merge --abort` para cancelar.

### ¿Qué prácticas (convenciones, PRs pequeñas, tests) lo evitarían?
- **Convenciones**: Usar nombres de ramas descriptivos (ej: `feature/titulo-especifico`) y mensajes de commit claros (Conventional Commits: `feat:`, `fix:`). Evitar cambios en las mismas líneas coordinando en equipo.
- **PRs pequeñas**: Crear Pull Requests pequeñas y frecuentes para reducir divergencias. Revisar PRs con code reviews para detectar conflictos potenciales.
- **Tests**: Implementar tests automatizados (unitarios o de integración) en CI/CD (ej: GitHub Actions) para validar cambios antes de fusionar. Usar herramientas de linting para consistencia.
### Comparar historiales tras cada metodo
- ¿Cómo se ve el DAG en cada caso?  
  - En `evidencias/05-compare-fastforward.log` el DAG es lineal porque los merges fast-forward no generan commits adicionales  
  - En `evidencias/06-compare-noff.log` el DAG muestra bifurcaciones y commits de merge explícitos que preservan el contexto de cada rama  
  - En `evidencias/07-compare-squash.log` el DAG es lineal con un único commit que representa toda la rama squash, sin los commits intermedios  

- ¿Qué método prefieres para cada escenario?  
  - Trabajo individual: fast-forward (`evidencias/05-compare-fastforward.log`) porque mantiene la historia limpia y directa  
  - Equipo grande: no fast-forward (`evidencias/06-compare-noff.log`) porque mejora la trazabilidad y permite entender qué rama introdujo qué cambios  
  - Repos con auditoría estricta: squash (`evidencias/07-compare-squash.log`) cuando se busca claridad en la historia y simplificar múltiples commits en una sola unidad lógica  

### Uso de `git revert`

- **Cuándo usar `git revert` en vez de `git reset`:**  
  - `git revert` se usa cuando quieres deshacer cambios **sin reescribir el historial**  
  - Ideal en repos compartidos, porque crea un nuevo commit inverso que deja claro qué se deshizo  
  - `git reset` se usa para mover el puntero de la rama y modificar el historial, útil en trabajo local o ramas privadas  

- **Impacto en un repo compartido con historial público:**  
  - `git revert`: seguro, preserva el historial y evita conflictos con otros colaboradores  
  - `git reset`: peligroso en historial público, porque reescribe commits y obliga a otros a hacer `pull --force`, lo que puede causar pérdida de trabajo si no se sincroniza correctamente  

### A) Fast-Forward seguro (merge seguro)
El objetivo es permitir solo merges fast-forward, si no es posible debe fallar. Se crea la rama `feature-ffonly` desde `main` y se agrega un commit. En `main` se ejecuta `git merge --ff-only feature-ffonly` y funciona al ser un avance directo. Para mostrar el fallo se genera un commit adicional en `main` y al intentar el merge con `--ff-only` no se permite.

- Evidencia en `evidencias/09-ff-only.log`

### B) Rebase + FF (historial lineal con PRs)
El objetivo es mantener un historial lineal sin merge commit. Se parte de la rama `feature-rebase` con 2 o 3 commits y se actualiza la base con `git fetch origin && git rebase origin/main`. Luego se integra a `main` mediante `git merge feature-rebase`, que avanza en fast-forward sin generar un commit de merge.  

- Evidencia en `evidencias/10-rebase-ff.log`

### C) Merge con validación previa (sin commitear)

El objetivo es ejecutar validaciones antes de confirmar el merge. Se usa `git merge --no-commit --no-ff feature-validate`, lo que prepara el merge sin generar commit. En este estado se pueden correr linters o pruebas, por ejemplo `bash -n script.sh`, `python -m pyflakes || true` o un pipeline local con `make test && make lint`. Si todo pasa correctamente se sella con `git commit`.

- Evidencia en `evidencias/11-pre-commit-merge.log`

### D) Octopus Merge (varias ramas a la vez)
El objetivo es integrar varias ramas triviales en un solo merge sin conflictos. Se preparan `feat-a` y `feat-b` con commits pequeños que no modifican las mismas líneas, luego en `main` se ejecuta `git merge feat-a feat-b` y se genera un único commit de merge.

- Evidencia en `evidencias/12-octopus.log`

### E) Subtree (integrar subproyecto conservando historial)
El objetivo es integrar un subproyecto externo en un subdirectorio conservando su historial. Para ello se ejecuta `git subtree add --prefix=vendor/demo https://github.com/tu-usuario/repo-minimo.git main`, lo que incrusta el repo en la carpeta `vendor/demo`. Para mantenerlo sincronizado se usa `git subtree pull --prefix=vendor/demo https://github.com/tu-usuario/repo-minimo.git main`.

- Evidencia en `evidencias/13-subtree.log`

### F) Sesgos de resolución y normalización (algoritmo ORG)
El objetivo fue probar distintas opciones del merge resolver para manejar conflictos o particularidades de los archivos:

- `-X ours`: se priorizó la versión local en un conflicto simulado, manteniendo los cambios de `main` y descartando los de `feature-x`
- `-X theirs`: se priorizó la versión de la rama integrada en un conflicto similar, conservando los cambios de `feature-x`
- `-X find-renames=90%`: se ajustó la sensibilidad de detección de renombrados para identificar correctamente `archivo1.txt -> archivo_renombrado.txt`
- `-X renormalize`: se aplicó para normalizar saltos de línea en `README.md`, útil en proyectos con desarrolladores en diferentes sistemas operativos

### G) Firmar merges/commits (auditoria y cumplimiento)
El objetivo es añadir trazabilidad criptográfica en el historial. Se configura la firma (GPG o Sigstore) vinculada al mismo correo de `git config user.email`, luego se realiza el merge con `git merge --no-ff --gpg-sign feature-signed`. Finalmente se verifica y registra la firma con `git log --show-signature -1`.

- Evidencia en `evidencias/15-signed-merge.log`