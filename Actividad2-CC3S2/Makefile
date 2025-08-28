.PHONY: run check-http check-tls check-dns setup clean logs

# Variables
APP_PORT ?= 8080
APP_MESSAGE ?= "Hola CC3S2"
APP_RELEASE ?= "v1"

run:
	PORT=$(APP_PORT) MESSAGE=$(APP_MESSAGE) RELEASE=$(APP_RELEASE) python3 app.py

check-http:
	curl -v http://127.0.0.1:8080/

check-tls:
	curl -k https://miapp.local/

check-dns:
	dig +short miapp.local
	getent hosts miapp.local

check-ports:
	sudo ss -ltnp | grep -E ':(443|8080)'

setup:
	@echo "Instalando dependencias..."
	sudo apt update
	sudo apt install -y python3 python3-pip python3-venv nginx curl dnsutils net-tools openssl
	@echo "Configurando entorno virtual..."
	python3 -m venv venv
	./venv/bin/pip install flask
	@echo "Configurando hosts..."
	echo "127.0.0.1 miapp.local" | sudo tee -a /etc/hosts
	@echo "Generando certificados TLS..."
	sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout /etc/ssl/private/miapp.key \
		-out /etc/ssl/certs/miapp.crt \
		-subj "/CN=miapp.local" \
		-addext "subjectAltName = DNS:miapp.local"
	sudo chmod 600 /etc/ssl/private/miapp.key
	@echo "Configurando Nginx..."
	sudo cp nginx-config /etc/nginx/sites-available/miapp
	sudo ln -sf /etc/nginx/sites-available/miapp /etc/nginx/sites-enabled/
	sudo nginx -t
	sudo systemctl restart nginx
	@echo "Setup completado!"

logs:
	sudo tail -f /var/log/nginx/error.log /var/log/nginx/access.log

clean:
	sudo rm -f /etc/nginx/sites-enabled/miapp
	sudo sed -i '/miapp.local/d' /etc/hosts
	sudo systemctl restart nginx
	@echo "Limpieza completada!"