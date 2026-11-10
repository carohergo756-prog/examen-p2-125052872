import os
import mysql.connector

archivo = "/app/mapreduce/resultado_hadoop/part-00000"

conexion = mysql.connector.connect(
    host=os.getenv("DB_HOST", "db"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS resultados (
    tienda VARCHAR(20) PRIMARY KEY,
    ticket_promedio DECIMAL(12,2) NOT NULL,
    registros INT NOT NULL,
    ingreso_total DECIMAL(18,2) NOT NULL
)
""")

cursor.execute("DELETE FROM resultados")

insertar = """
INSERT INTO resultados
(tienda, ticket_promedio, registros, ingreso_total)
VALUES (%s, %s, %s, %s)
"""

datos = []

with open(archivo, "r", encoding="utf-8") as f:
    for linea in f:
        partes = linea.strip().split("\t")

        if len(partes) != 4:
            continue

        tienda, promedio, registros, ingreso = partes

        datos.append((
            tienda,
            promedio,
            int(registros),
            ingreso
        ))

cursor.executemany(insertar, datos)
conexion.commit()

print(f"Resultados cargados correctamente: {len(datos)} tiendas")

cursor.close()
conexion.close()
