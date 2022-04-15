import sqlite3
from sqlite3 import Error
from flask import Flask

app = Flask(__name__)

def crearConexion():
    connection = None
    try:
        connection = sqlite3.connect(r"slang_sqlite.db")
        print(sqlite3.version)
    except Error as e:
        print(e)

    return connection

def crearTabla(conn):
    query = """ CREATE TABLE IF NOT EXISTS slang (
            palabra VARCHAR(255) NOT NULL,
            significado VARCHAR(255) NOT NULL,
            PRIMARY KEY (palabra)
        ); """
    cursor = conn.cursor()
    cursor.execute(query)

@app.route("/create", methods=("POST",))
def agregarPalabra(conn, palabra, significado):
    try:
        query = "INSERT INTO slang VALUES (?, ?)"
        values = (palabra, significado)
        cursor = conn.cursor()
        cursor.execute(query, values)
        print("Palabra agregada!\n")
    except Error as e:
        print(e)

@app.route("/<str:palabra>/update", methods=("POST",))
def editarPalabra(conn, palabra, significado):
    try:
        query = "UPDATE slang SET significado = ? WHERE palabra = ?"
        values = (significado, palabra)
        cursor = conn.cursor()
        cursor.execute(query, values)
        print("Palabra actualizada!\n")
    except Error as e:
        print(e)

@app.route("/<str:palabra>/delete", methods=("POST",))
def eliminarPalabra(conn, palabra):
    try:
        query = "DELETE FROM slang WHERE palabra = ?"
        values = (palabra,)
        cursor = conn.cursor()
        cursor.execute(query, values)
        print("Palabra eliminada!\n")
    except Error as e:
        print(e)

@app.route("/palabras")
def listarPalabras(conn):
    query = "SELECT * FROM slang ORDER BY palabra ASC"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print("- " + row[0] + ": " + row[1])

@app.route("/palabra/<str:palabra>")
def buscarPalabra(conn, palabra):
    query = "SELECT * FROM slang WHERE palabra = ?"
    values = (palabra)
    cursor = conn.cursor()
    cursor.execute(query, values)
    result = cursor.fetchone()
    print("- " + result[0] + ": " + result[1] + "\n")

conn = crearConexion()
with conn:
    crearTabla(conn)

