from flask import jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from . import app

# Configura la conexión a MongoDB

client = MongoClient("mongodb:27017")
db = client["proyecto"]
citas_collection = db["citas"]

# Crear una nueva cita
@app.route('/crear/cita', methods=['POST'])
def crear_cita():
    data = request.json
    cita = {
        "nombre": data.get("nombre"),
        "fecha": data.get("fecha"),
        "hora": data.get("hora"),
        "descripcion": data.get("descripcion")
    }
    result = citas_collection.insert_one(cita)
    return jsonify({"message": "Cita creada", "id": str(result.inserted_id)}), 201

# Consultar todas las citas
@app.route('/ver/citas', methods=['GET'])
def obtener_citas():
    citas = []
    for cita in citas_collection.find():
        citas.append({
            "id": str(cita["_id"]),
            "nombre": cita["nombre"],
            "fecha": cita["fecha"],
            "hora": cita["hora"],
            "descripcion": cita["descripcion"]
        })
    return jsonify(citas), 200

# Consultar una cita por ID
@app.route('/consultar/cita/<id>', methods=['GET'])
def obtener_cita(id):
    cita = citas_collection.find_one({"_id": ObjectId(id)})
    if cita:
        return jsonify({
            "id": str(cita["_id"]),
            "nombre": cita["nombre"],
            "fecha": cita["fecha"],
            "hora": cita["hora"],
            "descripcion": cita["descripcion"]
        }), 200
    return jsonify({"message": "Cita no encontrada"}), 404

# Actualizar una cita
@app.route('/modificar/cita/<id>', methods=['PUT'])
def actualizar_cita(id):
    data = request.json
    update_result = citas_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "nombre": data.get("nombre"),
            "fecha": data.get("fecha"),
            "hora": data.get("hora"),
            "descripcion": data.get("descripcion")
        }}
    )
    if update_result.matched_count == 1:
        return jsonify({"message": "Cita actualizada"}), 200
    return jsonify({"message": "Cita no encontrada"}), 404

# Eliminar una cita
@app.route('/borrar/cita/<id>', methods=['DELETE'])
def eliminar_cita(id):
    delete_result = citas_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return jsonify({"message": "Cita eliminada"}), 200
    return jsonify({"message": "Cita no encontrada"}), 404

if __name__== '_main_':
    app.run(debug=True)