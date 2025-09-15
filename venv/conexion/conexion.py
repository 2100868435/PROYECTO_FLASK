# conexion directa sin aqlalchemy

import mysql.connector

# conexion
def conexion():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='proyectodw'
    )
# CERRAR CONEXION
def cerrar_conexion(conn):
    if conn.is_connected():
        conn.close()
        print("conexión cerrada,")



