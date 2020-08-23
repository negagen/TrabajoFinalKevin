import re, math, pprint

n = int(input("Ingrese el numero de vertices: "))

deltas_ns = 0
deltas_ew = 0
suma_proyecciones_ns = 0
suma_proyecciones_ew = 0

suma_teorica = (n+2)*180 

pp = pprint.PrettyPrinter(indent=4)

def arreglar_angulo(angulo):
    if(angulo>=360):
        return arreglar_angulo(angulo-360)
    elif (angulo<0):
        return arreglar_angulo(angulo+360)
    else:
        return angulo

def decimal_a_gms(angulo_decimal ):
    minutos, grados  = math.modf(angulo_decimal)
    segundos, minutos = math.modf(minutos*60)
    segundos = segundos*60
    return (grados, minutos, segundos)


def gms_a_decimal(grados, minutos, segundos):
    return grados + minutos / 60 + segundos / 3600


def parse_gms_texto(dms_str):
    numbers = [*filter(len, re.split('\D+', dms_str, maxsplit=4))]

    degree = numbers[0]
    minute = numbers[1] if len(numbers) >= 2 else '0'
    second = numbers[2] if len(numbers) >= 3 else '0'
    frac_seconds = numbers[3] if len(numbers) >= 4 else '0'
    
    second += "." + frac_seconds
    return (int(degree), float(minute), float(second))


def obtener_angulos_azimut(angulos_corregidos, azimut_base):
    angulos_azimut = azimut_base
    yield(arreglar_angulo(angulos_azimut))
    for angulo in angulos_corregidos:
        angulos_azimut = angulos_azimut-180+angulo if angulos_azimut>180 else angulos_azimut+180+angulo
        yield(arreglar_angulo(angulos_azimut))

def preguntar_angulos(n):
    for i in range(0,n):
        angulo = gms_a_decimal(*parse_gms_texto(input( str(i+1) + ": " )))
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

print("Ingrese el angulo azimut base en grados, minutos y segundos de cada vertice: ")
angulo_azimut_base = list(preguntar_angulos(1))[0]

print("Ingrese el angulo externo en grados, minutos y segundos de cada vertice: ")
angulos_observados = list(preguntar_angulos(n))

suma_observable = sum(angulos_observados)

correcion_angular = (suma_teorica-suma_observable)/n

print("Correcion angular: "+ str(round(correcion_angular,6)))

angulos_corregidos = list(map(lambda angulo : angulo+correcion_angular, angulos_observados))

angulos_azimut = list(obtener_angulos_azimut(angulos_corregidos,angulo_azimut_base))

print("Angulos corregidos para cada vertice:")
for grado, minuto, segundo in [decimal_a_gms(angulo) for angulo in angulos_corregidos]:
    print("{}°\t{}'\t{}\"".format(int(grado),int(minuto),round(segundo)))

print("Azimut para cada vertice:")
for grado, minuto, segundo in [decimal_a_gms(angulo) for angulo in angulos_azimut]:
    print("{}°\t{}'\t{}\"".format(int(grado),int(minuto),round(segundo)))


print("Ingrese la distancia entre los vertices:")
distancias = list(preguntar_distancias(n))
proyecciones = list(hallar_proyecciones(distancias, angulos_azimut))
suma_distancias = sum(distancias)

for ns, ew in proyecciones:
    deltas_ns += ns
    deltas_ew += ew
    suma_proyecciones_ns += math.fabs(ns) 
    suma_proyecciones_ew += math.fabs(ew)

correcion_unitaria_ns = deltas_ns/suma_proyecciones_ns
correcion_unitaria_ew = deltas_ew/suma_proyecciones_ew

error_de_cierre_de_la_poligonal = ((deltas_ew*deltas_ew)+(deltas_ns*deltas_ns))**(1/2)

precision = suma_distancias/error_de_cierre_de_la_poligonal

proyecciones_corregidas = list(map(
    lambda ns_ew:(
        ns_ew[0] - math.fabs(ns_ew[0])*correcion_unitaria_ns,
        ns_ew[1] - math.fabs(ns_ew[1])*correcion_unitaria_ew
    ), proyecciones))


print("Proyecciones en terreno:")
pp.pprint([(round(proyeccion[0],3),round(proyeccion[1],3)) for proyeccion in proyecciones])

print("Correccion unitaria:")
pp.pprint((round(correcion_unitaria_ns,5),round(correcion_unitaria_ew,5)))

print("Proyecciones corregidas:")
pp.pprint([(round(proyeccion[0],3),round(proyeccion[1],3)) for proyeccion in proyecciones_corregidas])

print("Error de cierre de la poligonal:")
print(round(error_de_cierre_de_la_poligonal,3))

print("Precision:")
print("1:{}".format(round(precision)))

coordenada_ns = float(input("Ingrese la coordenada norte:"))
coordenada_ew = float(input("Ingrese la coordenada este:"))

coordenadas_ns = [coordenada_ns]
coordenadas_ew = [coordenada_ew]

for ns, ew in proyecciones_corregidas:
    coordenada_ns = coordenada_ns + ns
    coordenadas_ns.append(coordenada_ns)
    coordenada_ew = coordenada_ew + ew
    coordenadas_ew.append(coordenada_ew)

print("Coordenadas: ")
pp.pprint([(round(coordenadas[0],3),round(coordenadas[1],3)) for coordenadas in list(zip(coordenadas_ns,coordenadas_ew))])