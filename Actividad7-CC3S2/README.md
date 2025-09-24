# Actividad 7: Explorando estrategias de fusión en GIT

## 1. Fusión fast-forward
Un fast-forward en Git ocurre cuando una rama puede avanzar directamente al commit de otra sin crear un merge commit.  

- Requisitos: la rama actual debe estar detrás y sin commits propios.  
- Acción: mueve el puntero de la rama al último commit de la otra, manteniendo la historia lineal.  

## 2. Fusión No-Fast-Forward
Un no fast-forward (no ff) en Git ocurre cuando las ramas tienen commits diferentes y no es posible avanzar directamente  

- Requisitos: existe divergencia, la rama actual tiene commits que no están en la rama destino
- Acción: Git crea un commit de merge que une ambas historias
