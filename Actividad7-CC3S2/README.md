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
