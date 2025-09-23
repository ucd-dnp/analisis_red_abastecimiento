# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np

df = pd.read_stata('2019_2023_01_20.dta') 

centrales = df.copy()

df_2=df.groupby(['Fuente'])['Fuente'].count()
df_2 = df_2.reset_index(drop=True)


#Eliminar grupos
centrales = centrales.drop(centrales[centrales['Grupo']==""].index)

#Eliminar alimentos
centrales = centrales.drop(centrales[centrales['Alimento']=="Cervezas"].index)
centrales = centrales.reset_index(drop=True)

centrales["Fecha"]= centrales["FechaEncuesta"].astype(str)

centrales["Año"] = centrales['Fecha'].apply(lambda x: x[0:4])

centrales=centrales.drop(['FechaEncuesta', 'Fecha', 'Fecha_2'], axis=1)

centrales.to_pickle('centrales.pkl')

deptos=alimentos_centrales.Fuente.value_counts()

centrales = centrales.drop(centrales[centrales['DepartamentoProc']==""].index)


alimentos_centrales=centrales.copy()

alimentos_centrales=alimentos_centrales.drop(['Cod_DeptoProc', 'Cod_MunicipioProc', 'DepartamentoProc', 'MunicipioProc'], axis=1)

alimentos_centrales = alimentos_centrales.drop(alimentos_centrales[alimentos_centrales['Alimento']=="Frutas importadas otras"].index)

alimentos_centrales['Fuente'] = np.where(alimentos_centrales['Fuente'] == "Bogotá, D.C., Plaza Las Flores", "Bogotá D.C., Plaza Las Flores", alimentos_centrales['Fuente'])

alimentos_centrales[['Ciudad','Central']]=alimentos_centrales.Fuente.str.split(',',expand=True)

alimentos_centrales.to_pickle('alimentos_centrales.pkl')

grupo=alimentos_centrales.groupby(['Ciudad', 'Alimento','Año'])['CantKg'].sum()

agrupado = pd.DataFrame(grupo)
agrupado = agrupado.reset_index()

agrupado.to_excel("agrupado_2.xlsx") 


#########################
Produccion = pd.read_excel('Produccion.xlsx')

grupo_prod=Produccion.groupby(['Cultivo', 'CodMun','Municipio','Año'])['Produccion t'].sum()

produccion_grupo = pd.DataFrame(grupo_prod)
produccion_grupo = produccion_grupo.reset_index()

produccion_grupo.to_excel("produccion_grupo.xlsx") 


######Agrupar produccion

Centrales = pd.read_excel('Centrales_agrupado.xlsx')
Productores = pd.read_excel('Produccion_grupo.xlsx')

Centrales_gr_alimentos=Centrales.groupby(['Ciudad', 'Año','grupo'])['CantKg'].sum()
Centrales_gr_alimentos = pd.DataFrame(Centrales_gr_alimentos)
Centrales_gr_alimentos = Centrales_gr_alimentos.reset_index()
Centrales_gr_alimentos.to_excel("Centrales_gr_alimentos.xlsx") 


Productores_gr_alimentos=Productores.groupby(['CodMun', 'Municipio','Año','Grupo'])['ProduccionKg'].sum()
Productores_gr_alimentos = pd.DataFrame(Productores_gr_alimentos)
Productores_gr_alimentos = Productores_gr_alimentos.reset_index()
Productores_gr_alimentos.to_excel("Productores_gr_alimentos.xlsx") 

Productores_gr_alimentos = pd.read_excel('Productores_gr_alimentos.xlsx')

Centrales_gr_alimentos = pd.read_excel('Centrales_gr_alimentos.xlsx')

Total=pd.merge(Centrales_gr_alimentos, Productores_gr_alimentos, on='AñoGrupo')

Datos_total = pd.read_excel('Total.xlsx')

Datos_total.drop(Datos_total[(Datos_total['Municipio_productor'] =="Inírida") & (Datos_total['Tiempo'] == 0)].index, inplace=True)

cercanos = Datos_total.sort_values('Tiempo', ascending=True).groupby(['Año_x',"grupo","Ciudad_central"]).head(2).sort_index()

cercanos = cercanos.sort_values(['Año_x',"grupo","Ciudad_central",'Tiempo'])
cercanos.to_excel("cercanos.xlsx")

sum_produccion=cercanos.groupby(['CodMun_y', 'Año_x','grupo'])['CantKg'].sum()
sum_produccion = pd.DataFrame(sum_produccion)
sum_produccion = sum_produccion.reset_index()
sum_produccion.to_excel("sum_produccion.xlsx") 







