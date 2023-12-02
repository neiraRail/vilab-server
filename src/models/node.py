from src.database import db
from src.models.operacion import Operacion


class Node(db.DynamicDocument):
    active = db.IntField(required=True, default=0)
    ssid = db.StringField(required=True)
    password = db.StringField(required=True)
    rest_server = db.StringField(required=True)
    node = db.IntField(required=True, unique=True)
    detail = db.StringField(required=True)
    time_reset = db.IntField(required=True, default=24)
    time_update = db.IntField(required=True, default=60)
    time_sensor = db.IntField(required=True, default=100)
    protocol = db.StringField(required=True, default="http")
    batch_size = db.IntField()
    send_mode = db.StringField(required=True, default="stream")
    operaciones = db.ListField(db.EmbeddedDocumentField(Operacion), required=False)
    start = db.IntField(required=True, default=0)

    def to_json(self):
        # Initialize an empty dictionary to store the JSON representation
        json_data = {}

        # Iterate through all the fields in the document
        for field_name, field_value in self._data.items():
            # Check if the field is not None (empty) before adding it to the JSON
            if field_name != "id" and field_value is not None:
                json_data[field_name] = field_value

        return json_data