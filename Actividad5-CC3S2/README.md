# Actividad 5: Construyendo un pipeline DevOps con Make y Bash

## 1. EJERCICIOS 

### 1.1 Ejecuta make help y guarda la salida para análisis. Luego inspecciona .DEFAULT_GOAL y .PHONY dentro del Makefile. Comandos:
El comando `make help` imprime un listado de objetivos disponibles en el `Makefile` junto con una breve descripción de cada uno
La directiva `.DEFAULT_GOAL := help` hace que, al ejecutar `make` sin argumentos, se muestre directamente esta ayuda en lugar de otro objetivo  
Esto permite al usuario conocer las opciones sin necesidad de leer manualmente el archivo.  
Por su parte, `.PHONY` declara que ciertos objetivos (como `help`, `clean`, `test`) no corresponden a archivos reales 
Así se evita que `make` considere cumplido un target solo porque exista un fichero con ese nombre
En conjunto, estas prácticas mejoran la usabilidad y aseguran la ejecución confiable de los objetivos

### 1.2. Comprueba la generación e idempotencia de build. Limpia salidas previas, ejecuta build, verifica el contenido y repite build para constatar que no rehace nada si no cambió la fuente
En la primera corrida, `make build` ejecuta el grafo de dependencias y genera `out/hello.txt` porque no existía
En la segunda corrida, `make` detecta que `out/hello.txt` ya está actualizado respecto a su dependencia `src/hello.py`, por lo que no recompila  
Esto se debe a que `make` compara las marcas de tiempo de los archivos en el grafo de dependencias: si el objetivo está más reciente que sus fuentes, no hace nada  
En resumen, la primera ejecución construye el artefacto y la segunda confirma que no hay cambios pendientes

### 1.3 Fuerza un fallo controlado para observar el modo estricto del shell y .DELETE_ON_ERROR. Sobrescribe PYTHON con un intérprete inexistente y verifica que no quede artefacto corrupto.
El modo estricto del shell con `-e -u -o pipefail` asegura que cualquier error en un comando detenga la ejecución inmediatamente  
Con `-e`, si un comando falla no se continúa con el resto de la receta  
La opción `-u` evita usar variables no definidas que podrían generar resultados inesperados  
`-o pipefail` hace que un fallo en cualquier parte de una tubería se propague como error de toda la línea  
Además, la directiva `.DELETE_ON_ERROR` de `make` elimina automáticamente el archivo objetivo parcial si ocurre un fallo durante su construcción  
Esto evita que queden artefactos corruptos como `out/hello.txt` incompleto  
En conjunto, estas medidas garantizan que el árbol de dependencias se mantenga consistente y reproducible  

### 1.4 Realiza un "ensayo" (dry-run) y una depuración detallada para observar el razonamiento de Make al decidir si rehacer o no
La traza muestra cómo `make` lee primero el `Makefile` y decide si alguno de los objetivos requiere reconstrucción  
Al evaluar el objetivo `build`, detecta que depende de `out/hello.txt`  
Como `out/hello.txt` no existe, `make` sigue el grafo de dependencias hasta `src/hello.py`, que sí está actualizado y no necesita recompilarse  
Con esa verificación, determina que `out/hello.txt` debe reconstruirse  
Ejecuta entonces la receta correspondiente: primero `mkdir -p out` y luego `python3 src/hello.py > out/hello.txt`  
Los mensajes sobre procesos hijos indican que `make` lanzó subprocesos para cada comando y esperó su finalización exitosa  
Tras completarse, marca `out/hello.txt` como reconstruido y con ello satisface también el objetivo `build`  
En conclusión, la traza refleja paso a paso cómo `make` recorre dependencias, verifica marcas de tiempo y ejecuta solo lo necesario  

### 1.5. Demuestra la incrementalidad con marcas de tiempo. Primero toca la fuente y luego el target para comparar comportamientos
Cuando se ejecuta `touch src/hello.py`, se actualiza la marca de tiempo de la fuente, quedando más reciente que el archivo objetivo `out/hello.txt`  
`make` compara estas marcas de tiempo en el grafo de dependencias y concluye que el target está desactualizado respecto a su fuente  
Por ello, ejecuta nuevamente la receta para regenerar `out/hello.txt` a partir del script  
En cambio, al hacer `touch out/hello.txt`, el archivo objetivo aparece con fecha más nueva que la de `src/hello.py`  
Esto indica a `make` que el target ya está actualizado y no es necesario rehacerlo  
De esta manera, `make` evita trabajo innecesario y garantiza que los artefactos siempre estén sincronizados con sus fuentes  

### 1.6. Ejecuta verificación de estilo/formato manual (sin objetivos lint/tools). Si las herramientas están instaladas, muestra sus diagnósticos; si no, deja evidencia de su ausencia
En la corrida no se generaron advertencias porque las herramientas `shellcheck` y `shfmt` no están instaladas en el entorno  
`shellcheck` sirve para detectar errores y malas prácticas en scripts de shell, mientras que `shfmt` aplica formateo automático consistente  
La ausencia de ambas herramientas impide obtener sugerencias de mejora o verificar estilo y errores comunes  
Para instalarlas en Linux se pueden usar los paquetes del sistema, por ejemplo `sudo apt install shellcheck shfmt` en distribuciones basadas en Debian  
Con estas utilidades instaladas, el flujo de linting y formateo quedaría completo y reproducible  
EVIDENCIA:
```console
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ command -v shellcheck >/dev/null && shellcheck scripts/run_tests.sh | tee logs/lint-shellcheck.txt || echo "shellcheck no instalado" | tee logs/lint-shellcheck.txt
command -v shfmt >/dev/null && shfmt -d scripts/run_tests.sh | tee logs/format-shfmt.txt || echo "shfmt no instalado" | tee logs/format-shfmt.txt
shellcheck no instalado
shfmt no instalado
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ 
```

### 1.7. Construye un paquete reproducible de forma manual, fijando metadatos para que el hash no cambie entre corridas idénticas. Repite el empaquetado y compara hashes
Hash reproducible obtenido:  
`513feda84378f3b46112a0f326095d77246474532ccffd92f0c4df4b1f13ec30`  

La opción `--sort=name` ordena los archivos dentro del tar, eliminando variabilidad debida al orden de entrada  
`--mtime=@0` fija la marca de tiempo de todos los ficheros a la época (1970-01-01), evitando diferencias por fechas de modificación  
`--numeric-owner`, junto con `--owner=0` y `--group=0`, normaliza metadatos de usuario y grupo sin depender del sistema local  
El uso de `gzip -n` desactiva el almacenamiento del nombre original y la hora en el encabezado del gzip, garantizando compresión determinista  
Con estos parámetros, ejecutar el empaquetado múltiples veces produce siempre el mismo hash, validando la reproducibilidad  

### 1.8. Reproduce el error clásico "missing separator" sin tocar el Makefile original. Crea una copia, cambia el TAB inicial de una receta por espacios, y confirma el error

En Make, cada línea de receta debe comenzar con un carácter TAB y no con espacios, porque el parser distingue así las acciones de los objetivos  
Si se usan espacios en lugar de TAB, aparece el error “falta un separador” al leer el Makefile  
Esto se debe a que Make interpreta espacios como parte de la sintaxis de dependencias y no como inicio de receta  
Para diagnosticarlo rápido, basta revisar la línea indicada en el error o usar un editor que muestre caracteres invisibles  
Otra técnica es ejecutar `cat -A Makefile_bad | grep '^ '` para detectar espacios al inicio en lugar de TAB  

### 1.9. Ejecuta ./scripts/run_tests.sh en un repositorio limpio. Observa las líneas "Demostrando pipefail": primero sin y luego con pipefail. Verifica que imprime "Test pasó" y termina exitosamente con código 0 (echo $?).

```console
$ ./scripts/run_tests.sh |& tee logs/run_tests.txt
Demostrando pipefail:
Sin pipefail: el pipe se considera exitoso (status 0).
Con pipefail: se detecta el fallo (status != 0).
Test pasó: Hello, World!
$ echo $?
0
```

En esta ejecución se demuestra la diferencia entre un pipelinesin `pipefail` es decir que oculta errores, y con `pipefail` que propaga correctamente errores

El mensaje `Test pasó: Hello, World!` confirma que la lógica principal funcionó y el código de salida 0 valida que el script terminó exitosamente

### 1.10. Edita src/hello.py para que no imprima "Hello, World!". Ejecuta el script: verás "Test falló", moverá hello.py a hello.py.bak, y el trap lo restaurará. Confirma código 2 y ausencia de .bak
## Evidencia: fallo controlado y restauración de `src/hello.py`

```console
$ ./scripts/run_tests.sh
Demostrando pipefail:
Sin pipefail: el pipe se considera exitoso (status 0)
Con pipefail: se detecta el fallo (status != 0)
Test falló: salida inesperada
$ echo $?
2
```

En esta ejecución se modificó `src/hello.py` para producir una salida no esperada, el test detectó la discrepancia y el script terminó con código `2`  
Antes de salir, el script movió `hello.py` a `hello.py.bak` y el `trap` lo restauró, por lo que no queda ningún archivo `.bak` en el repositorio  
Esto demuestra el manejo seguro de fallos y la restauración automática del estado original

### 1.11. Ejecuta bash -x scripts/run_tests.sh. Revisa el trace: expansión de tmp y PY, llamadas a funciones, here-doc y tuberías. Observa el trap armado al inicio y ejecutándose al final; estado 0

```console
$ bash -x scripts/run_tests.sh |& tee logs/trace-run_tests.txt
+scripts/run_tests.sh:20:cleanup()  rc=0
+scripts/run_tests.sh:21:cleanup()  rm -f /tmp/tmp.oAu7BXlAVA
+scripts/run_tests.sh:22:cleanup()  '[' -f src/hello.py.bak ']'
+scripts/run_tests.sh:25:cleanup()  exit 0
exit=0
```
- El `trap` (línea 27 del script) asegura que al salir se ejecute `cleanup()`
- Se observa la expansión del archivo temporal en `/tmp/tmp.oAu7BXlAVA`
- La función `cleanup()` verifica si existe `hello.py.bak` y limpia residuos
- Finalmente, `exit=0` confirma que el script terminó exitosamente

### 1.12. Sustituye output=$("$PY" "$script") por ("$PY" "$script"). Ejecuta script. output queda indefinida; con set -u, al referenciarla en echo aborta antes de grep. El trap limpia y devuelve código distinto no-cero

```console
$ ./scripts/run_tests.sh
Demostrando pipefail:
Sin pipefail: el pipe se considera exitoso (status 0).
Con pipefail: se detecta el fallo (status != 0).
./scripts/run_tests.sh: línea 44: Hello, World!: orden no encontrada
```

Se sustituyó la asignación de output por ("$PY" "$script"), lo que ejecuta 
la cadena como comando en vez de capturar su salida. Por eso el shell intenta 
correr "Hello, World!" como si fuera un binario y falla. Al no definirse la 
variable output, con set -u y el trap activado el script termina en error 
no cero, pero asegurando limpieza y restauración correcta

## 2. Leer - Analizar un repositorio

### EJERCICIOS

#### 2.1. Ejecuta make -n all para un dry-run que muestre comandos sin ejecutarlos; identifica expansiones $@ y $<, el orden de objetivos y cómo all encadena tools, lint, build, test, package
```console
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ make -n all
command -v python3 >/dev/null || { echo "Falta python3"; exit 1; }
command -v shellcheck >/dev/null || { echo "Falta shellcheck"; exit 1; }
command -v shfmt >/dev/null || { echo "Falta shfmt"; exit 1; }
command -v grep >/dev/null || { echo "Falta grep"; exit 1; }
command -v awk >/dev/null || { echo "Falta awk"; exit 1; }
command -v tar >/dev/null || { echo "Falta tar"; exit 1; }
tar --version 2>/dev/null | grep -q 'GNU tar' || { echo "Se requiere GNU tar"; exit 1; }
command -v sha256sum >/dev/null || { echo "Falta sha256sum"; exit 1; }
shellcheck scripts/run_tests.sh
shfmt -d scripts/run_tests.sh
command -v ruff >/dev/null 2>&1 && ruff check src || echo "ruff no instalado; omitiendo lint Python"
mkdir -p out
python3 src/hello.py > out/hello.txt
scripts/run_tests.sh
python3 -m unittest discover -s tests -v
mkdir -p dist
tar --sort=name --owner=0 --group=0 --numeric-owner --mtime='UTC 1970-01-01' -czf dist/app.tar.gz -C out hello.txt
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ 
```
El dry run muestra que all encadena tools lint build test y package
Las variables automaticas como `$@` y `$<` se expanden a nombre de objetivo y primera dependencia aunque aqui se ven resueltas en comandos finales

Primero se revisan dependencias con command `-v` luego se ejecutan lint y formateo
Despues se genera `out/hello.txt` a partir de `src/hello.py` se corren pruebas y se empaqueta en `dist/app.tar.gz`

Esto confirma el flujo completo sin ejecutar nada realmente

#### 2.2. Evidencia: make -d build

```console
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ make -d build
Se considera el archivo objetivo 'build'.
 El archivo 'build' no existe.
  Se considera el archivo objetivo 'out/hello.txt'.
    Se considera el archivo objetivo 'src/hello.py'.
    No es necesario reconstruir el objetivo 'src/hello.py'..
   Se terminaron las dependencias del archivo objetivo 'out/hello.txt'.
   La dependencia 'src/hello.py' es más reciente que el objetivo 'out/hello.txt'.
  Se debe reconstruir el objetivo 'out/hello.txt'.
mkdir -p out
python3 src/hello.py > out/hello.txt
  Se reconstruyó con éxito el archivo objetivo 'out/hello.txt'.
Se reconstruyó con éxito el archivo objetivo 'build'.
```
Make analiza dependencias con marcas de tiempo y detecta que `src/hello.py` es mas reciente que `out/hello.txt` por eso recompila

La linea **"Se debe reconstruir"** muestra la decision de rehacer el target
`mkdir -p $(@D)` asegura que exista el directorio de destino antes de escribir el archivo evitando errores si out no esta creado

De esta forma make mantiene consistencia entre fuentes y productos

#### 2.3. Fuerza un entorno con BSD tar en PATH y corre make tools; comprueba el fallo con "Se requiere GNU tar" y razona por qué --sort, --numeric-owner y --mtime son imprescindibles para reproducibilidad determinista
Actualmente trabajo con `pop-os` el cual usa `GNU tar` por defecto, por lo que `make tools` no genera problemas.

#### 2.4. Ejecuta make verify-repro; observa que genera dos artefactos y compara SHA256_1 y SHA256_2. Si difieren, hipótesis: zona horaria, versión de tar, contenido no determinista o variables de entorno no fijadas.
# Verificación de reproducibilidad (`make verify-repro`)

```console
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ make verify-repro
SHA256_1=6527269e88253fb573312386dda40e33d6d73b6bb28604510fec567afae70240
SHA256_2=6527269e88253fb573312386dda40e33d6d73b6bb28604510fec567afae70240
OK: reproducible
```

El objetivo verify-repro construye dos veces el mismo artefacto.

Luego calcula el hash SHA-256 de cada artefacto (SHA256_1 y SHA256_2).

Si los hashes coinciden, significa que la compilación es reproducible: el mismo código fuente, con las mismas dependencias, produce exactamente los mismos binarios.

Si los hashes difieren, posibles causas incluyen:

* Zona horaria distinta al crear archivos.

* Versión diferente de tar u otra herramienta.

* Metadatos no deterministas (p. ej. timestamps o UID/GID en archivos).

* Variables de entorno que no estén fijadas.

#### 2.5. Corre make clean && make all, cronometrando; repite make all sin cambios y compara tiempos y logs. Explica por qué la segunda es más rápida gracias a timestamps y relaciones de dependencia bien declaradas.
# Comparación de ejecuciones con make

En la primera ejecución se hizo make clean y luego make all al borrarse los objetos se tuvo que recompilar todo desde cero se ejecutaron los compiladores y el enlazador y por eso el tiempo fue un poco mayor  

En la segunda ejecución se volvió a correr make all pero sin cambios en el código make solo revisó los timestamps y detectó que todo estaba actualizado ya no fue necesario recompilar y solo verificó dependencias lo que hizo que el tiempo fuera menor  

La diferencia principal es que la primera vez se reconstruye completo mientras la segunda es más rápida gracias al uso de marcas de tiempo y relaciones de dependencia bien declaradas  

#### 2.6. Ejecuta PYTHON=python3.12 make test (si existe). Verifica con python3.12 --version y mensajes que el override funciona gracias a ?= y a PY="${PYTHON:-python3}" en el script; confirma que el artefacto final no cambia respecto al intérprete por defecto.
La ejecución con `PYTHON=python3.12 make test` mostró que el override funciona ya que los tests corrieron con Python 3.12.11 y pasaron igual que con el intérprete por defecto, confirmando que el artefacto final no cambia  

```console
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ PYTHON=python3.12 make test
python3.12 --version
scripts/run_tests.sh
Demostrando pipefail:
Sin pipefail: el pipe se considera exitoso (status 0).
Con pipefail: se detecta el fallo (status != 0).
Test pasó: Hello, World!
python3.12 -m unittest discover -s tests -v
test_greet (test_hello.TestGreet.test_greet) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
Python 3.12.11 
```
#### 2.7. Ejecuta make test; describe cómo primero corre scripts/run_tests.sh y luego python -m unittest. Determina el comportamiento si el script de pruebas falla y cómo se propaga el error a la tarea global.
La ejecución de `make test` primero llamó al script `scripts/run_tests.sh` donde se muestra el ejemplo de `pipefail` y un mensaje de prueba exitoso  
Después se ejecutó `python3 -m unittest discover -s tests -v` corriendo los tests de `unittest`. El resultado fue que el test `test_greet` pasó y se reportó `OK` con 1 test ejecutado  
Esto confirma que la tarea global combina el script de pruebas inicial y luego la suite de `unittest`. Si el script fallara, `make` marcaría la receta con error y no llegaría a ejecutar los tests de `unittest`, propagando el fallo al target `test`

### 3. EXTENDER

#### 3.1 `lint` mejorado
Inicializamos un cambio en la linea 33 de `run_tests.sh` y cambiamos a:
```bash
if ! command -v $dep >/dev/null 2>&1; then
```
EL siguiente paso es ejecutar `make lint`obteniendo los siguientes resultados:
```console
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ make lint
shellcheck scripts/run_tests.sh

In scripts/run_tests.sh line 33:
		if ! command -v $dep >/dev/null 2>&1; then
                                ^--^ SC2086 (info): Double quote to prevent globbing and word splitting.

Did you mean: 
		if ! command -v "$dep" >/dev/null 2>&1; then


In scripts/run_tests.sh line 56:
if false | true > /dev/null; then
           ^--------------^ SC2216 (warning): Piping to 'true', a command that doesn't read stdin. Wrong command or missing xargs?


In scripts/run_tests.sh line 60:
if false | true > /dev/null; then
           ^--------------^ SC2216 (warning): Piping to 'true', a command that doesn't read stdin. Wrong command or missing xargs?

For more information:
  https://www.shellcheck.net/wiki/SC2216 -- Piping to 'true', a command that ...
  https://www.shellcheck.net/wiki/SC2086 -- Double quote to prevent globbing ...
make: *** [Makefile:39: lint] Error 1
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ 
```

Finalmente luego de solucionar el problema ocasionado intensionalmente obtenemos:
```console
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ make lint
shellcheck scripts/run_tests.sh
shfmt -d scripts/run_tests.sh
ruff no instalado; omitiendo lint Python
```
##### Salida de `make lint`

- **shellcheck**: Pasó sin errores (sin output = éxito)
- **shfmt**: Formato correcto (sin diferencias = éxito)  
- **ruff**: No instalado (se omite como esperado)

**Estado**: Lint exitoso - El código Bash cumple con los estándares

#### 3.2 RollBack Adicional
Para esta parte, se añadira:
```bash
# Escribir ruta del temporal para pruebas
mkdir -p out
echo "$tmp" > out/tmp_path.txt
echo "Archivo temporal: $tmp"
echo "Pausa de 3 segundos para permitir borrado manual..."
sleep 3

# Chequeo adicional: si el temporal desaparece, fallamos
if [[ ! -f "$tmp" ]]; then
    echo "Error: archivo temporal perdido"
    exit 3
fi
```
En run_tests.sh para depuracion de archivos temporales, creando `out`, guardando `tmp_path.txt` y mostrando el archivo temporal en consola, finalmente un pausa para borrar el archivo manualmente y verificar que ya no existe

Finalmente obtenemos la siguiente salida:
```console
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ ./scripts/run_tests.sh
Demostrando pipefail:
Sin pipefail: el pipe se considera exitoso (status 0).
Con pipefail: se detecta el fallo (status != 0).
Archivo temporal: /tmp/tmp.xEGwfwQM9m
Pausa de 3 segundos para permitir borrado manual...
Test pasó: Hello, World!
```

#### 3.3 Incrementabilidad
Se ejecuta `make clean` y `make benchmark` el cual construira todo desde cero lint, build, test, package y se espera que el tiempo sea mas largo ya que se crean todos los archivos
```console
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ make clean
rm -rf out dist
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ make benchmark
rm -rf out dist
make[1]: Entering directory '/home/ject/Escritorio/DS/Actividad5-CC3S2'
shellcheck scripts/run_tests.sh
shfmt -d scripts/run_tests.sh
ruff no instalado; omitiendo lint Python
mkdir -p out
python3 src/hello.py > out/hello.txt
scripts/run_tests.sh
Demostrando pipefail:
Sin pipefail: el pipe se considera exitoso (status 0).
Con pipefail: se detecta el fallo (status != 0).
Archivo temporal: /tmp/tmp.Z0uChPDmYs
Pausa de 3 segundos para permitir borrado manual...
Test pasó: Hello, World!
python3 -m unittest discover -s tests -v
test_greet (test_hello.TestGreet) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
mkdir -p dist
tar --sort=name --owner=0 --group=0 --numeric-owner --mtime='UTC 1970-01-01' -czf dist/app.tar.gz -C out hello.txt
make[1]: Leaving directory '/home/ject/Escritorio/DS/Actividad5-CC3S2'

real	0m3.243s
user	0m0.170s
sys	0m0.075s
Benchmark completado. Resultados en: out/benchmark.txt
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ 
```
Cuando se modifica el timestamp de `src/hello.py` el tiempo es ligeramente mayor, ya que este cambio obliga al sistema a crear todo de nuevo.

#### 3.4 Checklist de Smoke-Tests - Bootstrap
Salida de comprobacion de comandos:
```console
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ chmod +x scripts/run_tests.sh
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ make tools
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ make help
  all           Construir, testear y empaquetar todo
  build         Generar out/hello.txt
  test          Ejecutar tests
  package       Crear dist/app.tar.gz
  lint          Lint Bash y (opcional) Python
  tools         Verificar dependencias
  check         Ejecutar lint y tests
  benchmark     Medir tiempo de ejecución
  format        Formatear scripts con shfmt
  dist-clean    Limpiar todo (incluye caches opcionales)
  verify-repro  Verificar que dist/app.tar.gz sea 100% reproducible
  clean         Limpiar archivos generados
  help          Mostrar ayuda
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ 
```
* `chmod +x scripts/run_tests.sh` Presenta un exito silencioso asignando todos los permisos necesarios al script
* `make tools` Presenta tambien exito silencioso, implicando que todas las dependencias estan instaladas
* `make help` Funciona correctamente -> muestra 12 objetivos disponibles con sus respectivas descripciones

#### 3.5 Checklist de Smoke-Tests - Primera pasada
```console
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$ make all
ls -l out/hello.txt dist/app.tar.gz
tar -tzf dist/app.tar.gz
shellcheck scripts/run_tests.sh
shfmt -d scripts/run_tests.sh
ruff no instalado; omitiendo lint Python
scripts/run_tests.sh
Demostrando pipefail:
Sin pipefail: el pipe se considera exitoso (status 0).
Con pipefail: se detecta el fallo (status != 0).
Archivo temporal: /tmp/tmp.oUzwbBQcLc
Pausa de 3 segundos para permitir borrado manual...
Test pasó: Hello, World!!
python3 -m unittest discover -s tests -v
test_greet (test_hello.TestGreet) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
-rw-rw-r-- 1 ject ject 126 sep 22 14:38 dist/app.tar.gz
-rw-rw-r-- 1 ject ject  15 sep 22 14:38 out/hello.txt
hello.txt
ject@pop-os:~/Escritorio/DS/Actividad5-CC3S2$
```
Verificacion exitosa
* **linting**: Shellcheck y shfmt pasaron sin errores
* **Tests**: script de prueba y unittest ejecutados correctamente
* **Build**: Archivo out/hello.txt generado (15 bytes)
* **Package**: dist/app.tar.gz creado (126 bytes) con solo hello.txt
* **Contenido**: Tar contiene unicamente el archivo esperado
