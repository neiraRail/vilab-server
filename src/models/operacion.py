from src.database import db

class Operacion(db.DynamicEmbeddedDocument):
    tipo = db.StringField(required=True)
    subtipo = db.StringField(required=True)
