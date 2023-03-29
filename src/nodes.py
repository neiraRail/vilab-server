from flask import Blueprint, jsonify, request
from src.models.node import Node
import logging


bp = Blueprint(
    "nodes",
    __name__,
)


@bp.route("/init", methods=(["POST"]))
def init():
    if not request.is_json:
        return "Request no contiene un Json", 400

    json = request.json
    if "node" not in json:
        return "json no contiene 'node'", 400
    if "start" not in json:
        return "json no contiene 'start'", 400

    if Node.objects(node=json["node"]).count() == 0:
        return "No se encontraron nodos", 404

    # Actualiza base de datos
    id_del_nodo = Node.objects(node=json["node"]).first().id
    Node.objects(id=id_del_nodo).update(set__start=json["start"])

    newconf = Node.objects(node=json["node"]).first().to_json()

    return jsonify(newconf)


@bp.route("/", methods=(["GET"]))
def get_nodes():
    logging.info("GET nodos/ request")
    nodos = Node.objects()
    return jsonify(nodos)


@bp.route("/<id>", methods=(["GET"]))
def get_node_by_id(id):
    logging.info("GET nodos/{} request".format(id))
    node = Node.objects(node=id).first()
    if not node:
        return jsonify({"error": "nodo no encontrado"}), 404
    else:
        return jsonify(node.to_json())


@bp.route("/", methods=(["POST"]))
def crear_nodo():
    logging.info("POST nodos/ request")
    json = request.json
    validacion = validar_nodo(json)
    if not validacion["valido"]:
        return validacion, 400

    nodo = Node(**json)
    nodo.save()
    return jsonify(nodo.to_json())


def validar_nodo(nodo):
    if type(nodo) is not dict:
        return {"valido": False, "razon": "El nodo no es un diccionario"}
    if not nodo:
        return {"valido": False, "razon": "El nodo es nulo"}
    keys = set(
        [
            "ssid",
            "password",
            "serverREST",
            "serverREST2",
            "node",
            "time_reset",
            "time_event",
            "delay_sensor",
            "batch_size",
            "token",
            "detail",
            "start",
        ]
    )
    diferencia = [x for x in keys if x not in nodo.keys()]
    if len(diferencia) != 0:
        return {
            "valido": False,
            "razon": "Al nodo le faltan los atributos: " + str(diferencia),
        }
    if not all(
        [type(value) is str or type(value) is int for key, value in nodo.items()]
    ):
        return {
            "valido": False,
            "razon": "Alguno de los atributos no son str ni int",
        }
    return {"valido": True, "razon": None}
