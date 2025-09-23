# -*- coding: utf-8 -*-
"""
Created on Tue May 30 20:09:29 2023

@author: mquevedo
"""

import pandas as pd
import numpy as np

centrales = pd.read_pickle(r'centrales.pkl')

deptos=centrales.Fuente.value_counts()

centrales = centrales.drop(centrales[centrales['DepartamentoProc']==""].index)


alimentos_centrales=centrales.copy()


alimentos_centrales = alimentos_centrales.drop(alimentos_centrales[alimentos_centrales['Alimento']=="Frutas importadas otras"].index)

alimentos_centrales['Fuente'] = np.where(alimentos_centrales['Fuente'] == "Bogotá, D.C., Corabastos", "Bogotá D.C., Corabastos", alimentos_centrales['Fuente'])

alimentos_centrales[['Ciudad','Central']]=alimentos_centrales.Fuente.str.split(',',expand=True)


grupo=alimentos_centrales.groupby(['Cod_MunicipioProc', 'Alimento','Año','Ciudad'])['CantKg'].sum()

agrupado = pd.DataFrame(grupo)
agrupado = agrupado.reset_index()

agrupado.to_excel("Centrales_agrupado_fuente.xlsx") 

Final = pd.read_excel('Centrales_agrupado_fuente.xlsx')
grupo_final=Final.groupby(['Cod_MunicipioProc', 'Grupo','Año','Ciudad'])['CantKg'].sum()

grupo_final = pd.DataFrame(grupo_final)
grupo_final = grupo_final.reset_index()


grupo_final.to_excel("Abastecimiento_real.xlsx") 

Abastecimiento_real = pd.read_excel('Abastecimiento_real.xlsx')
