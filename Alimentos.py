# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 16:26:16 2023

@author: mquevedo
"""

import pandas as pd
import numpy as np
from pulp import *

centrales = pd.read_stata('2019_2023_01_20.dta') 
eva = pd.read_excel('EVA.xlsx')

df = centrales.copy()

#Extraer año

df["Fecha"]= df["FechaEncuesta"].astype(str)

df["Año"] = df['Fecha'].apply(lambda x: x[0:4])

df=df.drop(['FechaEncuesta', 'Fecha', 'Cod_DeptoProc',"DepartamentoProc"], axis=1)

df = df.drop(df[df['Año']=="NaT"].index)

df["CantTn"]=df['CantKg']/1000

df=df.drop(['CantKg'], axis=1)

alimento_necesario=df.groupby(['Fuente', 'Cod_MunicipioProc','MunicipioProc',"Alimento","Año"])['CantTn'].sum()

alimento_necesario = pd.DataFrame(alimento_necesario)
alimento_necesario = alimento_necesario.reset_index()
alimento_necesario.to_excel("tiempo_antes.xlsx") 

tiempo_antes = pd.read_excel('tiempo_antes.xlsx')

tiempo_antes_grupo=tiempo_antes.groupby(['Cod_central', 'Alimento','Año'])['Tiempo'].sum()
tiempo_antes_grupo = pd.DataFrame(tiempo_antes_grupo)
tiempo_antes_grupo = tiempo_antes_grupo.reset_index()
tiempo_antes_grupo.to_excel("tiempo_antes_tiempo.xlsx") 

tiempo_despues= pd.read_excel('Optimo_alimento.xlsx')

tiempo_antes_grupo=tiempo_despues.groupby(['Cod_central', 'Grupo','Año'])['Tiempo'].sum()
tiempo_antes_grupo = pd.DataFrame(tiempo_antes_grupo)
tiempo_antes_grupo = tiempo_antes_grupo.reset_index()
tiempo_antes_grupo.to_excel("tiempo_despues_tiempo.xlsx") 


datos_centrales= datos_centrales.drop(datos_centrales[datos_centrales['Alimento']=="Verduras y hortalizas otras"].index)

datos_centrales=datos_centrales.replace({"Tomate de árbol": "Tomatearbol"})

fuente= datos_centrales["Fuente"].str.split(expand=True)
fuente.columns = ['Ciudad', 'central1', 'central2', 'central3', 'central4', 'central5', 'central6']

datos_centrales["Ciudad"]=fuente["Ciudad"]

datos_centrales= datos_centrales.drop(datos_centrales[datos_centrales['Año']=="2023"].index)

datos_centrales=datos_centrales.drop(['Fuente'], axis=1)

grupo_centrales=datos_centrales.groupby(['Ciudad', 'Cod_MunicipioProc','MunicipioProc','Alimento','Año'])['CantTn'].sum()

ciudad_grupo = pd.DataFrame(grupo_centrales)

ciudad_grupo = ciudad_grupo.reset_index()

ciudad_grupo.to_excel("ciudad_grupo.xlsx") 

Base_eva = pd.read_excel('Base_eva_abastecidos.xlsx')
Base_centrales = pd.read_excel('alimento_necesario_abastecidos.xlsx')




#Alimento necesario para centrales por año
alimento_necesario=Base_centrales.groupby(['Ciudad', 'Alimento','Año'])['CantTn'].sum()
alimento_necesario = pd.DataFrame(alimento_necesario)
alimento_necesario = alimento_necesario.reset_index()
alimento_necesario.to_excel("alimento_necesario.xlsx") 
alimento_necesario = pd.read_excel('alimento_necesario.xlsx')

#Crear matriz total
Total=pd.merge(Base_centrales, Base_eva, on='Año_alimento')
Total=Total.drop(['Unnamed: 0',"Año_alimento","Cultivo","Año_x"], axis=1)

Total.to_excel("Total_alimentos_abastecidos.xlsx") 

Total = pd.read_excel('Total_alimentos_abastecidos.xlsx')



central_alimentos= pd.read_excel('central_alimentos.xlsx')


#Abrir datos
Datos = pd.read_excel('Total_alimentos_abastecidos.xlsx')


#Establecer año
Total= Datos.drop(Datos[Datos['Año_y']!=2021].index)

grupos=list(Total["Alimento"])
grupos=pd.unique(grupos)
grupos=list(grupos)

matriz_final= pd.DataFrame()

for g in grupos:   
    
    #Prueba 
    prueba = Total.drop(Total[Total['Alimento']!=g].index)
    
    #Extraer origen y destino en listas
    origen=list(prueba["CodMun"])
    origen=pd.unique(origen)
    origen=list(origen)
    
    destino=list(prueba["CodCiudad"])
    destino=pd.unique(destino)
    destino=list(destino)
        
    ##Oferta 
    Productores = pd.read_excel('Base_eva_abastecidos.xlsx')
    Productores = Productores.drop(Productores[Productores['Cultivo']!=g].index)
    Productores = Productores.drop(Productores[Productores['Año']!=2021].index)
    
    Productores=Productores.drop(['Año',"Cultivo","Grupo", "Año_alimento", "Municipio"], axis=1)
    
    oferta = Productores.set_index('CodMun').T.to_dict("records")
    oferta=oferta[0]
    
    
    #Demanda
    Centrales = pd.read_excel('alimento_necesario_abastecidos.xlsx')
    Centrales = Centrales.drop(Centrales[Centrales['Alimento']!=g].index)
    Centrales = Centrales.drop(Centrales[Centrales['Año']!=2021].index)
    
    Centrales=Centrales.drop(['Alimento',"Año", "Año_alimento","Ciudad"], axis=1)
    
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

matriz_final.to_excel("2021.xlsx") 


