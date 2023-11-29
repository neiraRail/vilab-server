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
    protocol = db.StringField(default="http")

    def to_json(self):
        # Initialize an empty dictionary to store the JSON representation
        json_data = {}

        # Iterate through all the fields in the document
        for field_name, field_value in self._data.items():
            # Check if the field is not None (empty) before adding it to the JSON
            if field_name != "id" and field_value is not None:
                json_data[field_name] = field_value

        return json_data