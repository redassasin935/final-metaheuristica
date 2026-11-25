import random
import json
from main import distancia, distancia_total

def hacer_matriz_distancias(ciudades):
    n = len(ciudades)

    matriz = []

    for i in range(n):
        fila = []

        for j in range(n):
            if i == j:
                fila.append(0)
            else:
                fila.append(distancia(ciudades[i], ciudades[j]))
        matriz.append(fila)
    return matriz

def hacer_matriz_feromonas(cantidad, inicial = 1.0):
    matriz = []
    
    for i in range(cantidad):
        fila = []

        for j in range(cantidad):
            if i == j:
                fila.append(0.0)
            else:
                fila.append(inicial)
        matriz.append(fila)
    return matriz

def selecciona_siguiente_ciudad(
        actual, no_visitadas, distancias,
        feromonas, rng, alfa = 1.0, beta = 2.0
):
    pesos = []

    for ciudad in no_visitadas:
        feromona = feromonas[actual][ciudad]
        distancia = distancias[actual][ciudad]

        peso = (feromona ** alfa) *(
            1/max(distancia, 1e-9)
        ) ** beta
        pesos.append(peso)
    
    siguiente = rng.choices(
        no_visitadas,
        weights = pesos,
        k = 1
    )[0]
    return siguiente

def construir_ruta(distancias, feromonas, rng, alfa = 1.0, beta = 2.0):
    n = len(distancias)

    ruta = [0]
    no_visitadas = list(range(1, n))

    while no_visitadas:
        actual = ruta[-1]

        siguiente = selecciona_siguiente_ciudad(
            actual,
            no_visitadas,
            distancias,
            feromonas,
            rng,
            alfa,
            beta
        )

        ruta.append(siguiente)
        no_visitadas.remove(siguiente)
    return ruta

def evaporar_feromonas(feromonas, evaporacion = 0.3):
    n = len(feromonas)

    for i in range(n):
        for j in range(n):
            if i != j:
                feromonas[i][j] = feromonas[i][j] * (1 - evaporacion)

def depositar_feromonas(feromonas, ruta, distancia_ruta, q=100):
    deposito = q / max(distancia_ruta, 1e-9)

    for i in range(len(ruta)):
        actual = ruta[i]
        siguiente = ruta[(i + 1) % len(ruta)]

        feromonas[actual][siguiente] += deposito
        feromonas[siguiente][actual] += deposito
        

def algoritmo_hormiga(
        ciudades,
        semilla = 100,
        Num_hormigas = 30,
        max_evaluaciones = 4000,
        evaporacion = 0.2,
        alfa  = 1.0,
        beta = 2.0,
        q = 100
):
    rng = random.Random(semilla)

    distancias = hacer_matriz_distancias(ciudades)
    feromonas = hacer_matriz_feromonas(len(ciudades))

    mejor_ruta = None
    Mejor_distancia = float("inf")
    evaluaciones = 0
    Convergencia = []

    while evaluaciones < max_evaluaciones:
        rutas = []

        for _ in range(Num_hormigas):
            if evaluaciones >= max_evaluaciones:
                break
            
            ruta = construir_ruta(
                distancias, feromonas, rng, alfa, beta
            )

            valor = distancia_total(ruta, ciudades)
            evaluaciones = evaluaciones + 1

            rutas.append((ruta, valor))

            if valor < Mejor_distancia:
                Mejor_distancia = valor
                mejor_ruta = ruta.copy()
            
            Convergencia.append(
                (evaluaciones, Mejor_distancia)
            )
        evaporar_feromonas(feromonas, evaporacion)
        
        for ruta, valor in rutas:
            depositar_feromonas(
                feromonas, ruta, valor, q
            )
    return {
        "ruta": mejor_ruta,
        "distancia": Mejor_distancia,
        "evaluaciones": evaluaciones,
        "convergencia": Convergencia
    }

if __name__ == "__main__":
    with open("ciudades_A.json", "r") as archivo:
        ciudades = json.load(archivo)
    resultado = algoritmo_hormiga(ciudades)

    print("mejor ruta:", resultado["ruta"])
    print("mejor distancia:", round(resultado["distancia"], 2))
    print("evaluaciones:", resultado["evaluaciones"])

    ruta = resultado["ruta"]

    assert len(ruta) == len(ciudades)
    assert ruta[0] == 0
    assert sorted(ruta) == list(range(len(ciudades)))

    print("ruta valida")
