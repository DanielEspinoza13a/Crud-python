from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from pymongo import response

from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["MONGO_URI"]='mongodb://localhost/test'
mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():

    _id = request.json['_id']
    nombre = request.json['nombre']
    fecha_nacimiento = request.json['fecha_nacimiento']
    password = request.json['password']

    if _id and nombre and fecha_nacimiento and password:
        hashed_password = generate_password_hash(password)
        mongo.db.person.insert(
            {'_id': _id, 'nombre': nombre, 'fecha_nacimiento': fecha_nacimiento, 'password':password}
        )
        response = {
            '_id': str(_id),
            'nombre': nombre,
            'fecha_nacimiento': fecha_nacimiento,
            'password': hashed_password,
        }
        return response
    else:
        return not_found()

    return {'message': 'received'}

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.person.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.person.find({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return response

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.person.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):
    nombre = request.json['nombre']
    fecha_nacimiento = request.json['fecha_nacimiento']
    password = request.json['password']

    if nombre and fecha_nacimiento and password:
        hashed_password = generate_password_hash(password)
        mongo.db.person.update_one({'_id': ObjectId(_id['id'])},{'$set': {
            'nombre': nombre,
            'fecha_nacimiento': fecha_nacimiento, 
            'password':password
         }})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not found:' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__=="__main__":
    app.run(debug=True)