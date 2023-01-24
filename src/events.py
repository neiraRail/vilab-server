from flask import Blueprint, jsonify, request
from datetime import datetime
import logging
import time

from src.models.event import Event

bp = Blueprint(
    "events",
    __name__,
)


@bp.route("/", methods=(["GET"]))
def get_events():
    logging.info("GET eventos/ request")
    eventos = Event.objects()
    return jsonify(eventos)


@bp.route("/<event>", methods=(["GET"]))
def get_event(event):
    logging.info("GET eventos/{} request".format(event))
    evento = Event.objects(event=event).first()
    if not evento:
        return jsonify({"error": "evento no encontrado"})
    else:
        return jsonify(evento.to_json())


@bp.route("/", methods=(["POST"]))
def create_event_jota():
    logging.info("POST eventos/ request")
    json = request.json
    json["time"] = time.mktime(datetime.now().timetuple())
    resultado = validar_vector(json)
    if not resultado["valido"]:
        return resultado
    event = Event(**json)
    event.save()
    return jsonify(event.to_json())


@bp.route("/<id>", methods=(["DELETE"]))
def delete_event(id):
    logging.info("DELETE eventos/{id} request".format(id))
    evento = Event.objects.get_or_404(id=id)
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
            "event",
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
    if set(vector.keys()) != keys:
        diferencia = [x for x in keys if x not in vector.keys()]
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
