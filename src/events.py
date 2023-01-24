from flask import Blueprint
from database import mongo
from datetime import datetime
from bson import json_util, ObjectId
import logging

bp = Blueprint(
    "events",
    __name__,
)


@bp.route("/", methods=(["GET"]))
def get_events():
    logging.info("GET events/ request")
    events = json_util.dumps(mongo.db.events.find())
    return events


@bp.route("/<id>", methods=(["GET"]))
def get_event(id):
    logging.info("GET events/{} request".format(id))
    return json_util.dumps(mongo.db.events.find_one({"_id": ObjectId(id)}))


@bp.route("/", methods=(["POST"]))
def create_event_jota():
    logging.info("POST events/ request")
    event = request.json
    event["time"] = str(datetime.now())
    if not validar_vector(event):
        return "Formato de json no válido"

    mongo.db.datos.insert_one(event)
    return "ok"


@bp.route("/", methods=(["DELETE"]))
def delete_event():
    mongo.db.events.remove({})
    return "deleted"


def validar_vector(vector):
    print(vector)
    if type(vector) is not dict:
        return False
    if not vector:
        return False
    if set(vector.keys()) != set(
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
    ):
        return False
    if not all(
        [
            type(value) is float or type(value) is int
            for key, value in vector.items()
            if key != "time"
        ]
    ):
        return False
    if type(vector["time"]) is not str:
        return False
    return True
