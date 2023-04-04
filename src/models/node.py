from src.database import db


class Node(db.Document):
    node = db.IntField(required=True, unique=True)
    ssid = db.StringField(required=True)
    password = db.StringField(required=True)
    serverREST = db.StringField(required=True)
    serverREST2 = db.StringField(required=True)
    time_reset = db.IntField(default=24)
    time_event = db.IntField()
    delay_sensor = db.IntField(default=100)
    batch_size = db.IntField()
    token = db.StringField()
    detail = db.StringField(required=True)
    start = db.IntField(default=0)
    active = db.IntField(default=0)

    def to_json(self):
        return {
            "node": self.node,
            "ssid": self.ssid,
            "password": self.password,
            "serverREST": self.serverREST,
            "serverREST2": self.serverREST2,
            "time_reset": self.time_reset,
            "time_event": self.time_event,
            "delay_sensor": self.delay_sensor,
            "batch_size": self.batch_size,
            "token": self.token,
            "detail": self.detail,
            "start": self.start,
            "active": self.active,
        }
