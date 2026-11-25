import random
import json
from main import distancia_total

def crear_ruta(cantidad, rng):
    ruta = list(range(1, cantidad))
    rng.shuffle(ruta)
    return [0] + ruta

def seleccionar(poblacion, puntajes, rng, metodo="torneo"):
    if metodo == "torneo":
        candidatos = rng.sample(
            range(len(poblacion)),
            min(3, len(poblacion))
        )

        ganador = min(
            candidatos,
            key = lambda i: puntajes[i]
        )

        return poblacion[ganador]
    

    if metodo == "ruleta":
        pesos = [
            1/max(valor, 1e-9)
            for valor in puntajes
        ]
        return rng.choices(
            poblacion,
            weights = pesos,
            k = 1
        )[0]
    raise ValueError("metodo desconocido")
      


def cruzada(padre1, padre2, rng):
    n = len(padre1)

    if n < 4:
        return padre1.copy()

    a, b = sorted(rng.sample(range(1, n), 2))

    hijo = [None] * n
    hijo[0] = 0

    hijo[a:b+1] = padre1[a:b+1]

    usados = set(hijo[a:b+1])
    usados.add(0)

    orden_padre2 = (
        padre2[b+1:] +
        padre2[1:b+1]
    )

    restantes = [
        ciudad for ciudad in orden_padre2
        if ciudad not in usados
    ]

    posiciones = (
        list(range(b+1, n)) +
        list(range(1, a))
    )

    for posicion, ciudad in zip(posiciones, restantes):
        hijo[posicion] = ciudad

    return hijo

def cruzada_pmx(padre1, padre2, rng):
    n = len(padre1)

    if n < 4:
        return padre1.copy()

    a, b = sorted(rng.sample(range(1, n), 2))

    hijo = [None] * n
    hijo[0] = 0

    # Copiar un segmento del padre 1
    hijo[a:b+1] = padre1[a:b+1]

    # checar correspondencias padre 2
    for i in range(a, b+1):
        ciudad = padre2[i]

        if ciudad not in hijo:
            posicion = i

            while a <= posicion <= b:
                ciudad_padre1 = padre1[posicion]
                posicion = padre2.index(ciudad_padre1)

            hijo[posicion] = ciudad

    # Completar los espacios restantes
    for i in range(1, n):
        if hijo[i] is None:
            hijo[i] = padre2[i]

    return hijo

    
     
    
def mutar(ruta, rng, probabilidad = 0.3):
    nueva = ruta.copy()

    if rng.random() < probabilidad:
        i, j = rng.sample(range(1, len(ruta)), 2)
        nueva[i], nueva[j] = nueva[j], nueva[i]

    return nueva

def algoritmo_genetico(
        ciudades,
        semilla = 100,
        tam_poblacion = 40,
        max_evaluaciones = 4000,
        prob_mutacion = 0.3,
        metodo_seleccion = "torneo",
        metodo_cruzamiento = "OX",
        poblacion_inicial = None,
        fitness_inicial = None
):
    rng = random.Random(semilla)
    n = len(ciudades)

    if poblacion_inicial is None:
        poblacion = []
    else:
        poblacion = [ruta.copy() for ruta in poblacion_inicial]
    
    while len(poblacion) < tam_poblacion:
        poblacion.append(crear_ruta(n, rng))

    evaluaciones = 0
    mejor_ruta = None
    mejor_distancia = float("inf")
    convervengia = []

    def evaluar(ruta):
        nonlocal evaluaciones, mejor_ruta, mejor_distancia

        valor = distancia_total(ruta, ciudades)
        evaluaciones = evaluaciones + 1

        if valor < mejor_distancia:
            mejor_distancia = valor
            mejor_ruta = ruta.copy()

        convervengia.append((evaluaciones, mejor_distancia))
        return valor
    
    puntajes = []
    for i, ruta in enumerate(poblacion):
        if fitness_inicial is not None and i < len(fitness_inicial):
            valor = fitness_inicial[i]

            if valor < mejor_distancia:
                mejor_distancia = valor
                mejor_ruta = ruta.copy()

            puntajes.append(valor)
        else:
            puntajes.append(evaluar(ruta))

    assert len(puntajes) == len(poblacion), \
    "La cantidad de puntajes no coincide con la población"

    while evaluaciones < max_evaluaciones:
        orden = sorted(range(len(poblacion)), key = lambda i: puntajes[i])

        elite = poblacion[orden[0]].copy()
        nueva_poblacion = [elite]
        nuevos_puntajes = [puntajes[orden[0]]]

        while(len(nueva_poblacion) < tam_poblacion
              and evaluaciones < max_evaluaciones):
            
            padre1 = seleccionar(poblacion, puntajes, rng, metodo_seleccion)
            padre2 = seleccionar(poblacion, puntajes, rng, metodo_seleccion)

            if metodo_cruzamiento == "OX":
                hijo = cruzada(padre1, padre2, rng)
            elif metodo_cruzamiento == "PMX":
                hijo = cruzada_pmx(padre1, padre2, rng)
            else:
                raise ValueError("metodo de cruzamiento desconocido")
            hijo = mutar(hijo, rng, prob_mutacion)

            puntaje = evaluar(hijo)

            nueva_poblacion.append(hijo)
            nuevos_puntajes.append(puntaje)
        if len(nueva_poblacion) < tam_poblacion:
            break
        
        poblacion = nueva_poblacion
        puntajes = nuevos_puntajes

    return{
        "ruta": mejor_ruta,
        "distancia": mejor_distancia,
        "evaluaciones": evaluaciones,
        "convergencia": convervengia
    }

if __name__ == "__main__":
    with open("ciudades_A.json", "r") as archivo:
        ciudades = json.load(archivo)

    
    for metodo in ["torneo", "ruleta"]:
        for cruzamiento in ["OX", "PMX"]:

            resultado = algoritmo_genetico(
                ciudades,
                semilla=100,
                metodo_seleccion=metodo,
                metodo_cruzamiento=cruzamiento
            )

            ruta = resultado["ruta"]

            assert len(ruta) == len(ciudades)
            assert ruta[0] == 0
            assert sorted(ruta) == list(range(len(ciudades)))
            assert resultado["evaluaciones"] == 4000

            print("\nSelección:", metodo)
            print("Cruzamiento:", cruzamiento)
            print("Distancia:", round(resultado["distancia"], 2))
            print("Evaluaciones:", resultado["evaluaciones"])
            print("Ruta válida")


        rng = random.Random(100)

        padre1 = crear_ruta(len(ciudades), rng)
        padre2 = crear_ruta(len(ciudades), rng)

        hijo = cruzada_pmx(padre1, padre2, rng)

        print("\n--- PRUEBA PMX ---")
        print("Padre 1:", padre1)
        print("Padre 2:", padre2)
        print("Hijo:", hijo)

        assert len(hijo) == len(ciudades)
        assert hijo[0] == 0
        assert sorted(hijo) == list(range(len(ciudades)))

        print("PMX válido")

        rng = random.Random(200)

        for prueba in range(1000):
            padre1 = crear_ruta(len(ciudades), rng)
            padre2 = crear_ruta(len(ciudades), rng)

            hijo = cruzada_pmx(padre1, padre2, rng)

            assert hijo[0] == 0
            assert len(hijo) == len(ciudades)
            assert sorted(hijo) == list(range(len(ciudades)))
        print("1000 pruebas PMX superadas")

