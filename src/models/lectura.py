from src.database import db


class Lectura(db.DynamicDocument):
    delta = db.IntField(required=True)
    time = db.LongField(required=True)
    node = db.IntField(required=True)
    acc_x = db.FloatField(required=True)
    acc_y = db.FloatField(required=True)
    acc_z = db.FloatField(required=True)
    gyr_x = db.FloatField()
    gyr_y = db.FloatField()
    gyr_z = db.FloatField()
    mag_x = db.FloatField()
    mag_y = db.FloatField()
    mag_z = db.FloatField()
    temp = db.FloatField()