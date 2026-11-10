#!/usr/bin/env python3
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

resultados = {}

for linea in sys.stdin:
    try:
        partes = linea.strip().split("\t")

        if len(partes) != 3:
            continue

        tienda = partes[0]
        ingreso = Decimal(partes[1])
        cantidad = int(partes[2])

        if tienda not in resultados:
            resultados[tienda] = [Decimal("0"), 0]

        resultados[tienda][0] += ingreso
        resultados[tienda][1] += cantidad

    except (ValueError, InvalidOperation):
        continue

for tienda in sorted(resultados):
    total, registros = resultados[tienda]

    if registros > 0:
        promedio = (total / registros).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        print(f"{tienda}\t{promedio}\t{registros}\t{total:.2f}")
