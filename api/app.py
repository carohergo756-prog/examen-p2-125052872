import os
from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

def convertir(registro):
    registro["ticket_promedio"] = float(registro["ticket_promedio"])
    registro["ingreso_total"] = float(registro["ingreso_total"])
    return registro

@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "proyecto": "DataMart",
        "estado": "API funcionando",
        "pregunta": "Ticket promedio por tienda"
    })

@app.route("/resultados", methods=["GET", "POST"])
def resultados():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    if request.method == "GET":
        cursor.execute("SELECT * FROM resultados ORDER BY tienda")
        datos = [convertir(r) for r in cursor.fetchall()]
        cursor.close()
        conexion.close()
        return jsonify(datos)

    datos = request.get_json(silent=True) or {}

    campos = ["tienda", "ticket_promedio", "registros", "ingreso_total"]

    if not all(campo in datos for campo in campos):
        cursor.close()
        conexion.close()
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    cursor.execute("""
        INSERT INTO resultados
        (tienda, ticket_promedio, registros, ingreso_total)
        VALUES (%s, %s, %s, %s)
    """, (
        datos["tienda"],
        datos["ticket_promedio"],
        datos["registros"],
        datos["ingreso_total"]
    ))

    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"mensaje": "Resultado agregado"}), 201

@app.route("/resultados/<tienda>", methods=["GET", "PUT", "DELETE"])
def resultado_tienda(tienda):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    if request.method == "GET":
        cursor.execute(
            "SELECT * FROM resultados WHERE tienda = %s",
            (tienda,)
        )
        dato = cursor.fetchone()
        cursor.close()
        conexion.close()

        if dato is None:
            return jsonify({"error": "Tienda no encontrada"}), 404

        return jsonify(convertir(dato))

    if request.method == "PUT":
        datos = request.get_json(silent=True) or {}

        cursor.execute("""
            UPDATE resultados
            SET ticket_promedio = %s,
                registros = %s,
                ingreso_total = %s
            WHERE tienda = %s
        """, (
            datos.get("ticket_promedio"),
            datos.get("registros"),
            datos.get("ingreso_total"),
            tienda
        ))

        conexion.commit()
        modificados = cursor.rowcount
        cursor.close()
        conexion.close()

        if modificados == 0:
            return jsonify({"error": "Tienda no encontrada"}), 404

        return jsonify({"mensaje": "Resultado actualizado"})

    cursor.execute("DELETE FROM resultados WHERE tienda = %s", (tienda,))
    conexion.commit()
    eliminados = cursor.rowcount
    cursor.close()
    conexion.close()

    if eliminados == 0:
        return jsonify({"error": "Tienda no encontrada"}), 404

    return jsonify({"mensaje": "Resultado eliminado"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
