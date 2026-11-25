import csv
import os
import statistics
import matplotlib.pyplot as plt

os.makedirs("resultados", exist_ok = True)

registros = []

with open("resultados/ejecuciones.csv", "r") as archivo:
    lector = csv.DictReader(archivo)
    registros = list(lector)

algoritmos = ["Genetico", "Hormigas", "Hibrido"]
escenarios = ["A", "B", "C"]

for escenario in escenarios:
    promedios = []
    desviaciones = []

    for algoritmo in algoritmos:
        distancias =[
            float(fila["distancia"])
            for fila in registros
            if fila["escenario"] == escenario
            and fila["algoritmo"] == algoritmo
        ]

        assert len(distancias) == 10, (
            f"se esperaban 10 resultados de"
            f"{algoritmo} en escenario {escenario}"
        )

        promedios.append(statistics.mean(distancias))
        desviaciones.append(statistics.stdev(distancias))
    
    plt.figure(figsize =(8, 5))

    plt.bar(
        algoritmos,
        promedios,
        yerr = desviaciones,
        capsize = 5
    )

    plt.title(f"Comparación de algoritmos - Escenario {escenario}")
    plt.ylabel("Distancia promedio")
    plt.xlabel("Algoritmo")
    plt.tight_layout()

    plt.savefig(f"resultados/comparacion_{escenario}.png", dpi=150)
    plt.close()

    print(f"Gráfica del escenario {escenario} generada")