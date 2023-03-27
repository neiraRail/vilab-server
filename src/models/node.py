from src.database import db


class Node(db.Document):
    node = db.IntField()
    ssid = db.StringField()
    password = db.StringField()
    serverREST = db.StringField()
    serverREST2 = db.StringField()
    time_event = db.IntField()
    delay_sensor = db.IntField()
    time_reset = db.IntField()
    token = db.StringField()

    def to_json(self):
        return {
            "ssid": self.ssid,
            "password": self.password,
            "serverREST": self.serverREST,
            "node": self.node,
            "time_event": self.time_event,
            "delay_sensor": self.delay_sensor,
            "time_reset": self.time_event,
            "token": self.token,
        }
