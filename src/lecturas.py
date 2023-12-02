import json
from flask import Blueprint, jsonify, request
from datetime import datetime
import time
import logging
from mongoengine.errors import NotUniqueError, ValidationError, FieldDoesNotExist

from src.models.lectura import Lectura
from src.procesado import baseProceso

bp = Blueprint(
    "lectura",
    __name__,
)

@bp.route("", methods=(["POST"]))
def recieve_lectura_http():
    json_data = request.json
    reloj = time.perf_counter_ns()
    # resultado = validar_vector(json_data)
    # if not resultado["valido"]:
    #     return resultado, 400
    try:
        event = Lectura(**json_data)
        event.validate()
        event.save()
    except FieldDoesNotExist as e:
        return jsonify({"valido": "false", "razon": str(e)}), 400
    except ValidationError as e:
        return jsonify({"valido": "false", "razon": e.to_dict()}), 400
    except NotUniqueError as e:
        return jsonify({"valido": "false", "razon": str(e)}), 400
    # logging.info(json)
    # baseProceso.procesar_segun_config(event)
    logging.info("delta: {}".format(json_data["delta"]))
    # logging.info( "Tiempo de ejecución: {}".format( time.perf_counter_ns()-reloj))
    return jsonify(event.to_json())


def recieve_lectura_udp(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        reloj = time.perf_counter_ns()

        # Convert bytes to JSON
        json_data = json.loads(data.decode())
        # resultado = validar_vector(json_data)
        # if not resultado["valido"]:
        #     logging.info(resultado)
        #     continue
        # Serialize using mongoengine and save to MongoDB
        try:
            event = Lectura(**json_data)
            event.validate()
            event.save()
        except FieldDoesNotExist as e:
            return jsonify({"valido": "false", "razon": str(e)}), 400
        except ValidationError as e:
            return jsonify({"valido": "false", "razon": e.to_dict()}), 400
        except NotUniqueError as e:
            return jsonify({"valido": "false", "razon": str(e)}), 400
        
        # baseProceso.procesar_segun_config(json_data)
        logging.info("delta: {}".format(json_data["delta"]))
        # logging.info( "Tiempo de ejecución: {}".format( time.perf_counter_ns()-reloj))
        print(f"Saved data from {addr}")

# def recieve_lectura_tcp(conn, addr):
#     while True:
#         reloj = time.perf_counter_ns()
#         data = conn.recv(1024)

#         if not data:
#             break

#         # Convert bytes to JSON
#         json_data = json.loads(data.decode())
#         resultado = validar_vector(json_data)
#         if not resultado["valido"]:
#             logging.info(resultado)
#             continue
#         # Serialize using mongoengine and save to MongoDB
#         lectura = Lectura(**json_data)
#         print(lectura.to_json())
#         lectura.save()
        
#         baseProceso.procesar_segun_config(json_data)

#         logging.info( "Tiempo de ejecución: {}".format( time.perf_counter_ns()-reloj))
#         print(f"Saved data from {addr}")

def recieve_lectura_mqtt(client, userdata, msg):
    reloj = time.perf_counter_ns()
    json_data = json.loads(msg.payload.decode())
    # resultado = validar_vector(json_data)
    # if not resultado["valido"]:
    #     logging.info(resultado)
    #     return
    
    try:
        event = Lectura(**json_data)
        event.validate()
        event.save()
    except FieldDoesNotExist as e:
        return jsonify({"valido": "false", "razon": str(e)}), 400
    except ValidationError as e:
        return jsonify({"valido": "false", "razon": e.to_dict()}), 400
    except NotUniqueError as e:
        return jsonify({"valido": "false", "razon": str(e)}), 400

    # baseProceso.procesar_segun_config(json_data)
    logging.info("delta: {}".format(json_data["delta"]))
    # logging.info( "Tiempo de ejecución: {}".format( time.perf_counter_ns()-reloj))

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


# def validar_vector(vector):
#     if type(vector) is not dict:
#         return {"valido": False, "razon": "El vector no es un diccionario"}
#     if not vector:
#         return {"valido": False, "razon": "El vector es nulo"}
#     keys = set(
#         [
#             "delta",
#             "time",
#             "node",
#             "acc_x",
#             "acc_y",
#             "acc_z",
#             "gyr_x",
#             "gyr_y",
#             "gyr_z",
#             "mag_x",
#             "mag_y",
#             "mag_z",
#             "temp",
#         ]
#     )
#     # keys = set(["node", "event"])
#     diferencia = [x for x in keys if x not in vector.keys()]
#     if len(diferencia) != 0:
#         return {
#             "valido": False,
#             "razon": "Al vector le faltan los atributos: " + str(diferencia),
#         }
#     if not all(
#         [type(value) is float or type(value) is int for key, value in vector.items()]
#     ):
#         return {
#             "valido": False,
#             "razon": "Alguno de los atributos no son float ni int",
#         }
#     return {"valido": True, "razon": None}
