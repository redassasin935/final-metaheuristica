from A_genetico import algoritmo_genetico
from B_hormiga import algoritmo_hormiga

def algoritmo_hibrido(
    ciudades,
    semilla = 100,
    max_evaluaciones = 4000
):
    presupuesto_aco = int(max_evaluaciones * 0.10)
    presupuesto_ag = max_evaluaciones - presupuesto_aco

    resultado_aco = algoritmo_hormiga(
        ciudades,
        semilla = semilla,
        max_evaluaciones = presupuesto_aco
    )

    rutas_iniciales = [resultado_aco["ruta"]]

    resultado_ag = algoritmo_genetico(
        ciudades,
        semilla = semilla,
        max_evaluaciones = presupuesto_ag,
        poblacion_inicial = rutas_iniciales,
        fitness_inicial =[resultado_aco["distancia"]]
    )

    if resultado_aco["distancia"] < resultado_ag["distancia"]:
        mejor_ruta = resultado_aco["ruta"]
        mejor_distancia = resultado_aco["distancia"]
    else:
        mejor_ruta = resultado_ag["ruta"]
        mejor_distancia = resultado_ag["distancia"]

    convergencia = resultado_aco["convergencia"].copy()

    evaluaciones_aco = resultado_aco["evaluaciones"]
    mejor_acumulada = resultado_aco["distancia"]

    for evaluacion, distancia in resultado_ag["convergencia"]:
        mejor_acumulada = min(mejor_acumulada, distancia)

        convergencia.append((
            evaluaciones_aco + evaluacion,
            mejor_acumulada
        ))

    return {
        "convergencia": convergencia,
        "ruta": mejor_ruta,
        "distancia": mejor_distancia,
        "evaluaciones": (
            resultado_aco["evaluaciones"]
            + resultado_ag["evaluaciones"]
        ),
        "aco": resultado_aco,
        "ag": resultado_ag
     }

if __name__ == "__main__":
    import json

    with open("ciudades_A.json", "r") as archivo:
        ciudades = json.load(archivo)

    resultado = algoritmo_hibrido(ciudades)

    print("Distancia ACO:",
          round(resultado["aco"]["distancia"], 2))

    print("Distancia AG:",
          round(resultado["ag"]["distancia"], 2))

    print("Evaluaciones totales:",
          resultado["aco"]["evaluaciones"]
          + resultado["ag"]["evaluaciones"])
    

    print("Mejor distancia híbrida:",
      round(resultado["distancia"], 2))

    print("Evaluaciones:",
      resultado["evaluaciones"])

    print("Puntos de convergencia:",
      len(resultado["convergencia"]))

    ruta = resultado["ruta"]

    assert ruta[0] == 0
    assert sorted(ruta) == list(range(len(ciudades)))
    assert resultado["evaluaciones"] == 4000
    assert len(resultado["convergencia"]) == 4000

    print("Híbrido válido")

    