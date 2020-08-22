import re

n = int(input("Ingrese el numero de vertices: "))

angulos_observados = []
suma_teorica = (n+2)*180
suma_observable = 0

print("Ingrese el angulo externo en grados, minutos y segundos de cada vertice: ")
for i in range(0,n+1):
    dms_str = input( str(i+1) + ":" )
    
    numbers = [*filter(len, re.split('\D+', dms_str, maxsplit=4))]

    degree = numbers[0]
    minute = numbers[1] if len(numbers) >= 2 else '0'
    second = numbers[2] if len(numbers) >= 3 else '0'
    frac_seconds = numbers[3] if len(numbers) >= 4 else '0'
    
    second += "." + frac_seconds
    
    angulo = int(degree) + float(minute) / 60 + float(second) / 3600
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
