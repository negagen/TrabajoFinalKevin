import re, math

n = int(input("Ingrese el numero de vertices: "))

deltas_ns = 0
deltas_ew = 0
suma_proyecciones_ns = 0
suma_proyecciones_ew = 0

suma_teorica = (n+2)*180 

def decimal_a_gmd(angulo_decimal ):
    grados, minutos = math.modf(angulo_decimal)
    minutos, segundos = math.modf(minutos*60)
    segundos = segundos*60
    return (grados, minutos, segundos)


def gmd_a_decimal(grados, minutos, segundos):
    return grados + minutos / 60 + segundos / 3600


def parse_gmd_texto(dms_str):
    numbers = [*filter(len, re.split('\D+', dms_str, maxsplit=4))]

    degree = numbers[0]
    minute = numbers[1] if len(numbers) >= 2 else '0'
    second = numbers[2] if len(numbers) >= 3 else '0'
    frac_seconds = numbers[3] if len(numbers) >= 4 else '0'
    
    second += "." + frac_seconds
    return (int(degree), float(minute), float(second))


def obtener_angulos_asimov(angulos_corregidos, asimov_base):
    angulos_asimov = asimov_base
    yield(angulos_asimov if angulos_asimov<360 else angulos_asimov - 360)
    for angulo in angulos_corregidos:
        angulos_asimov = angulos_asimov-180+angulo if angulos_asimov>180 else angulos_asimov+180+angulo
        yield(angulos_asimov if angulos_asimov<360 else angulos_asimov - 360)

def preguntar_angulos(n):
    for i in range(0,n):
        angulo = gmd_a_decimal(*parse_gmd_texto(input( str(i+1) + ": " )))
        yield(angulo)

def hallar_proyeccion(distancia, angulo):
    proyeccion_ns = math.cos(math.radians(angulo))*distancia
    proyeccion_ew = math.sin(math.radians(angulo))*distancia
    return proyeccion_ns, proyeccion_ew

def hallar_proyecciones(distancias,angulos):
    for distancia, angulo in zip(distancias, angulos):
        yield(hallar_proyeccion(distancia, angulo))

def preguntar_distancias(n):
    for i in range(n):
        yield(float(input("")))

print("Ingrese el angulo asimov base en grados, minutos y segundos de cada vertice: ")
angulo_asimov_base = list(preguntar_angulos(1))[0]

print("Ingrese el angulo externo en grados, minutos y segundos de cada vertice: ")
angulos_observados = list(preguntar_angulos(n))

suma_observable = sum(angulos_observados)

correcion_angular = (suma_teorica-suma_observable)/n

print("Correcion angular: "+ str(correcion_angular))

angulos_corregidos = list(map(lambda angulo : angulo+correcion_angular, angulos_observados))

angulos_asimov = list(obtener_angulos_asimov(angulos_corregidos,angulo_asimov_base))

print("Asimut para cada vertice:")
print([decimal_a_gmd(angulo) for angulo in angulos_asimov])
# Preguntar distancia entre vertices y coordenada base

print("Ingrese la distancia entre los vertices:")
distancias = list(preguntar_distancias(n))
proyecciones = list(hallar_proyecciones(distancias, angulos_asimov))
suma_distancias = sum(distancias)

for ns, ew in proyecciones:
    deltas_ns += ns
    deltas_ew += ew
    suma_proyecciones_ns += math.fabs(ns) 
    suma_proyecciones_ew += math.fabs(ew)

correcion_unitaria_ns = deltas_ns/suma_proyecciones_ns
correcion_unitaria_ew = deltas_ew/suma_proyecciones_ew

print("Correccion unitaria:")
print((correcion_unitaria_ns,correcion_unitaria_ew))

error_de_cierre_de_la_poligonal = ((deltas_ew*deltas_ew)+(deltas_ns*deltas_ns))**(1/2)

print("Error de cierre de la poligonal:")
print(error_de_cierre_de_la_poligonal)

precision = suma_distancias/error_de_cierre_de_la_poligonal

print("Precision:")
print(precision)


proyecciones_corregidas = list(map(
    lambda ns_ew:(
        ns_ew[0] - math.fabs(ns_ew[0])*correcion_unitaria_ns,
        ns_ew[1] - math.fabs(ns_ew[1])*correcion_unitaria_ew
    ), proyecciones))


print("Proyecciones en terreno:")
print(proyecciones)


print("Proyecciones corregidas:")
print(list(proyecciones_corregidas))

coordenada_ns = int(input("Ingrese la coordenada norte:"))
coordenada_ew = int(input("Ingrese la coordenada este:"))

coordenadas_ns = [coordenada_ns]
coordenadas_ew = [coordenada_ew]

for ns, ew in proyecciones_corregidas:
    coordenada_ns = coordenada_ns + ns
    coordenadas_ns.append(coordenada_ns)
    coordenada_ew = coordenada_ew + ew
    coordenadas_ew.append(coordenada_ew)

print("Coordenadas: ")
print(list(zip(coordenadas_ns,coordenadas_ew)))