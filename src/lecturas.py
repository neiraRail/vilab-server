from flask import Blueprint, jsonify, request
from datetime import datetime
import time
import logging

from src.models.lectura import Lectura

bp = Blueprint(
    "lectura",
    __name__,
)

@bp.route("", methods=(["POST"]))
def create_event_jota():
    reloj = time.perf_counter_ns()
    json = request.json
    resultado = validar_vector(json)
    if not resultado["valido"]:
        return resultado, 400
    event = Lectura(**json)
    event.save()
    # logging.info(json)
    logging.info( "Tiempo de ejecución: {}".format( time.perf_counter_ns()-reloj))
    return jsonify(event.to_json())


@bp.route("", methods=(["GET"]))
def get_events():
    eventos = Lectura.objects()
    return jsonify(eventos)



@bp.route("/node/<node>", methods=(["GET"]))
def get_all_by_node(node):
    logging.info("GET events/node/{} request".format(node))
    pipeline = [
        {"$match": {"node": int(node)}},
        {"$sort": {"time": 1}},
        {"$group": {"_id": "$event", "time": {"$first": "$time"}}},
        {"$project": {"_id": 0, "event": "$_id", "time": 1}},
    ]

    eventos = list(Lectura.objects.aggregate(pipeline))
    if not eventos:
        return jsonify({"error": "nodo no encontrado"}), 404
    else:
        return jsonify(eventos)


@bp.route("/node/<node>/event/<event>", methods=(["GET"]))
def get_all_by_event(node, event):
    logging.info("GET events/node/{}/event/{}".format(node, event))
    eventos = Lectura.objects(node=node, event=event).order_by("time")
    if not eventos:
        return jsonify({"error": "evento no encontrado"}), 404
    else:
        return jsonify(eventos)



@bp.route("/<id>", methods=(["DELETE"]))
def delete_event(id):
    logging.info("DELETE eventos/{} request".format(id))
    evento = Lectura.objects.get_or_404(id=id)
    evento.delete()
    return jsonify(evento.to_json())


def validar_vector(vector):
    if type(vector) is not dict:
        return {"valido": False, "razon": "El vector no es un diccionario"}
    if not vector:
        return {"valido": False, "razon": "El vector es nulo"}
    keys = set(
        [
            "time_lap",
            "time",
            "node",
            "acc_x",
            "acc_y",
            "acc_z",
            "gyr_x",
            "gyr_y",
            "gyr_z",
            "mag_x",
            "mag_y",
            "mag_z",
            "temp",
        ]
    )
    # keys = set(["node", "event"])
    diferencia = [x for x in keys if x not in vector.keys()]
    if len(diferencia) != 0:
        return {
            "valido": False,
            "razon": "Al vector le faltan los atributos: " + str(diferencia),
        }
    if not all(
        [type(value) is float or type(value) is int for key, value in vector.items()]
    ):
        return {
            "valido": False,
            "razon": "Alguno de los atributos no son float ni int",
        }
    return {"valido": True, "razon": None}
