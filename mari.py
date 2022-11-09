from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '/home/vps2/vilab/files'

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

@app.route("/files", methods=(['POST']))
def save_file():
    print("Endpint reached")
    # check if the post request has the file part
    print(request.get_data())
    print(request.files)
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


@app.route('/upload_multipart', methods=['POST'])
def upload_multipart():
	print("upload_multipart")
	print("request={}".format(request))
	print("request.files={}".format(request.files))
	file_dict = request.files.to_dict(flat=False)
	#print("dict={}".format(file_dict))
	print("data={}".format(request.get_data()))

	'''
	file is werkzeug.datastructures.FileStorage Object.
	This object have these member.
		filename: Uploaded File Name
		name: Field name of Form
		headers: HTTP request header information(header object of flask)
		content_length: content-length of HTTP request
		mimetype: mimetype
	'''

	FileStorage = file_dict['test'][0]
	print("FileStorage={}".format(FileStorage))
	print("FileStorage.filename={}".format(FileStorage.filename))
	print("FileStorage.mimetype={}".format(FileStorage.mimetype))

	filename = FileStorage.filename
	filepath = os.path.join(UPLOAD_DIR, werkzeug.utils.secure_filename(filename))
	#FileStorage.save(filepath)

	try:
		FileStorage.save(filepath)
		responce = {'result':'upload OK'}
		print("{} uploaded {}, saved as {}".format(request.remote_addr, filename, filepath))
	except IOError as e:
		#logging.error("Failed to write file due to IOError %s", str(e))
		responce = {'result':'upload FAIL'}

	return json.dumps(responce)


@app.route("/events", methods=(['DELETE']))
def delete_event():
    mongo.db.events.remove({})
    return 'deleted'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



ALLOWED_EXTENSIONS = ['txt']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS