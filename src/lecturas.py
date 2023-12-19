import json
from flask import Blueprint, jsonify, request
from datetime import datetime
import time
import logging
from mongoengine.errors import NotUniqueError, ValidationError, FieldDoesNotExist
from threading import Thread

from src.models.lectura import Lectura
from src.procesado import baseProceso
from src.executor import executor

bp = Blueprint(
    "lectura",
    __name__,
)

def guardarLectura(json_data, isHttp):
    try:
        event = Lectura(**json_data)
        event.validate()
        event.save()
    except FieldDoesNotExist as e:
        logging.error(e)
        if isHttp:
            return jsonify({"valido": "false", "razon": str(e)}), 400
    except ValidationError as e:
        logging.error(e)
        if isHttp:
            return jsonify({"valido": "false", "razon": e.to_dict()}), 400
    except NotUniqueError as e:
        logging.error(e)
        if isHttp:
            return jsonify({"valido": "false", "razon": str(e)}), 400
    
    logging.info("delta: {}".format(json_data["delta"]))
    if isHttp:
        return jsonify(event.to_json())

def guardarBatch(json_data, isHttp):
    try:
        logging.info("Se recibió un batch")
        logging.info("batch_id: {}".format(str(json_data["id"])+"/"+str(json_data["batch"][0]["start"])))
        logging.info("len: {}".format(json_data["len"]))
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
        if isHttp:
            executor.submit(baseProceso.procesar_segun_config, identifier)
        else:
            Thread(target=baseProceso.procesar_segun_config, args=(identifier,)).start()
        logging.info("delta: {}".format(json_data["batch"][1]["delta"]))
    except FieldDoesNotExist as e:
        logging.error(e)
        if isHttp:
            return jsonify({"valido": "false", "razon": str(e)}), 400
    except ValidationError as e:
        logging.error(e)
        if isHttp:
            return jsonify({"valido": "false", "razon": e.to_dict()}), 400
    except NotUniqueError as e:
        logging.error(e)
        if isHttp:
            return jsonify({"valido": "false", "razon": str(e)}), 400
    except Exception as e:
        logging.error(e)
        if isHttp:
            return jsonify({"valido": "false", "razon": str(e)}), 400
    if isHttp:
        return jsonify(True)

@bp.route("", methods=(["POST"]))
def recieve_lectura_http():
    try:
        json_data = request.json
        if "batch" in json_data:
            return guardarBatch(json_data, True)
        else:
            return guardarLectura(json_data, True)
    except Exception as e:
        logging.error(e)
        return jsonify({"valido": "false", "razon": str(e)}), 400


def recieve_lectura_udp(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            # reloj = time.perf_counter_ns()
            # Convert bytes to JSON
            logging.info("Recieved message from UDP client")
            json_raw = data.decode()

            #If the message does not ends in "]}" wait for another package and append it
            while json_raw[-2:] != "]}":
                data, addr = sock.recvfrom(1024)
                json_raw += data.decode()
            logging.info(json_raw)
            
            json_data = json.loads(json_raw)
            if "batch" in json_data:
                response = guardarBatch(json_data, False)
            else:
                response = guardarLectura(json_data, False)
        except Exception as e:
            logging.error(e)


def recieve_lectura_mqtt(client, userdata, msg):
    try:
        # reloj = time.perf_counter_ns()
        json_data = json.loads(msg.payload.decode())
        if "batch" in json_data:
            guardarBatch(json_data, False)
        else:
            guardarLectura(json_data, False)
    except Exception as e:
        logging.error(e)


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