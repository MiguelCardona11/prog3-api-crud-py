# Se importa la libreria para montar el servidor local.
from flask import Flask, request, jsonify
# Se importa el conector para la base de datos.
import mysql.connector

app = Flask(__name__)

# Creo una nueva conexión con MySQL para poder interactuar con nuestra DB
mysqlConnection = mysql.connector.connect(
    # En el host se podría poner el equipo en el que esté.
    host="localhost",
    user="root",
    password="root",
    database="project_db"
)
# Ahora con este cursor puedo utilizar la bases de datos.
cursor = mysqlConnection.cursor(dictionary=True)

# Tengo un servidor para que cuando pongan la ruta por defecto, utilizando el método GET (obtener informacion, metodo por defecto)
# Nos ejecute nuestra funcion de Hola Mundo
@app.route('/', methods=['GET'])
def holaMundo():
    # Me retorna un JSON
    response={
        "message":"hello world"
    }
    # convertimos el diccionario a JSON.
    return jsonify(response)

@app.route('/users', methods=['GET'])
def getUsers():
    # Ejecuto una sentencia SQL (seleccione todos los datos de la tabla "users")
    cursor.execute("SELECT * FROM users")
    # fetchall devuelve una lista con los datos de todos los usuarios
    users = cursor.fetchall()
    # Convierte la lista de diccionarios en texto en formato JSON
    return jsonify(users)

# @app.route define la ruta, y luego se selecciona el método
@app.route('/users', methods=['POST'])
def createUser():
    # data es lo que vamos a enviar en formato JSON que luego pasará a ser un diccionario
    data = request.get_json()
    # Tomamos los datos que vienen del cliente
    name = data['name']
    password = data['password']
    email = data['email']
    nickname = data['nickname']
    # Inserto en la tabla "usuarios" los campos obtenidos (lo de VALUES es para el formato y se ponen las 4 variables)
    cursor.execute("INSERT INTO users (name, password, email, nickname) VALUES (%s, %s, %s, %s)",
                   (name, password, email, nickname))
    # Ejecuto el mensaje
    mysqlConnection.commit()
    # Retorno en formato JSON un mensaje
    return jsonify({"message": "User created successfully"})

# Obtener usuario por ID
# Lo nuevo de esta URL es que en la ruta podemos definir un parametro, en este caso un int
@app.route('/users/<int:userId>', methods=['GET'])
# Definimos la funcion donde toma como parametro un "userId"
def getUser(userId):
    # Recibe toda la informacion de "users" donde el id coincida con el id userId
    cursor.execute("SELECT * FROM users WHERE id = %s", (userId,))
    # Selecciona la informacion de un solo usuario
    user = cursor.fetchone()
    return jsonify(user)

# Actualizar usuario por ID
# Recibo el ID del usuario en la ruta
@app.route('/users/<int:userId>', methods=['PUT'])
# Necesito saber a quien voy a actualizar: "userID"
def updateUser(userId):
    # Necesito leer la nueva información, la que voy a usar
    data = request.get_json()
    name = data['name']
    password = data['password']
    email = data['email']
    nickname = data['nickname']
    # Se usa la consulta SQL de actualizacion Actualizo en la tabla "users" todos los parametros, DONDE los
    # parametros coincidan con la userId que vino en la funcion.
    cursor.execute("UPDATE users SET name = %s, password = %s, email =%s, nickname = %s WHERE id = %s",
                   (name, password, email, nickname, userId))
    # Se ejecuta la consulta
    mysqlConnection.commit()
    return jsonify({"message": "User updated successfully"})

# Eliminar usuario por ID
# Recibo el ID del usuario en la ruta
@app.route('/users/<int:userId>', methods=['DELETE'])
def deleteUser(userId):
    # Borro en la tabla "users" el id "userId"
    cursor.execute("DELETE FROM users WHERE id = %s", (userId,))
    mysqlConnection.commit()
    return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    print("hola mundo")
    app.run(debug=True)