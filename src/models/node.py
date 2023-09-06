from src.database import db


class Node(db.DynamicDocument):
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
        data = {}
        for field_name in self._fields:
            # Use getattr to retrieve the value of the field
            field_value = getattr(self, field_name, None)
            data[field_name] = field_value
        return data
    
    
