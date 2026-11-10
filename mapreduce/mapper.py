#!/usr/bin/env python3
import sys
import csv
from decimal import Decimal, InvalidOperation

for linea in sys.stdin:
    try:
        fila = next(csv.reader([linea]))

        if len(fila) != 8 or fila[0].strip().lower() == "id":
            continue

        tienda = fila[2].strip()
        cantidad = Decimal(fila[5])
        precio = Decimal(fila[6])

        if not tienda:
            continue

        ingreso = cantidad * precio

        print(f"{tienda}\t{ingreso:.2f}\t1")

    except (ValueError, InvalidOperation, IndexError, csv.Error):
        continue
