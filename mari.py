from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import json_util, ObjectId

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/vibration_db'

mongo = PyMongo(app)

@app.route("/events", methods=(['GET']))
def get_events():
    events = json_util.dumps(mongo.db.events.find())
    return events

@app.route("/events/<id>", methods=(['GET']))
def get_event(id):
    return json_util.dumps(mongo.db.events.find_one({'_id': ObjectId(id)}))

@app.route("/events", methods=(['POST']))
def create_event():
    #a = {"text": "chao"}
    a = request.json
    id = mongo.db.events.insert_one(a)
    return json_util.dumps(mongo.db.events.find_one({'_id': id.inserted_id}))
        

@app.route("/events", methods=(['DELETE']))
def delete_event():
    mongo.db.events.remove({})
    return 'deleted'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
