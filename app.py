from flask import Flask, request
from werkzeug.utils import secure_filename
from datetime import datetime
import logging
import time
import os


from src.database import db as mongo
from src.events import bp as events_blueprint
from src.nodes import bp as nodes_blueprint

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(APP_ROOT, "files")

# logging.getLogger('werkzeug').disabled = True
logging.basicConfig(
    filename="logs/vilab_server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
)

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {
    "db": "vibration_db",
    "host": "172.17.0.1",
    "port": 27017,
}
# app.config["MONGO_URI"] = "mongodb://localhost:27017/vibration_db"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.register_blueprint(events_blueprint, url_prefix="/events")
app.register_blueprint(nodes_blueprint, url_prefix="/nodes")

mongo.init_app(app)


@app.route("/status")
def status():
    logging.info("GET status/ request")
    return {"estado": "1", "texto": "OK"}


@app.route("/time")
def time_unix():
    d = datetime.now()
    return {"time": time.mktime(d.timetuple())}


@app.route("/events_old", methods=(["POST"]))
def create_event():
    logging.info("POST events_old/ request")
    event = request.json
    if not validar_evento_old(event):
        return "Formato de json no válido"

    mongo.db[event["filename"]].delete_many({})
    mongo.db[event["filename"]].insert_many(event["data"])

    # with open(
    #     os.path.join(app.config["UPLOAD_FOLDER"], event["filename"]), "w"
    # ) as myfile:
    #     for data in event["data"]:
    #         myfile.write(str(data))
    #         myfile.write("\n")
    return "Ingresados {} registros".format(len(event["data"]))


@app.route("/files", methods=(["POST"]))
def save_file():
    logging.info("POST files/ request")
    # Checkear si la petición tiene el archivo.
    if len(request.files) == 0:
        logging.info("files/ : Largo de request.files es igual a 0")
        return "No hay archivo"
    file = list(request.files.values())[0]
    # Hay casos en que se se envía un archivo vacío sin un filename
    if file.filename == "":
        logging.info("files/ : file.filename está vacío")
        return "No hay archivo"
    logging.info("Hay un archivo de nombre: {}".format(file.filename))
    if allowed_file(file.filename):
        logging.info("La extensión del archivo es aceptada")
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return "Archivo guardado en {}".format(
            os.path.join(app.config["UPLOAD_FOLDER"], filename)
        )
    else:
        logging.info("La extensión del archivo no está permitida")
        return "Extensión no permitida"


ALLOWED_EXTENSIONS = ["txt", "json"]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validar_evento_old(evento):
    if type(evento) is not dict:
        return False
    if "filename" not in evento:
        return False
    if "data" not in evento:
        return False
    if type(evento["data"]) is not list:
        return False
    if len(evento["data"]) == 0:
        return False
    if type(evento["filename"]) is not str:
        return False

    for vector in evento["data"]:
        if not validar_vector_old(vector):
            return False
    return True


def validar_vector_old(vector):
    if type(vector) is not dict:
        return False
    if not vector:
        return False
    if set(vector.keys()) != set(
        ["time", "acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z", "temp"]
    ):
        return False
    if not all([type(value) is float for key, value in vector.items()]):
        return False
    return True


if __name__ == "__main__":
    logging.info("Servidor funcionando")
    app.run(host="0.0.0.0", port=8080, debug=True)
    logging.info("Servidor finalizado")
