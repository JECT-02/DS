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

