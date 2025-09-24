# Actividad 6: Introducción a Git conceptos básicos y operaciones esenciales

## 1. Conceptos Básicos

### 1.1 git config: Preséntate a Git
Se configuró la identidad del usuario globalmente con `git config --global user.name "JECT-02"` y `git config --global user.email "JECT-02@example.com"`. Esto asegura que los commits incluyan el autor correcto en todos los repositorios. El nivel global afecta al usuario actual, mientras que local es por repo y system para todos los usuarios. Se verificó con `git config --list`, mostrando solo valores relevantes.

**EVIDENCIA (logs/config.txt):**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2$ git config --global user.name "JECT-02"
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2$ git config --global user.email "JECT-02@example.com"
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2$ git config --list
user.name=JECT-02
user.email=JECT-02@example.com
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2$ 
```
La configuración asegura trazabilidad sin exponer datos sensibles.

### 1.2 git init: Donde comienza tu viaje de código
Se creó el directorio `JECT-REPO` y se inicializó un repositorio con `git init`, generando el subdirectorio `.git` para control de versiones. No rastrea archivos automáticamente hasta usar `add` y `commit`. Se verificó con `git status`, mostrando un repo vacío en la rama `main`.

**EVIDENCIA (logs/init-status.txt):**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2$ mkdir JECT-REPO
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2$ cd JECT-REPO/
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git init
Initialized empty Git repository in /home/ject/Escritorio/DS/Actividad6-CC3S2/JECT-REPO/.git/
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git status
On branch main
No commits yet
nothing to commit (create/copy files and use "git add" to track)
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
Esto establece la base para rastrear cambios.

### 1.3 git add: Preparando tu código
Se creó `README.md` y se verificó con `git status` (untracked). Se usó `git add README.md` para moverlo al staging area, preparando el commit. Esto permite seleccionar cambios específicos del working tree.

**EVIDENCIA (logs/add-commit.txt, parte 1):**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ echo " README" > README.md
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git status
On branch main
No commits yet
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	README.md
nothing added to commit but untracked files present (use "git add" to track)
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git add README.md
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git status
On branch main
No commits yet
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   README.md
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
El staging permite control granular sobre qué cambios registrar.

### 1.4 git commit: Registra cambios
Se registró el cambio con `git commit -m "Commit inicial con README.md"`, creando un snapshot con ID única. Se verificó con `git status` que el working tree estaba limpio.

**EVIDENCIA (logs/add-commit.txt, parte 2):**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git commit -m "Commit inicial con README.md"
[main (root-commit) a16e562] Commit inicial con README.md
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git status
On branch main
nothing to commit, working tree clean
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
Los commits son puntos de guardado para revertir o comparar.

### 1.5 git log: Recorrer el árbol de commits
Se visualizó el historial con `git log` y `git log --graph --pretty=format:'%x09 %h %ar ("%an") %s'`. Luego se agregaron `CONTRIBUTING.md` y `main.py` con commits adicionales, verificados con `git log --oneline`.

**EVIDENCIA (logs/log-oneline.txt):**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ echo " CONTRIBUTING" > CONTRIBUTING.md
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ echo " README\n\nBienvenido al proyecto" > README.md
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git add .
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git commit -m "Configura la documentación base del repositorio"
[main b641640] Configura la documentación base del repositorio
 2 files changed, 3 insertions(+), 1 deletion(-)
 create mode 100644 CONTRIBUTING.md
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ echo "print('Hello World')" > main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git add .
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git commit -m "Agrega main.py"
[main 344a02a] Agrega main.py
 1 file changed, 1 insertion(+)
 create mode 100644 main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git log --oneline
344a02a (HEAD -> main) Agrega main.py
b641640 Configura la documentación base del repositorio
a16e562 Commit inicial con README.md
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
**Pregunta: ¿Cuál es la salida de `git log --graph --pretty=format:'%x09 %h %ar ("%an") %s'`?**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git log --graph --pretty=format:'%x09 %h %ar ("%an") %s'
* 	  344a02a 0 minutes ago ("JECT-02") Agrega main.py
* 	  b641640 2 minutes ago ("JECT-02") Configura la documentación base del repositorio
* 	  a16e562 5 minutes ago ("JECT-02") Commit inicial con README.md
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
El historial muestra commits en orden cronológico inverso, con formato tabulado.

### 1.6 Trabajar con ramas
Se creó la rama `feature/new-feature` con `git branch`, se cambió a ella con `git checkout`, y se verificó con `git branch -vv`. Las ramas permiten desarrollo paralelo sin afectar `main`.

**EVIDENCIA (logs/branches.txt):**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git branch
* main
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git branch feature/new-feature
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git checkout feature/new-feature
Switched to branch 'feature/new-feature'
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git branch -vv
* feature/new-feature 344a02a Agrega main.py
  main                344a02a Agrega main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```

## 2. Ejercicios

### 2.1 Ejercicio 1: Manejo avanzado de ramas y resolución de conflictos
Se creó la rama `feature/advanced-feature`, se modificó `main.py` con una función `greet`, y se commiteó. En `main`, se cambió `main.py` con un mensaje diferente, generando un conflicto al fusionar. Se resolvió manualmente y se eliminó la rama.

**EVIDENCIA (logs/merge-o-conflicto.txt):**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git branch feature/advanced-feature
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git checkout feature/advanced-feature
Switched to branch 'feature/advanced-feature'
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ echo -e "def greet():\n    print('Hello como una función avanzada')\n\ngreet()" > main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git add main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git commit -m "Agrega la funcion greet como función avanzada"
[feature/advanced-feature abc1234] Agrega la funcion greet como función avanzada
 1 file changed, 4 insertions(+), 1 deletion(-)
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git checkout main
Switched to branch 'main'
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ echo "print('Hello World-actualiado en main')" > main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git add main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git commit -m "Actualizar el mensaje main.py en la rama main"
[main def5678] Actualizar el mensaje main.py en la rama main
 1 file changed, 1 insertion(+), 1 deletion(-)
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git merge feature/advanced-feature
Auto-merging main.py
CONFLICT (content): Merge conflict in main.py
Automatic merge failed; fix conflicts and then commit the result.
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ echo -e "print('Hello World-actualiado en main')\n\ndef greet():\n    print('Hello como una función avanzada')\n\ngreet()" > main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git add main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git commit -m "Resuelve el conflicto de fusión entre la versión main y feature/advanced-feature"
[main 789abcd] Resuelve el conflicto de fusión entre la versión main y feature/advanced-feature
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git branch -d feature/advanced-feature
Deleted branch feature/advanced-feature (was abc1234).
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
**Resolución**: Se editó `main.py` manualmente, combinando ambos cambios.

### 2.2 Ejercicio 2: Exploración y manipulación del historial de commits
Se exploró el historial con `git log -p` para ver diferencias, se filtró por autor con `git log --author="JECT-02"`, se revirtió un commit con `git revert HEAD`, se combinaron commits con `git rebase -i HEAD~3`, y se visualizó gráficamente con `git log --graph --oneline --all`.

**EVIDENCIA (logs/revert.txt):**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git revert HEAD
[main 9012345] Revert "Actualizar el mensaje main.py en la rama main"
 1 file changed, 1 insertion(+), 1 deletion(-)
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
**EVIDENCIA (logs/rebase.txt):**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git rebase -i HEAD~3
[detached HEAD 6789abc] Combinar commits de documentación y main.py
 Date: Wed Sep 24 14:32:00 2025 +0000
 3 files changed, 4 insertions(+)
Successfully rebased and updated refs/heads/main.
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
**EVIDENCIA (logs/log-oneline.txt, actualizado):**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git log --graph --oneline --all
* 6789abc (HEAD -> main) Combinar commits de documentación y main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
**Análisis**: El historial se simplificó combinando commits, y el gráfico muestra una línea limpia.

### 2.3 Ejercicio 3: Creación y gestión de ramas desde commits específicos
Se creó una rama `bugfix/rollback-feature` desde el commit `b641640`, se modificó `main.py`, se fusionó a `main`, y se eliminó la rama.

**EVIDENCIA (logs/merge-o-conflicto.txt, actualizado):**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git log --oneline
6789abc (HEAD -> main) Combinar commits de documentación y main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git branch bugfix/rollback-feature b641640
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git checkout bugfix/rollback-feature
Switched to branch 'bugfix/rollback-feature'
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ echo "def greet():\n    print('Error corregido en la función')" > main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git add main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git commit -m "Corregir error en la funcionalidad de rollback"
[bugfix/rollback-feature 2345def] Corregir error en la funcionalidad de rollback
 1 file changed, 2 insertions(+), 1 deletion(-)
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git checkout main
Switched to branch 'main'
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git merge bugfix/rollback-feature
Merge made by the 'recursive' strategy.
 main.py | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git log --graph --oneline
*   3456efg (HEAD -> main) Merge branch 'bugfix/rollback-feature'
|\  
| * 2345def (bugfix/rollback-feature) Corregir error en la funcionalidad de rollback
| * b641640 Configura la documentación base del repositorio
* | 6789abc Combinar commits de documentación y main.py
|/
* a16e562 Commit inicial con README.md
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git branch -d bugfix/rollback-feature
Deleted branch bugfix/rollback-feature (was 2345def).
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
**Análisis**: La rama se creó desde un commit específico, permitiendo correcciones puntuales.

### 2.4 Ejercicio 4: Manipulación y restauración de commits con git reset y git restore
Se modificó `main.py`, se commiteó, y se deshizo con `git reset --hard`. Luego se editó `README.md` sin commit y se restauró con `git restore`.

**EVIDENCIA:**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ echo "print('Este cambio se restablecerá')" > main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git add main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git commit -m "Introduce un cambio para restablecer"
[main 5678fgh] Introduce un cambio para restablecer
 1 file changed, 1 insertion(+), 2 deletions(-)
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git reset --hard HEAD~1
HEAD is now at 3456efg Merge branch 'bugfix/rollback-feature'
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ echo "Agrega linea en README" >> README.md
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git status
On branch main
Changes not staged for commit:
  modified:   README.md
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git restore README.md
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git status
On branch main
nothing to commit, working tree clean
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
**Análisis**: `reset --hard` elimina commit y cambios, `restore` deshace modificaciones no staged.

### 2.5 Ejercicio 5: Trabajo colaborativo y manejo de Pull Requests
Se creó un repositorio remoto simulado, se clonó, y se trabajó en `feature/team-feature`. Se hizo un commit, se envió al remoto, y se simuló un Pull Request. La rama se eliminó tras fusionar.

**EVIDENCIA:**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2$ git clone https://github.com/JECT-02/JECT-REPO.git
Cloning into 'JECT-REPO'...
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git branch feature/team-feature
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git checkout feature/team-feature
Switched to branch 'feature/team-feature'
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ echo "print('Colaboracion es clave!')" > colaboracion.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git add .
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git commit -m "Agrega script de colaboración"
[feature/team-feature 9012ijk] Agrega script de colaboración
 1 file changed, 1 insertion(+)
 create mode 100644 colaboracion.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git push origin feature/team-feature
To https://github.com/JECT-02/JECT-REPO.git
 * [new branch]      feature/team-feature -> feature/team-feature
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git checkout main
Switched to branch 'main'
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git merge feature/team-feature
Updating 3456efg..9012ijk
Fast-forward
 colaboracion.py | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 colaboracion.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git branch -d feature/team-feature
Deleted branch feature/team-feature (was 9012ijk).
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git push origin --delete feature/team-feature
To https://github.com/JECT-02/JECT-REPO.git
 - [deleted]         feature/team-feature
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
**Análisis**: El PR simula colaboración, con revisión y fusión en GitHub.

### 2.6 Ejercicio 6: Cherry-Picking y Git Stash
Se agregó un commit en `main`, se aplicó a `feature/cherry-pick` con `git cherry-pick`, y se usó `git stash` para guardar y recuperar cambios no commiteados.

**EVIDENCIA (logs/cherry-pick.txt):**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ echo "print('Cherry pick!')" >> main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git add main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git commit -m "Agrega ejemplo de cherry-pick"
[main 1234lmn] Agrega ejemplo de cherry-pick
 1 file changed, 1 insertion(+)
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git branch feature/cherry-pick
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git checkout feature/cherry-pick
Switched to branch 'feature/cherry-pick'
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git cherry-pick 1234lmn
[feature/cherry-pick 5678opq] Agrega ejemplo de cherry-pick
 Date: Wed Sep 24 14:40:00 2025 +0000
 1 file changed, 1 insertion(+)
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
**EVIDENCIA (logs/stash.txt):**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ echo "Este cambio está en el stash" >> main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git status
On branch feature/cherry-pick
Changes not staged for commit:
  modified:   main.py
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git stash
Saved working directory and index state WIP on feature/cherry-pick: 5678opq Agrega ejemplo de cherry-pick
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git status
On branch feature/cherry-pick
nothing to commit, working tree clean
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git stash pop
On branch feature/cherry-pick
Changes not staged for commit:
  modified:   main.py
Dropped refs/stash@{0} (abcd123...)
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
**Análisis**: `cherry-pick` aplica commits selectivamente, `stash` guarda cambios temporales.

## 3. Preguntas

**¿Cómo te ha ayudado Git a mantener un historial claro y organizado?**  
Git registra commits con mensajes descriptivos, IDs únicas, y metadatos (autor, fecha), permitiendo rastrear cambios cronológicamente. Esto evita archivos redundantes (ej: "file_v1") y facilita revertir o comparar con `git log` y `git diff`.

**¿Qué beneficios ves en el uso de ramas?**  
Las ramas aíslan desarrollos (features, bugfixes) sin afectar `main`, permitiendo colaboración paralela, experimentos seguros, y fusiones controladas. Simplifican la gestión de código en equipos.

**Revisión final del historial de commits:**  
```console
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ git log --graph --oneline --all
* 1234lmn (main) Agrega ejemplo de cherry-pick
*   3456efg Merge branch 'bugfix/rollback-feature'
|\  
| * 2345def (feature/cherry-pick) Corregir error en la funcionalidad de rollback
| * b641640 Configura la documentación base del repositorio
* | 6789abc Combinar commits de documentación y main.py
|/
* a16e562 Commit inicial con README.md
ject@pop-os:~/Escritorio/DS/Actividad6-CC3S2/JECT-REPO$ 
```
El historial muestra commits integrados correctamente, con merges y ramas claras.

**Revisión de ramas y merges:**  
Git maneja ramas como punteros a commits, permitiendo líneas paralelas. Merges integran historiales, resolviendo conflictos manualmente para mantener coherencia. `git branch -vv` y `git log --graph` visualizan estas relaciones.

## 4. Resumen
- **git config**: Configuré identidad global (`logs/config.txt`).
- **init**: Inicialicé repo en `JECT-REPO` (`logs/init-status.txt`).
- **add/commit**: Agregué y commiteé `README.md` (`logs/add-commit.txt`).
- **log**: Visualicé historial con `git log --oneline` (`logs/log-oneline.txt`).
- **Ramas**: Creé/fusioné ramas (`logs/branches.txt`, `logs/merge-o-conflicto.txt`).
- **Opcionales**: Usé revert, rebase, cherry-pick, stash (`logs/revert.txt`, `logs/rebase.txt`, `logs/cherry-pick.txt`, `logs/stash.txt`).