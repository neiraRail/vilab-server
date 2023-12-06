from src.database import db

class Feature(db.DynamicEmbeddedDocument):
    subtipo = db.StringField(required=True)
    node = db.IntField(required=True)
    time = db.LongField(required=True)
    start = db.IntField(required=True)
    batch_id = db.IntField(required=True)