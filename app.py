import logging
import time
import os
from flask import Flask
from flask_cors import CORS
from src.database import db as mongo
from src.events import bp as events_blueprint
from src.nodes import bp as nodes_blueprint

logging.basicConfig(
    filename="logs/vilab_server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
)

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(APP_ROOT, "files")

# Crear app con CORS y configuración de base de datos.
app = Flask(__name__)
CORS(app)
app.config["MONGODB_SETTINGS"] = {
    "db": "vibration_db",
    "host": "localhost",
    "port": 27017,
}

# Registrar los endpoints
app.register_blueprint(events_blueprint, url_prefix="/events")
app.register_blueprint(nodes_blueprint, url_prefix="/nodes")

# Iniciar la conexión con la base de datos.
mongo.init_app(app)


@app.route("/status")
def status():
    logging.info("GET status/ request")
    return {"estado": "1", "texto": "OK"}


if __name__ == "__main__":
    logging.info("Servidor funcionando")
    app.run(host="0.0.0.0", port=8080, debug=True)
    logging.info("Servidor finalizado")
