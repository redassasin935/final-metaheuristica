import json
import time
import statistics
import csv
import os



from A_genetico import algoritmo_genetico
from B_hormiga import algoritmo_hormiga
from hibrido import algoritmo_hibrido

algoritmos = {
    "Genetico": algoritmo_genetico,
    "Hormigas": algoritmo_hormiga,
    "Hibrido": algoritmo_hibrido
}

semillas = range(100, 110)
escenarios = ["A", "B", "C"]

os.makedirs("resultados", exist_ok = True)
registros = []

for escenario in escenarios:

    with open(f"ciudades_{escenario}.json", "r") as archivo:
        ciudades = json.load(archivo)
    print(f"\n===== ESCENARIO {escenario} =====")

    for nombre, algoritmo in algoritmos.items():
        distancias = []
        tiempos = []

        for semilla in semillas:
            inicio = time.perf_counter()

            resultado = algoritmo(
                ciudades,
                semilla = semilla,
                max_evaluaciones = 4000
            )
            tiempo = time.perf_counter() - inicio

            assert resultado["evaluaciones"] == 4000

            distancias.append(resultado["distancia"])
            tiempos.append(tiempo)

            registros.append({
                "algoritmo": nombre,
                "escenario": escenario,
                "semilla": semilla,
                "distancia": resultado["distancia"],
                "evaluaciones": resultado["evaluaciones"],
                "tiempo": tiempo
            })
            
    print("\nAlgoritmo:", nombre)
    print("Mejor distancia:", round(min(distancias), 2))
    print("Promedio:", round(statistics.mean(distancias), 2))
    print("Desviación estándar:",
              round(statistics.stdev(distancias), 2))
    print("Tiempo promedio:",
              round(statistics.mean(tiempos), 4), "segundos")





with open("resultados/ejecuciones.csv", "w", newline="") as archivo:
    campos = [
        "algoritmo", "escenario", "semilla",
        "distancia", "evaluaciones", "tiempo"
    ]

    escritor = csv.DictWriter(archivo, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(registros)

print("\nResultados guardados en resultados/ejecuciones.csv")



    