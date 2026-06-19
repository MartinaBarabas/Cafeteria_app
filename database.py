import mysql.connector

def conectar():

    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tiziano.yantz",
        database="cafeteria"
    )

    return conexion