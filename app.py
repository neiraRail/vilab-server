from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'files'

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/vibration_db'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER


mongo = PyMongo(app)

@app.route("/events", methods=(['GET']))
def get_events():
    events = json_util.dumps(mongo.db.events.find())
    return events

@app.route("/")
def hola():
    return "Hola como estamo"

@app.route("/events/<id>", methods=(['GET']))
def get_event(id):
    return json_util.dumps(mongo.db.events.find_one({'_id': ObjectId(id)}))

@app.route("/events", methods=(['POST']))
def create_event():
    #a = {"text": "chao"}
    a = request.json
    id = mongo.db.events.insert_one(a)
    return json_util.dumps(mongo.db.events.find_one({'_id': id.inserted_id}))

@app.route("/add")
def add_event():
    a = {
        "a": 1
    }
    id = mongo.db.events.insert_one(a)
    return json_util.dumps(mongo.db.events.find_one({'_id': id.inserted_id}))

@app.route("/files", methods=(['POST']))
def save_file():
    print("Endpint reached")
    # check if the post request has the file part
    # print(request.get_data())
    # print(request.files)
    if len(request.files) == 0:
        print("Not file cause len of request.files is equal to 0")
        return 'No fileeee'
    file = list(request.files.values())[0]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        print("not file cause file.filename is empty")
        return 'No fileeeee'
    if True:
        print("File and is allowed")
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'file saved on {}'.format(os.path.join(app.config['UPLOAD_FOLDER'], filename))


@app.route("/events", methods=(['DELETE']))
def delete_event():
    mongo.db.events.remove({})
    return 'deleted'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)



ALLOWED_EXTENSIONS = ['txt']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
