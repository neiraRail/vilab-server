from flask import Blueprint, jsonify, request
from src.models.node import Node
import logging


bp = Blueprint(
    "nodes",
    __name__,
)


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
        return jsonify({"error": "nodo no encontrado"})
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
            "node",
            "time_event",
            "delay_sensor",
            "time_reset",
            "token",
        ]
    )
    if set(nodo.keys()) != keys:
        diferencia = [x for x in keys if x not in nodo.keys()]
        return {
            "valido": False,
            "razon": "Al vector le faltan los atributos: " + str(diferencia),
        }
    if not all(
        [type(value) is str or type(value) is int for key, value in nodo.items()]
    ):
        return {
            "valido": False,
            "razon": "Alguno de los atributos no son str ni int",
        }
    return {"valido": True, "razon": None}
