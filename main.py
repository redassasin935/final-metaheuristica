import math

def distancia(ciudad1, ciudad2):
    x1, y1 = ciudad1
    x2, y2 = ciudad2

    resultado = math.sqrt((x2-x1)**2 + (y2-y1)**2)

    return resultado



ruta = [0, 1, 2, 3]

def distancia_total(ruta, ciudades):
    total = 0

    for i in range(len(ruta)):
        actual = ciudades[ruta[i]]
        siguiente = ciudades[ruta[(i+1) % len(ruta)]]

        total = total + distancia(actual, siguiente)
    return total

