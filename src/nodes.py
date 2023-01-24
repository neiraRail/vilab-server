from flask import Blueprint, jsonify


from src.models.node import Node


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
        return validacion["razon"]

    nodo = Node(**json)
    nodo.save()
    return jsonify(nodo.to_json())


def validar_nodo():
    return {"valido": True, "razon": None}
