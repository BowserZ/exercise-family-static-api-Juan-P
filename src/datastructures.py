
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name

        # example list of members
        self._members = []

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        # fill this method and update the return
        if "id" not in member:
            member["id"] = self._generateId()  # Genera un ID único si no existe
        member["last_name"] = self.last_name  # Asegura que el apellido sea "Jackson"
        self._members.append(member)  # Agrega el miembro a la lista
        return member  # Devuelve el miembro agregado

    def delete_member(self, id):
        # fill this method and update the return
        for member in self._members:
            if member["id"] == id:
                self._members.remove(member)  # Elimina el miembro si se encuentra
                return True  # Indica que el miembro fue eliminado
        return False  # Indica que el miembro no se encontró

    def get_member(self, id):
        # fill this method and update the return
        for member in self._members:
            if member["id"] == id:
                return member  # Devuelve el miembro si se encuentra
        return None  # Devuelve None si el miembro no existe

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members



"""

This is for a new family, but in order for the test to work I commented this.

This module takes care of starting the API Server, Loading the DB and Adding the endpoints

import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

# Initialize the Flask app
app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Dictionary to store more families :D
families = {
    "Jackson": FamilyStructure("Jackson"),
    "Neumann": FamilyStructure("Neumann")
}

#Family Members

families["Jackson"].add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})
families["Jackson"].add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})
families["Jackson"].add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
})

families["Neumann"].add_member({
    "first_name": "Johannes",
    "age": 25,
    "lucky_numbers": [7, 33, 100]
})

# Error handler
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Get all members of a specific family
@app.route('/<family_name>/members', methods=['GET'])
def get_members(family_name):
    if family_name not in families:
        return jsonify({"error": "Family not found"}), 404
    members = families[family_name].get_all_members()
    return jsonify(members), 200

# Get a specific member from a family by ID
@app.route('/<family_name>/member/<int:member_id>', methods=['GET'])
def get_member(family_name, member_id):
    if family_name not in families:
        return jsonify({"error": "Family not found"}), 404
    member = families[family_name].get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

# Add a new member to a family
@app.route('/<family_name>/member', methods=['POST'])
def add_member(family_name):
    if family_name not in families:
        return jsonify({"error": "Family not found"}), 404
    new_member = request.get_json()
    if not new_member:
        return jsonify({"error": "Invalid input"}), 400
    families[family_name].add_member(new_member)
    return jsonify({"message": "Member added"}), 200

# Delete a member from a family by ID
@app.route('/<family_name>/member/<int:member_id>', methods=['DELETE'])
def delete_member(family_name, member_id):
    if family_name not in families:
        return jsonify({"error": "Family not found"}), 404
    if families[family_name].delete_member(member_id):
        return jsonify({"done": True}), 200
    return jsonify({"error": "Member not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
"""