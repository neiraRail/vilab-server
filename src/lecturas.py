import json
from flask import Blueprint, jsonify, request
from datetime import datetime
import time
import logging
from mongoengine.errors import NotUniqueError, ValidationError, FieldDoesNotExist

from src.models.lectura import Lectura
from src.procesado import baseProceso
from src.executor import executor

bp = Blueprint(
    "lectura",
    __name__,
)

def guardarLectura(json_data):
    try:
        event = Lectura(**json_data)
        event.validate()
        event.save()
    except FieldDoesNotExist as e:
        logging.errir(e)
        return jsonify({"valido": "false", "razon": str(e)}), 400
    except ValidationError as e:
        logging.errir(e)
        return jsonify({"valido": "false", "razon": e.to_dict()}), 400
    except NotUniqueError as e:
        logging.errir(e)
        return jsonify({"valido": "false", "razon": str(e)}), 400
    
    logging.info("delta: {}".format(json_data["delta"]))
    return jsonify(event.to_json())

def guardarBatch(json_data):
    logging.info("Se recibió un batch")
    logging.info("batch_id: {}".format(str(json_data["id"])+"/"+str(json_data["batch"][0]["start"])))
    logging.info("len: {}".format(json_data["len"]))
    try:
        for data in json_data["batch"]:
            event = Lectura(**data)
            event.validate()
            event.save()
        
        # Procesar batch
        identifier = {
            "node": json_data["batch"][0]["node"],
            "start": json_data["batch"][0]["start"],
            "batch_id": json_data["id"],
            "batch": json_data["batch"]
        }
        executor.submit(baseProceso.procesar_segun_config, identifier)
    except FieldDoesNotExist as e:
        logging.errir(e)
        return jsonify({"valido": "false", "razon": str(e)}), 400
    except ValidationError as e:
        logging.errir(e)
        return jsonify({"valido": "false", "razon": e.to_dict()}), 400
    except NotUniqueError as e:
        logging.errir(e)
        return jsonify({"valido": "false", "razon": str(e)}), 400
    
    logging.info("delta: {}".format(json_data["batch"][1]["delta"]))
    return jsonify(True)

@bp.route("", methods=(["POST"]))
def recieve_lectura_http():
    json_data = request.json
    if "batch" in json_data:
        return guardarBatch(json_data)
    else:
        return guardarLectura(json_data)


def recieve_lectura_udp(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        # reloj = time.perf_counter_ns()

        # Convert bytes to JSON
        json_data = json.loads(data.decode())
        if "batch" in json_data:
            guardarBatch(json_data)
        else:
            guardarLectura(json_data)


def recieve_lectura_mqtt(client, userdata, msg):
    # reloj = time.perf_counter_ns()
    json_data = json.loads(msg.payload.decode())
    if "batch" in json_data:
        guardarBatch(json_data)
    else:
        guardarLectura(json_data)


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