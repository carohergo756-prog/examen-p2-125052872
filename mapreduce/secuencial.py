import csv
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

archivo = sys.argv[1] if len(sys.argv) > 1 else "ventas_125052872.csv"

resultados = defaultdict(lambda: [Decimal("0"), 0])

with open(archivo, "r", encoding="utf-8", newline="") as f:
    lector = csv.DictReader(f)

    for fila in lector:
        try:
            tienda = fila["tienda"].strip()
            cantidad = Decimal(fila["cantidad"])
            precio = Decimal(fila["precio_unitario"])

            if not tienda:
                continue

            resultados[tienda][0] += cantidad * precio
            resultados[tienda][1] += 1

        except (ValueError, InvalidOperation, KeyError, TypeError):
            continue

with open("mapreduce/resultado_secuencial.txt", "w", encoding="utf-8") as salida:
    for tienda in sorted(resultados):
        total, registros = resultados[tienda]

        if registros > 0:
            promedio = (total / registros).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

            salida.write(
                f"{tienda}\t{promedio}\t{registros}\t{total:.2f}\n"
            )

print("Procesamiento secuencial terminado.")
print(f"Tiendas procesadas: {len(resultados)}")
