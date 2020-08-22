import re, math

n = int(input("Ingrese el numero de vertices: "))

angulo = dict()

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


angulos_observados = []
suma_teorica = (n+2)*180
suma_observable = 0

print("Ingrese el angulo externo en grados, minutos y segundos de cada vertice: ")
for i in range(0,n+1):
    angulo = gmd_a_decimal(*parse_gmd_texto(input( str(i+1) + ":" )))
    suma_observable += angulo if i>0 else 0
    print(suma_observable)
    angulos_observados.append(angulo)

correcion_angular = (suma_teorica-suma_observable)/n

angulos_corregidos = list(map(lambda angulo : angulo+correcion_angular, angulos_observados[1:]))        

angulos_asimov = list([0]*(n+1))
angulos_asimov[0] = angulos_observados[0]

def obtener_angulos_asimov(angulos_corregidos, angulos_asimov):
    for i in range(1,n+1):
        print(i)
        angulos_asimov[i] = angulos_asimov[i-1]-180+angulos_corregidos[i-1] if angulos_asimov[i-1]>180 else angulos_asimov[i-1]+180+angulos_corregidos[i-1]

obtener_angulos_asimov(angulos_corregidos,angulos_asimov)
angulos_asimov = list(map(lambda angulo: angulo if angulo<360 else angulo - 360,angulos_asimov))


print(angulos_observados)
print(angulos_corregidos)
print(angulos_asimov)
