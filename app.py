import re, math

n = int(input("Ingrese el numero de vertices: "))

angulos_observados = []
suma_teorica = (n+2)*180
suma_observable = 0

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


print("Ingrese el angulo externo en grados, minutos y segundos de cada vertice: ")
for i in range(0,n+1):
    angulo = gmd_a_decimal(*parse_gmd_texto(input( str(i+1) + ": " )))
    suma_observable += angulo if i>0 else 0
    print(suma_observable)
    angulos_observados.append(angulo)

correcion_angular = (suma_teorica-suma_observable)/n

angulos_corregidos = list(map(lambda angulo : angulo+correcion_angular, angulos_observados[1:]))        

angulos_asimov = list(obtener_angulos_asimov(angulos_corregidos,angulos_observados[0]))

# Preguntar distancia entre vertices y coordenada base

print(angulos_observados)
print(angulos_corregidos)
print(angulos_asimov)
