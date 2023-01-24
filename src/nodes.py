from flask import Blueprint
from bson import json_util, ObjectId
from database import mongo

bp = Blueprint(
    "nodes",
    __name__,
)


@bp.route("/<id>", methods=(["GET"]))
def index(id):
    # {
    #     "ssid": "DRAGINO_IOT",
    #     "password": "Jota.2020",
    #     "serverREST": "http://200.13.5.47:8080/events",
    #     "node": id,
    #     "time_event": 2500,
    #     "delay_sensor": 200,
    #     "time_reset": 24,
    #     "token": "108160136",
    # }
    return json_util.dumps(mongo.db.nodes.find_one({"node": id}))


@bp.route("/", methods=(["POST"]))
def crear_nodo():
    node = request.json
    if not validar_nodo(node):
        return "Formato de json no válido"
    mongo.db.nodes.insert_one(node)
    return "OK"


def validar_nodo():
    return true
