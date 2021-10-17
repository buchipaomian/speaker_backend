from flask import *
from flask_cors import CORS
import os,sys, time
 
app = Flask(__name__)
cors = CORS() 
cors.init_app(app)

@app.route('/audio/<id>', methods=['GET'])
def get_file1(id):
    directory = './'
    print(id)
    id = int(id)
    file_name = ""
    if id ==1:
        file_name = "mixed.wav"
    elif id ==2:
        file_name = "embedder.wav"
    elif id ==3:
        file_name = "result.wav"
    print(file_name)
    response = make_response(
        send_from_directory(directory, file_name, as_attachment=True))
    return response

@app.route('/upload/mixed', methods=['POST'])
def save_mixed():
    blob = request.files['mixed']
    filename = "mixed.wav"
    id = 1
    blob.save(filename)

    return jsonify({"id": 1})

@app.route('/upload/embedder', methods=['POST'])
def save_embedder():
    blob = request.files['embedder']
    name = request.form['name']
    print(name)
    filename = "embedder.wav"
    id = 2
    blob.save(filename)

    return jsonify({"status": True, "id":id, "name":name})

@app.route('/embedder',methods = ['GET'])
def get_embedder():
    list = [{'id':2, 'name':'Alice'}, {'id':2, 'name':'Bob'}]
    return jsonify(list)

@app.route('/filter',methods = ['POST'])
def get_filter():
    mixed = request.form['mixed']
    embedder = request.form['embedder']
    print(mixed, embedder)
    id = 3
    time.sleep(10)
    return jsonify({'id':id})

@app.route('/to_text',methods = ['GET'])
def get_text():
    text = "Hello, this the template message of speech to text."
    status = 'done'
    return jsonify({'status':status, 'text':text})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
