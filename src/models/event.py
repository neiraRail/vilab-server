from src.database import db


class Event(db.Document):
    time_lap = db.LongField()
    time = db.IntField()
    node = db.IntField()
    event = db.IntField()
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
    start = db.IntField()

    def to_json(self):
        return {
            "time_lap": self.time_lap,
            "time": self.time,
            "node": self.node,
            "event": self.event,
            "acc_x": self.acc_x,
            "acc_y": self.acc_y,
            "acc_z": self.acc_z,
            "gyr_x": self.gyr_x,
            "gyr_y": self.gyr_y,
            "gyr_z": self.gyr_z,
            "mag_x": self.mag_x,
            "mag_y": self.mag_y,
            "mag_z": self.mag_z,
            "temp": self.temp,
            "start": self.start,
        }
