from src.database import db


class Node(db.Document):
    node = db.IntField()
    ssid = db.StringField()
    password = db.StringField()
    serverREST = db.StringField()
    serverREST2 = db.StringField()
    time_reset = db.IntField()
    time_event = db.IntField()
    delay_sensor = db.IntField()
    batch_size = db.IntField()
    token = db.StringField()
    detail = db.StringField()

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
        }
