import mysql.connector

def obtener_conexion():
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="cafeteria_rosita",
        port=3307
    )
    return conexion