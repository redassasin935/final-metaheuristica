import json
import os
import matplotlib.pyplot as plt

from A_genetico import algoritmo_genetico
from B_hormiga  import algoritmo_hormiga
from hibrido import algoritmo_hibrido

algoritmos = {
    "genetico": algoritmo_genetico,
    "hormigas": algoritmo_hormiga,
    "Hibrido": algoritmo_hibrido
}

os.makedirs("resultados", exist_ok = True)

for escenario in ["A", "B", "C"]:
    with open(f"ciudades_{escenario}.json", "r") as archivo:
        ciudades = json.load(archivo)
    
    plt.figure(figsize=(9,5))

    for nombre, algoritmo in algoritmos.items():
        resultado = algoritmo(
            ciudades,
            semilla = 100,
            max_evaluaciones = 4000
        )

        convergencia = resultado["convergencia"]

        assert len(convergencia) == 4000
        assert resultado["evaluaciones"] == 4000

        evaluaciones = [punto[0] for punto in convergencia]
        distancias = [punto[1] for punto in convergencia]

        plt.plot(evaluaciones, distancias, label = nombre)
        
    plt.title(f"Convergencia - Escenario {escenario}")
    plt.xlabel("Evaluaciones")
    plt.ylabel("Mejor distancia acumulada")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        f"resultados/convergencia_{escenario}.png",
        dpi=150
    )
    plt.close()

    print(f"Convergencia del escenario {escenario} generada")

