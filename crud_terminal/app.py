from pymongo import MongoClient # El cliente de MongoDB
from bson.objectid import ObjectId # Para crear ObjectId, porque _id como cadena no funciona
from datetime import date

def obtener_bd():
    # host = "localhost"
    # puerto = "27017"
    base_de_datos = "test"
    cliente = MongoClient("mongodb://127.0.0.1:27017/")
    return cliente[base_de_datos]

def insertar(x, y, z):
    base_de_datos = obtener_bd()
    persona = base_de_datos.persona
    return persona.insert_one({
        "_id": x,
        "nombre": y,
        "cantidad": z,
        }).inserted_id

def obtener():
    base_de_datos = obtener_bd()
    persona =  list(base_de_datos.persona.find())
    return persona
def actualizar(id, user):
    base_de_datos = obtener_bd()
    resultado = base_de_datos.persona.update_one(
        {
        '_id': ObjectId(id)
        }, 
        {
            '$set': {
                "_id": user._id,
                "nombre": user.nombre,
                "fecha_nacimiento": user.fecha_nacimiento,
            }
        })
    return resultado.modified_count

def eliminar(id):
    base_de_datos = obtener_bd()
    resultado = base_de_datos.persona.delete_one(
        {
        '_id': ObjectId(id)
        })
    return resultado.deleted_count

menu = """Welcome.
1 - Insertar usuario
2 - Ver todos
3 - Actualizar
4 - Eliminar
5 - Salir
"""
eleccion = None
while eleccion is not 5:
    print(menu)
    eleccion = int(input("Elige: "))
    if eleccion is 1:
        print("Insertar")
        _id = str(input("id: "))
        nombre = str(input("Nombre: "))
        fecha_nacimiento = str(input("Fecha_de_nacimiento: "))
        perso = insertar(_id,nombre,fecha_nacimiento)
    elif eleccion is 2:
        print("Obteniendo users")
        for personas in obtener():
            print("=================")
            print("Id: ", personas["_id"])
            print("Nombre: ", personas["nombre"])
            print("fecha_nacimiento: ", personas["cantidad"])
    elif eleccion is 3:
        print("Actualizar")
        id = input("Dime el id: ")
        nombre = str(input("Nuevo nombre: "))
        fecha_nacimiento = str(input("Nueva fecha de nacimiento: "))
        user = user(nombre, fecha_nacimiento)
        usuarios_actualizados = actualizar(id, user)
        print("Número de usuarios actualizados: ", usuarios_actualizados)
    elif eleccion is 4:
        print("Eliminar")
        id = input("Dime el id: ")
        usuarios_eliminados = eliminar(id)
        print("Número de usuarios eliminados: ", usuarios_eliminados)