"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
# añadir mi codigo aquí!!!
@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def create_person():
    # POST request
    body = request.get_json()  # Obtener el request body de la solicitud
    
    if body is None:
        return "El cuerpo de la solicitud es null", 400
    if 'first_name' not in body:
        return 'Debes especificar el nombre (first_name)', 400
    if 'age' not in body:
        return 'Debes especificar la edad (age)', 400
    if 'lucky_numbers' not in body:
        return 'Debes especificar los números de la suerte (lucky_numbers)', 400
    
    members = jackson_family.add_member(body)
    response_body = {
        "hello": "world",
        "family": members
    }

    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_person(id):
    deleted = jackson_family.delete_member(id)

    if deleted is False:
        return "Este miembro no existe", 400
    
    response_body = {
        "hello": "world",
        "deleted": deleted
    }

    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_person(id):
    members = jackson_family.get_member(id)

    if members is None:
        return "Este miembro no existe", 400
    
    response_body = {
        "hello": "world",
        "family": members
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
