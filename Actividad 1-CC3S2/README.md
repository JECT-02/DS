# Actividad 1 – Introducción a DevOps y DevSecOps
**Nombre:** Jhon Edmilson Cruz Tairo
**Fecha:** 27/08/2025  
**Tiempo total invertido (hh:mm):** 00:00  

**Contexto del entorno:** Trabajo en Linux Pop-OS, uso navegador Brave para inspeccionar HTTP/TLS y draw.io para diagramas. No se incluira datos sensibles

## 4.1 DevOps vs Cascada
**Cascada:** Es un enfoque secuencial y lineal para el desarrollo de software, con fases definidas (requisitos, diseño, implementacion, pruebas y despliegue). Es ideal para proyectos con requisitos estables, pero rigidos ante cambios, lo que puede elevar los costos y retrasos `Pressman 2004`

**DevOps:** DevOps en cambio , es una cultura de desarrollo `DEV` y operaciones `OPS`, promoviendo integraciones continuas conocido como (CI/CD), automatizacion y entregas rápidas. Se fomenta la colaboración, retroalimentacion y mejora iterativa, acelerando el time to market `Kim et al 2006`

| Comparativa | Cascada | DevOps |
|------|------|------|
| Estructura   | Lineal, por fases   | Ciclica y colaborativa  |
| Flexibilidad   | Baja, resiste cambios   | Alta, se adapta a cambios   |
| Velocidad   | Lenta en entornos dinamicos (actualidad)   | Rápida e iterativa   |

**IMAGEN COMPARATIVA:**
![](imagenes/devops-vs-cascada.png)

## 4.2 Ciclo tradicional y silos
### Limitaciones del ciclo "Construccion -> Operación"

Sin integracion continua, el ciclo tradicional se presenta de la siguiente manera:
1. **Grandes Lotes:** Entregas masivas de codigo elevan el **costo de integración tardia**, acumulando conflictos y defectos `Kim et al 2016`
2. **Colas de Defectos:** Los Handoffs sin retroalimentación generan asimetrias de información, restando la resolución y aumento de **MTTR**

### ANTI-PATRONES
1. **Throw Over The Wall:** Desarrolladores entregan software sin colaboración, causan retrabajos y degradaciones repetitivas por la falta de contexto.
2. **Seguridad Tardia:** Auditorias de seguridad al final del ciclo introducen volnurabilidades y retrasos que requieren correcciones costodsas.

<p align="center">
  <img src="imagenes/silos-equipos.png" alt="Texto alternativo">
</p>

## 4.3 Principios y Beneficios (CI/CD y Agile)
### CI/CD: Principios Clave
- **Integración Continua (CI)** implica cambios pequeños y frecuentes al codigo, integrados automaticamente con pruebas cercanas al desarrollo `Pressman 2014` **Despliegue Continuo (CD)** automatizado la entrega a entornos de prueba a producción lo que asegura despliegues rápidosy confiables, ambos promueven colaboración DevOps reduciendo asimetrias de informacion mediante retroalimentaciónconstante y automatización `Kim et al 2016`

### Agile como Precursor
- Practicas Agile, como **Reuniones Diarias** y **Retrospectiva**, alimentan el pipeline CI/CD. Las diarias identifican con antelación cuellos de botella, priorizando que cambios promover o bloquear. Las retrospectivas analizan fallos, ajustando pruebas automatizadas para prevenir defectos recurrentes, fortaleciendo la calidad de nuestro despliegue

### Indicador de Colaboración
* **Indicador propuesto:** Tiempo desde el pull request listo hasta despliegues de prueba. Mide la fluidez entre Dev y Ops reflejando colaboración efectiva. Un tiempo reducido indica menos fricciones y mejor alineación.
* **Recolección sin herramientas pagas:**
* **Bitácoras:** Usar logs de sistema de control de versiones (Git) para registrar timestamps de PRs creados y aprobados
* **Metadatos dePRs:** Extraer fechas de aprobación y merge desde plataformas como GitHub (API pública gratuita)
* **Registro de despliegue:** Analizar logs de servidores (jenkings, scripts bash) para marcar el momento de despliegue en pruebas

