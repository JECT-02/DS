import os
import logging
from flask import Flask, jsonify

# Configurar logging para stdout (12-Factor)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    message = os.getenv('MESSAGE', 'Hola mundo')
    release = os.getenv('RELEASE', 'v0')
    logger.info(f"Acceso a la ruta / - Mensaje: {message}, Release: {release}")
    return jsonify({"message": message, "release": release})

@app.route('/health', methods=['GET'])
def health():
    logger.info("Health check realizado")
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    logger.info(f"Iniciando aplicación en puerto {port}")
    app.run(host='0.0.0.0', port=port)