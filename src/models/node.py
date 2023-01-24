from src.database import db


class Node(db.Document):
    ssid = db.StringField()
    password = db.StringField()
    serverREST = db.StringField()
    node = db.IntField()
    time_event = db.IntField()
    delay_sensor = db.IntField()
    time_reset = db.IntField()
    token = db.StringField()

    def to_json():
        return {
            "ssid": db.StringField(),
            "password": db.StringField(),
            "serverREST": db.StringField(),
            "node": db.IntField(),
            "time_event": db.IntField(),
            "delay_sensor": db.IntField(),
            "time_reset": db.IntField(),
            "token": db.StringField(),
        }
