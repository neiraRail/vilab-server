from src.database import db


class Lectura(db.DynamicDocument):
    time_lap = db.LongField()
    time = db.LongField()
    node = db.IntField(required=True)
    acc_x = db.FloatField()
    acc_y = db.FloatField()
    acc_z = db.FloatField()
    gyr_x = db.FloatField()
    gyr_y = db.FloatField()
    gyr_z = db.FloatField()
    mag_x = db.FloatField()
    mag_y = db.FloatField()
    mag_z = db.FloatField()
    temp = db.FloatField()