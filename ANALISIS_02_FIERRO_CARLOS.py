# -*- coding: utf-8 -*-
"""
@author: carlos
"""
import csv

# La siguiente función ayuda al usuario a definir que reporte quiere 
# generar
def elegir_reporte():
    print("¿Qué reporte desea generar?")
    print("-----------------------------------------------")
    print("1) Rutas de importación y exportación")
    print("2) Medio de transporte utilizado")
    print("3) Valor total de importaciones y exportaciones")
    print("-----------------------------------------------")
    reporte = int(input("Indique con número: "))
    print("-----------------------------------------------")
    print("-----------------------------------------------")
    return reporte

reporte = elegir_reporte()

# Creamos con este pedazo de código una lista que contiene todas las rutas
rutas = set()
with open("synergy_logistics_database.csv","r") as archivo_madre:
    lector = csv.DictReader(archivo_madre)
    for linea in lector:
        if (linea["destination"],linea["origin"]) not in rutas:
            tupla_de_ruta = (linea["origin"],linea["destination"])
            rutas.add(tupla_de_ruta)
rutas = list(rutas)
rutas.sort()


# Definimos función que calcule el total de exportaciones o importaciones
# por año para cada ruta 
def demanda_anual(ano,tipo):
    resultado_final = []
    with open("synergy_logistics_database.csv","r") as archivo_madre:
        lector = csv.DictReader(archivo_madre)
        for linea in lector:
            if int(linea["year"]) == ano and linea["direction"] == tipo:
                for ruta in rutas:
                    if ruta == (linea["origin"],linea["destination"]) or ruta == (linea["destination"],linea["origin"]):
                        resultado_final.append((ruta,int(linea["total_value"])))
    resultado_final.sort(key=lambda x: x[0],reverse=True)
    suma_final = []
    suma = resultado_final[0][1]
    for j in range(len(resultado_final)-1):
        if resultado_final[j][0] == resultado_final[j+1][0]:
            suma += resultado_final[j+1][1]
        else:
            suma_final.append((resultado_final[j][0],suma))
            suma = resultado_final[j+1][1]
    if resultado_final[-2][0] == resultado_final[-1][0]:
        suma_final.append((resultado_final[-2][0],suma))
    else:
        suma_final.append((resultado_final[-1][0],resultado_final[-1][1]))
    suma_final.sort(key=lambda x: x[1],reverse=True)
    return suma_final
# suma_final contiene todas las exportaciones o importaciones por rutas
# del año indicado.


# Creamos con este pedazo de código una lista que contiene todos los
# diferentes medios de transporte
transportes = set()
with open("synergy_logistics_database.csv","r") as archivo_madre:
    lector = csv.DictReader(archivo_madre)
    for linea in lector:
        if linea["transport_mode"] not in transportes:
            valor_de_ruta = linea["transport_mode"]
            transportes.add(valor_de_ruta)
transportes = list(transportes)
transportes.sort()


# La siguiente función ayuda a calcular el total de exportaciones más 
# importaciones por año para cada medio de transporte
def total_medios(ano):
    resultado_final = []
    with open("synergy_logistics_database.csv","r") as archivo_madre:
        lector = csv.DictReader(archivo_madre)
        for linea in lector:
            if int(linea["year"]) == ano:
                for transporte in transportes:
                    if transporte == linea["transport_mode"]:
                        resultado_final.append((transporte,int(linea["total_value"])))
    resultado_final.sort(key=lambda x: x[0],reverse=True)
    suma_final = []
    suma = resultado_final[0][1]
    for j in range(len(resultado_final)-1):
        if resultado_final[j][0] == resultado_final[j+1][0]:
            suma += resultado_final[j+1][1]
        else:
            suma_final.append((resultado_final[j][0],suma))
            suma = resultado_final[j+1][1]
    if resultado_final[-2][0] == resultado_final[-1][0]:
        suma_final.append((resultado_final[-2][0],suma))
    else:
        suma_final.append((resultado_final[-1][0],resultado_final[-1][1]))
    suma_final.sort(key=lambda x: x[1],reverse=True)
    return suma_final
# suma_final contiene todas las exportaciones e importaciones por medio
# de transporte para el año indicado.


# Creamos con este pedazo de código una lista que contiene todos los
# diferentes países de exportación e importación
paises = set()
with open("synergy_logistics_database.csv","r") as archivo_madre:
    lector = csv.DictReader(archivo_madre)
    for linea in lector:
        if linea["origin"] not in paises:
            valor_de_pais = linea["origin"]
            paises.add(valor_de_pais)
        if linea["destination"] not in paises:
            valor_de_pais = linea["destination"]
            paises.add(valor_de_pais)
paises = list(paises)
paises.sort()


# Definimos función que calcule el total de importaciones y exportaciones
# para un año determinado.
def total_exp_imp(ano):
    suma_final = 0
    with open("synergy_logistics_database.csv","r") as archivo_madre:
        lector = csv.DictReader(archivo_madre)
        for linea in lector:
            if int(linea["year"]) == ano:
                suma_final += int(linea["total_value"])
    return suma_final


# Definimos funcion que calcule, para un año determinado, el porcentaje
# que contribuyó cada país al total de exportaciones e importaciones.
def contribucion(ano):
    expos_total = total_exp_imp(ano)
    resultado_final = []
    with open("synergy_logistics_database.csv","r") as archivo_madre:
        lector = csv.DictReader(archivo_madre)
        for linea in lector:
            if int(linea["year"]) == ano:
                for pais in paises:
                    if pais == linea["origin"] or pais == linea["destination"]:
                        resultado_final.append((pais,int(linea["total_value"])))
    resultado_final.sort(key=lambda x: x[0],reverse=True)
    suma_final = []
    suma = resultado_final[0][1]
    for j in range(len(resultado_final)-1):
        if resultado_final[j][0] == resultado_final[j+1][0]:
            suma += resultado_final[j+1][1]
        else:
            suma_final.append((resultado_final[j][0],suma*100/expos_total))
            suma = resultado_final[j+1][1]
    if resultado_final[-2][0] == resultado_final[-1][0]:
        suma_final.append((resultado_final[-2][0],suma*100/expos_total))
    else:
        suma_final.append((resultado_final[-1][0],resultado_final[-1][1]*100/expos_total))
    suma_final.sort(key=lambda x: x[1],reverse=True)
    return suma_final
# suma_final contiene todas las exportaciones o importaciones por rutas
# del año indicado.


# Este código genera e imprime en pantalla los reportes.
login = True
while login == True:
    if reporte == 1:
        print("RUTAS DE IMPORTACIÓN Y EXPORTACIÓN")
        print("-----------------------------------------------")
        for i in [2015,2016,2017,2018,2019,2020]:
            print("-----------------------------------------------")
            print("Las siguientes son las diez rutas más demandadas de exportación del ",i)
            print("-----------------------------------------------")
            expos = demanda_anual(i,"Exports")
            print("Ruta            Cantidad")
            for j in range(10):
                print(f"{expos[j][0][0]}-{expos[j][0][1]}     {expos[j][1]}")
        for i in [2015,2016,2017,2018,2019,2020]:
            print("-----------------------------------------------")
            print("Las siguientes son las diez rutas más demandadas de importación del ",i)
            print("-----------------------------------------------")
            imports = demanda_anual(i,"Imports")
            print("Ruta            Cantidad")
            for j in range(10):
                print(f"{imports[j][0][0]}-{imports[j][0][1]}     {imports[j][1]}")
    
    
    if reporte == 2:
        print("METODO DE TRANSPORTE UTILIZADO")
        print("-----------------------------------------------")
        for i in [2015,2016,2017,2018,2019,2020]:
            print("-----------------------------------------------")
            print("Medios de transporte por volumen de importación y exportación para el ",i)
            print("-----------------------------------------------")
            transpos = total_medios(i)
            print("Transporte      Exportación+Importación")
            for j in range(4):
                print(f"{transpos[j][0]}     {transpos[j][1]}")

    
    if reporte == 3:
        print("VALOR TOTAL DE IMPORTACIONES Y EXPORTACIONES")
        print("-----------------------------------------------")
        for i in [2015,2016,2017,2018,2019,2020]:
            print("-----------------------------------------------")
            print("Lista de países que contribuyeron con el 80% de todas las importaciones y exportaciones para el año ",i)
            print("-----------------------------------------------")
            contribuciones = contribucion(i)
            print("País      Contribución (%)")
            lim = contribuciones[0][1]
            for w in range(len(contribuciones)):
                if lim < 80.0:
                    print(f"{contribuciones[w][0]}     {round(contribuciones[w][1],2)}")
                    lim += contribuciones[w+1][1]
        
    
    
    print("--------------------------------------------")
    print("¿Desea generar otro reporte? (si/no)")
    respuesta = input("Indique su respuesta: ")
    print("--------------------------------------------")
    if respuesta == "si":
        reporte = elegir_reporte()
    elif respuesta == "no":
        print("Programa cerrado exitosamente")
        login = False
        
    
