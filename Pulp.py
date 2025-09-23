# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 14:46:25 2023

@author: mquevedo
"""


import pandas as pd
from pulp import *

#Abrir datos
Total = pd.read_excel('Total.xlsx')
#Establecer año
Total_2020= Total.drop(Total[Total['Año_x']!=2021].index)
Total=Total_2020

grupos=["Annonaceas","Araceas","Caducifolios","Cereales","Cítricos",
"Condimentos","Cultivos Tropicales Tradicionales","Demas frutales",
"Hortalizas de Flor","Hortalizas de Fruto","Hortalizas de Hoja",
"Hortalizas de raíz","Hortalizas de Tallo","Leguminosas",
"Myrtaceas","Passifloraceas","Raíces y Tubérculos","Solanaceas"]

matriz_final= pd.DataFrame()

for g in grupos:   
    
    #Prueba 
    prueba = Total.drop(Total[Total['grupo']!=g].index)
    
    #Extraer origen y destino en listas
    origen=list(prueba["CodMun_y"])
    origen=pd.unique(origen)
    origen=list(origen)
    
    destino=list(prueba["CodMun_x"])
    destino=pd.unique(destino)
    destino=list(destino)
        
    ##Oferta 
    Productores = pd.read_excel('Productores_gr_alimentos.xlsx')
    Productores = Productores.drop(Productores[Productores['Grupo']!=g].index)
    Productores = Productores.drop(Productores[Productores['Año']!=2021].index)
    
    Productores=Productores.drop(['Municipio', 'Año',"Grupo"], axis=1)
    
    oferta = Productores.set_index('CodMun').T.to_dict("records")
    oferta=oferta[0]
    
    
    #Demanda
    Centrales = pd.read_excel('Centrales_gr_alimentos.xlsx')
    Centrales = Centrales.drop(Centrales[Centrales['grupo']!=g].index)
    Centrales = Centrales.drop(Centrales[Centrales['Año']!=2021].index)
    
    Centrales=Centrales.drop(['Ciudad', 'Año',"grupo"], axis=1)
    
    demanda = Centrales.set_index('CodMun').T.to_dict("records")
    demanda=demanda[0]
    
    #Tiempos
    Tiempos = pd.read_excel('Costo_tiempo.xlsx')
    Tiempos = Tiempos.set_index('Origen').to_dict("index")
    
    prob = LpProblem('Abastecimiento', LpMinimize)
    
    rutas = [(i,j) for i in origen for j in destino]
    
    cantidad = LpVariable.dicts('Cantidad de Envio',(origen,destino),0)
    
    prob += lpSum(cantidad[i][j]*Tiempos[i][j] for (i,j) in rutas)
    
    for j in destino:
        prob += lpSum(cantidad[i][j] for i in origen) >= demanda[j]
        
    for i in origen:
        prob += lpSum(cantidad[i][j] for j in destino) <= oferta[i]
        
    ### Resolvemos e imprimimos el Status, si es Optimo, el problema tiene solución.
    prob.solve()
    print("Status:", LpStatus[prob.status])
    
    
    ### Imprimimos la solución
    trayecto=[]
    toneladas=[]
    for v in prob.variables():
        if v.varValue > 0:           
            t=v.name
            c=v.varValue
            trayecto.append(t)
            toneladas.append(c)
            grupo=[g]*len(trayecto)              
    
    matriz = pd.DataFrame((zip(trayecto,toneladas,grupo)), columns = ['trayecto','toneladas',"grupo"])

    matriz_final = pd.concat([matriz_final, matriz])

matriz_final.to_excel("20211.xlsx") 

