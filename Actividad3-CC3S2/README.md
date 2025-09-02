# Actividad 3: Integración de DevOps y DevSecOps con HTTP, DNS, TLS y 12-Factor App

## Parte Teórica

### 1. Introducción a DevOps: ¿Qué es y qué no es?

**DevOps** es una filosofía, cultura y conjunto de prácticas que busca integrar desarrollo (Dev) y operaciones (Ops) para acelerar la entrega de software de calidad mediante colaboración, automatización y feedback continuo. Desde el código hasta la producción, DevOps abarca la escritura de código, pruebas automatizadas, integración continua (CI), despliegue continuo (CD) y monitoreo en producción. A diferencia del modelo **waterfall**, que divide el desarrollo en fases secuenciales (requisitos, diseño, desarrollo, pruebas, despliegue), DevOps promueve ciclos cortos y entregas incrementales, reduciendo el tiempo entre idea y producción.

**Qué no es DevOps**:
- **No es solo herramientas**: Aunque usa herramientas como Git, Jenkins o Docker, DevOps es principalmente cultural.
- **No elimina Ops**: No reemplaza a los equipos de operaciones, sino que fomenta colaboración.
- **No es caos sin procesos**: Implica disciplina, como gates de calidad para garantizar estabilidad.

**"You build it, you run it"** en el laboratorio significa que el equipo que desarrolla la aplicación (app.py) también es responsable de su despliegue y monitoreo (Nginx, systemd). Por ejemplo, el Makefile podría incluir tareas para pruebas unitarias (`pytest`), linting (`flake8`) y despliegue (`systemctl reload nginx`), asegurando que los desarrolladores gestionen el ciclo completo.

**Mitos vs Realidades**:
- **Mito**: DevOps es solo automatización con herramientas. **Realidad**: El marco **CALMS** (Culture, Automation, Lean, Measurement, Sharing) enfatiza la cultura y la colaboración. Por ejemplo, el laboratorio usa automatización (Makefile), pero requiere comunicación para alinear equipos.
- **Mito**: DevOps elimina la necesidad de procesos. **Realidad**: Introduce gates de calidad, como verificar coverage de pruebas en el Makefile antes de un despliegue (`make test-coverage`).
- **Ejemplo de gate de calidad en Makefile**:
```makefile
test-coverage:
    pytest --cov=app --cov-report=xml --cov-fail-under=80
```
Este gate asegura que el coverage de pruebas sea ≥80% antes de permitir un despliegue.

### 2. Marco CALMS en acción

**CALMS** (Culture, Automation, Lean, Measurement, Sharing) es un marco para evaluar prácticas DevOps. A continuación, se describe cada pilar y su relación con el laboratorio:

- **Culture**: Fomenta colaboración entre equipos. En el laboratorio, la configuración de Nginx y systemd requiere que desarrolladores y operaciones acuerden puertos y procesos, evitando silos.
  - **Ejemplo**: El archivo `app.py` expone un endpoint `/health` que ambos equipos usan para monitorear.
- **Automation**: Automatiza tareas repetitivas. El Makefile incluye tareas como `make build` (construir la app), `make test` (ejecutar pruebas) y `make deploy` (desplegar con systemd).
  - **Ejemplo**: 
    ```makefile
    deploy:
        sudo systemctl restart myapp
    ```
- **Lean**: Optimiza procesos para eliminar desperdicio. El laboratorio usa Netplan para configurar redes eficientemente, evitando configuraciones manuales propensas a errores.
  - **Ejemplo**: Archivo Netplan (`/etc/netplan/01-netcfg.yaml`) define IPs estáticas para consistencia.
- **Measurement**: Mide el desempeño para mejorar. El endpoint `/health` en `app.py` permite monitorear la salud de la aplicación, integrable con herramientas como Prometheus.
  - **Ejemplo**: 
    ```python
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"})
    ```
- **Sharing**: Promueve compartir conocimientos. El laboratorio carece de runbooks, pero se podría extender con un archivo Markdown (`runbook.md`) que documente pasos para recuperación ante fallos (ej. reiniciar Nginx).
  - **Propuesta de runbook**:
    ```markdown
    # Runbook: Recuperación de fallo en Nginx
    1. Verificar logs: `sudo journalctl -u nginx`
    2. Reiniciar servicio: `sudo systemctl restart nginx`
    3. Probar endpoint: `curl http://localhost/health`
    ```

**Extensión de Sharing**: Crear un postmortem tras un fallo (ej. puerto ocupado). Documentar en equipo causas, impacto y mitigaciones en un archivo `postmortem.md`.

### 3. Visión cultural de DevOps y paso a DevSecOps

**Colaboración en DevOps** evita silos al alinear desarrolladores, operaciones y seguridad. En el laboratorio, configurar Nginx (`/etc/nginx/sites-available/myapp`) requiere que desarrolladores definan endpoints y operaciones aseguren puertos abiertos (ej. 80, 443). **DevSecOps** integra seguridad desde el diseño hasta producción, como configurar cabeceras TLS en Nginx o escanear dependencias en CI/CD.

**Escenario retador: Fallo de certificado TLS**
- **Problema**: El certificado TLS expira, causando errores HTTPS.
- **Mitigación cultural**:
  1. **Colaboración**: Equipo de seguridad notifica a desarrolladores y operaciones via Slack.
  2. **Automatización**: Configurar un job CI/CD para renovar certificados con Let’s Encrypt (`certbot`).
  3. **Sharing**: Documentar el fallo en un postmortem y actualizar el runbook.
- **Solución técnica**:
  ```bash
  sudo certbot renew
  sudo systemctl reload nginx
  ```

**Tres controles de seguridad sin contenedores y su lugar en CI/CD**:
1. **Escaneo de dependencias** (ej. `pip-audit`): En CI, antes de construir la app, verificar vulnerabilidades en `requirements.txt`.
   - **Ejemplo**: 
     ```bash
     pip-audit -r requirements.txt
     ```
2. **Cabeceras de seguridad en Nginx**: Configurar HSTS y CSP en `/etc/nginx/sites-available/myapp`.
   - **Ejemplo**:
     ```nginx
     add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
     add_header Content-Security-Policy "default-src 'self'";
     ```
   - **CI/CD**: Verificar cabeceras en pruebas de integración (`curl -I https://myapp`).
3. **Restricción de puertos en Netplan**: Limitar acceso a puertos específicos (ej. 443) en `/etc/netplan/01-netcfg.yaml`.
   - **CI/CD**: Validar configuración de red antes de despliegue con un script (`netplan try`).

### 4. Metodología 12-Factor App

La metodología **12-Factor App** define principios para aplicaciones modernas. A continuación, se analizan 4 factores y su implementación en el laboratorio:

1. **Config por entorno**:
   - **Implementación**: Las variables de entorno (ej. `PORT`, `DB_URL`) se definen en `/etc/systemd/system/myapp.service`:
     ```ini
     [Service]
     Environment="PORT=8080"
     Environment="DB_URL=postgresql://user:pass@localhost/db"
     ```
   - **Fallo**: Si `app.py` tiene configuraciones hardcodeadas, viola este principio. **Mejora**: Usar `os.getenv` en `app.py`:
     ```python
     import os
     port = int(os.getenv('PORT', 8080))
     ```

2. **Port binding**:
   - **Implementación**: `app.py` se liga a un puerto dinámico (`PORT`) servido por Nginx como proxy inverso.
     ```python
     app.run(host='0.0.0.0', port=port)
     ```
   - **Fallo**: Si el puerto está hardcodeado, no es portable. **Mejora**: Validar `PORT` en CI/CD.

3. **Logs como flujos**:
   - **Implementación**: Los logs de `app.py` se envían a stdout y capturados por systemd (`journalctl -u myapp`).
   - **Fallo**: Si `app.py` escribe logs a un archivo, viola este principio. **Mejora**: Usar `print` o `logging` a stdout:
     ```python
     import logging
     logging.basicConfig(level=logging.INFO)
     logging.info("Application started")
     ```

4. **Statelessness (ausencia de estado)**:
   - **Implementación**: `app.py` no debería almacenar estado localmente, sino usar un backing service como PostgreSQL.
   - **Reto**: Si `app.py` usa variables globales para estado, no es stateless. **Mejora**: Usar una base de datos externa:
     ```python
     from sqlalchemy import create_engine
     engine = create_engine(os.getenv('DB_URL'))
     ```
   - **Backing services**: Configurar PostgreSQL como servicio externo, accesible via `DB_URL`.

**Mejora general**: Auditar `app.py` para eliminar configuraciones hardcodeadas y agregar un endpoint `/metrics` para monitoreo, integrable con Prometheus.