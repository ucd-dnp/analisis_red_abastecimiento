# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 10:34:36 2023

@author: mquevedo
"""


#pip install -U kaleido
# pip install streamlit
# pip install pickle-mixin
# pip install scikit-learn
#pip install pyproj
#pip install folium
#pip install streamlit-folium
#pip install streamlit-extras



#importar librerías
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
from plotly.graph_objs import *
import plotly.io as pio
import streamlit as st
import plotly.express as px
import plotly.offline
import folium
from streamlit_folium import st_folium
from PIL import Image
from streamlit_extras.metric_cards import style_metric_cards
from branca.element import Figure

st.set_page_config(layout="wide")
    
col1, col2, col3 = st.columns(3)

Colombia= Image.open('Colombia.png')

DNP = Image.open('DNP.png')

with col1:
    st.image(Colombia)

with col2:
    st.write("                                                            ")

with col3:
    st.image(DNP)

st.title('Rutas de abastecimiento de alimentos en Colombia')

# Crear pestañas
titulos_pestanas = ['Principal', 'Acerca de']
pestaña1, pestaña2= st.tabs(titulos_pestanas)
 

with pestaña1:
    
    analisis = st.radio(
        "Seleccione el tipo de análisis",
        ('Grupo de alimentos', 'Alimentos'))
    
    st.divider()
    
    if analisis == 'Grupo de alimentos':
        from annotated_text import annotated_text

        
        #Ubicacion de los filtros
        Ciudad, Año, Grupo= st.columns([5, 5, 5])
        
        #filtro de grupo, ciudad y año
        
        with Ciudad:
            Ciudad_choice = st.selectbox(
                  'Seleccione una ciudad con central de abastos',
                  ("Armenia","Barranquilla","Bogotá","Bucaramanga","Cali",
                          "Cartagena de Indias","Cúcuta","Ibagué","Ipiales","Manizales",
                          "Medellín","Montería","Neiva","Pasto","Pereira","Popayán",
                          "Santa Marta","Sincelejo","Tunja","Valledupar","Villavicencio"))
            
        with Año:
             Año_choice = st.selectbox(
                   'Seleccione un año',
                   (2019,2020,2021))
            
        Grupo_lista = pd.read_excel('Optimizado.xlsx')
        Filtro_grupo = Grupo_lista[(Grupo_lista.Nombre_ciudad == Ciudad_choice)]
        Filtro_grupo = Filtro_grupo[(Filtro_grupo.Año == Año_choice)]
        
        grupo_ciudad=list(Filtro_grupo["Grupo"])
        grupo_ciudad=pd.unique(grupo_ciudad)
        grupo_ciudad=list(grupo_ciudad)    
        
    
        with Grupo:
            Grupo_choice = st.selectbox(
                  'Seleccione un grupo de alimentos',
                  (grupo_ciudad))
        
        st.subheader("")
        
        if Año_choice!=2021:
            
            indicadores = pd.read_excel('Indicadores.xlsx')
            
            indicadores_filtro = indicadores[(indicadores.Central == Ciudad_choice)]
            indicadores_filtro = indicadores_filtro[(indicadores_filtro.Grupo == Grupo_choice)]
            indicadores_filtro = indicadores_filtro[(indicadores_filtro.Año == Año_choice)]
    
            col1, col2, col3 = st.columns(3)
            col1.metric("Toneladas necesarias", round(indicadores_filtro["Toneladas_necesarias"],2))
            col2.metric("Horas de abastecimiento", indicadores_filtro["Tiempo_antes"])
            col3.metric("Centrales de abasto", indicadores_filtro["Numero_centrales"])
            style_metric_cards()
            

            #leer datos
            Coordenadas = pd.read_excel('Datos_total.xlsx')
            
            #filtrar datos
            Total_filtro = Coordenadas[(Coordenadas.Nombre_ciudad == Ciudad_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Grupo == Grupo_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Año == Año_choice)]
            
            Productor=list(zip(Total_filtro["Lat_productor"],Total_filtro["Lon_productor"]))
            
            Coord_productor=[]
            
            for p in Productor:
                a=list(p)
                Coord_productor.append(a)
              
                
            Central=list(zip(Total_filtro["Lat_central"],Total_filtro["Lon_central"]))
            Central=Central[0]  
            Coord_central=list(Central)
            
            st.divider()
            
            Mapa, espacio, Sankey= st.columns([10, 2, 10])
            
            ###############
            with Mapa:
                st.subheader("Rutas de distribución de xxxxxxxxxxxxxxxxxxx")
                m = folium.Map(location=Coord_central, zoom_start=8,
                                tiles="Stamen Terrain")

                for i in Coord_productor:
                    
                    folium.PolyLine([Coord_central, i], color="orange").add_to(m)
                
                     
                    folium.Marker(
                    location=Coord_central,
                    #popup="Some Other Location",
                    icon=folium.Icon(color="red"),
                    ).add_to(m)
                    
                    folium.Marker(
                    location=i,
                    #popup="Some Other Location",
                    icon=folium.Icon(color="blue"),
                    ).add_to(m)
                    
                st_map=st_folium(m, width="90%")
            
            with espacio:
                st.subheader("    ")
                
            ##############SANKEY########################
            
            #leer datos
            Total = pd.read_excel('Datos_total.xlsx')
            
            #filtrar datos
            Total_filtro = Total[(Total.Nombre_ciudad == Ciudad_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Grupo == Grupo_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Año == Año_choice)]
            
            productores=list(Total_filtro["Nombre_productor"])
            productores.insert(0, Ciudad_choice)
            cantidades=list(Total_filtro["Toneladas"])
            
            
            #crear graficos sankey     
            with Sankey:    
                st.subheader("Toneladas enviadas por municipios productores a xxxxxxxxxxxxxxxxxxxxxx")
                fig = go.Figure(
                            data=[
                                go.Sankey(
                                    node=dict(
                                        pad=10,
                                        thickness=30,
                                        line=dict(color="white", width=0.0),
                                        label=productores,
                                        ),
                                    link=dict(
                                        source = list(range(1, len(productores))),
                                        target=list(np.zeros(len(productores)-1, dtype=int)),                        
                                        value=cantidades,
                                        ),
                                )
                            ]
                        )
                
               
                st.plotly_chart(fig)
        
        else:
            st.subheader("")
            
            indicadores = pd.read_excel('Indicadores.xlsx')
            
            indicadores_filtro = indicadores[(indicadores.Central == Ciudad_choice)]
            indicadores_filtro = indicadores_filtro[(indicadores_filtro.Grupo == Grupo_choice)]
            indicadores_filtro = indicadores_filtro[(indicadores_filtro.Año == Año_choice)]
    
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Toneladas necesarias", round(indicadores_filtro["Toneladas_necesarias"],2))
            col2.metric("Horas de abastecimiento antes", indicadores_filtro["Tiempo_antes"])
            col3.metric("Horas de abastecimiento después", indicadores_filtro["Tiempo_despues"])
            col4.metric("Centrales de abasto", indicadores_filtro["Numero_centrales"])
            style_metric_cards()

            st.divider()
            
            st.header("Rutas de envío de alimentos")
            
            Mapa1, espacio, Mapa2= st.columns([10,1, 10])
        
            #leer datos
            Coordenadas = pd.read_excel('Datos_total.xlsx')
        
            #filtrar datos
            Total_filtro = Coordenadas[(Coordenadas.Nombre_ciudad == Ciudad_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Grupo == Grupo_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Año == Año_choice)]
            
            Productor=list(zip(Total_filtro["Lat_productor"],Total_filtro["Lon_productor"]))
            
            Coord_productor=[]
            
            for p in Productor:
                a=list(p)
                Coord_productor.append(a)
              
                
            Central=list(zip(Total_filtro["Lat_central"],Total_filtro["Lon_central"]))
            Central=Central[0]  
            Coord_central=list(Central)
            
            
            ###############
            with Mapa1:
                st.subheader("Rutas de la base de datos")
            
                m = folium.Map(location=Coord_central,zoom_start=8,width="100%",height="100%",tiles = "Stamen Terrain")
                
                for i in Coord_productor:
                    
                    folium.PolyLine([Coord_central, i], color="orange").add_to(m)
                
                     
                    folium.Marker(
                    location=Coord_central,
                    popup="Some Other Location",
                    icon=folium.Icon(color="red"),
                    ).add_to(m)
                    
                    folium.Marker(
                    location=i,
                    popup="Some Other Location",
                    icon=folium.Icon(color="blue"),
                    ).add_to(m)
                    
                st_map=st_folium(m, width="70%")
            
            with espacio:
                st.subheader("    ")    
                
            #Mapa 2
            Optimizado = pd.read_excel('Optimizado.xlsx')
            
            #filtrar datos
            Total_filtro_2 = Optimizado[(Optimizado.Nombre_ciudad == Ciudad_choice)]
            Total_filtro_2 = Total_filtro_2[(Total_filtro_2.Grupo == Grupo_choice)]
            Total_filtro_2 = Total_filtro_2[(Total_filtro_2.Año == Año_choice)]
            
            Productor=list(zip(Total_filtro_2["Lat_productor"],Total_filtro_2["Lon_productor"]))
            
            Coord_productor=[]
            
            for p in Productor:
                a=list(p)
                Coord_productor.append(a)
              
                
            Central=list(zip(Total_filtro_2["Lat_central"],Total_filtro_2["Lon_central"]))
            Central=Central[0]  
            Coord_central=list(Central)
            
            
            ###############
            with Mapa2:
                st.subheader("Rutas sugeridas por el algoritmo")
            
                m = folium.Map(location=Coord_central,zoom_start=8,tiles = "Stamen Terrain")
                
                for i in Coord_productor:
                    
                    folium.PolyLine([Coord_central, i], color="orange").add_to(m)
                
                     
                    folium.Marker(
                    location=Coord_central,
                    popup="Some Other Location",
                    icon=folium.Icon(color="red"),
                    ).add_to(m)
                    
                    folium.Marker(
                    location=i,
                    popup="Some Other Location",
                    icon=folium.Icon(color="blue"),
                    ).add_to(m)
                    
                st_map=st_folium(m, width="70%")
                
                
            st.divider()
            
            
            ##############SANKEY########################
            st.subheader("Toneladas enviadas por municipio")
            
            Sankey1, Sankey2= st.columns([10, 10])
        
            #leer datos
            Total = pd.read_excel('Datos_total.xlsx')
            
            #filtrar datos
            Total_filtro = Total[(Total.Nombre_ciudad == Ciudad_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Grupo == Grupo_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Año == Año_choice)]
            
            productores=list(Total_filtro["Nombre_productor"])
            productores.insert(0, Ciudad_choice)
            cantidades=list(Total_filtro["Toneladas"])
            
            
            #crear graficos sankey     
            with Sankey1:    
                st.subheader("Toneladas enviadas según la base de datos")
                fig = go.Figure(
                            data=[
                                go.Sankey(
                                    node=dict(
                                        pad=10,
                                        thickness=30,
                                        line=dict(color="white", width=0.0),
                                        label=productores,
                                        ),
                                    link=dict(
                                        source = list(range(1, len(productores))),
                                        target=list(np.zeros(len(productores)-1, dtype=int)),                        
                                        value=cantidades,
                                        ),
                                )
                            ]
                        )
                st.plotly_chart(fig)
            #leer datos
            Total2 = pd.read_excel('Optimizado.xlsx')
            
            #filtrar datos
            Total_filtro_2 = Total2[(Total2.Nombre_ciudad == Ciudad_choice)]
            Total_filtro_2 = Total_filtro_2[(Total_filtro_2.Grupo == Grupo_choice)]
            Total_filtro_2 = Total_filtro_2[(Total_filtro_2.Año == Año_choice)]
            
            productores=list(Total_filtro_2["Nombre_productor"])
            productores.insert(0, Ciudad_choice)
            cantidades=list(Total_filtro_2["Toneladas"])
            
            
            #crear graficos sankey     
            with Sankey2:    
                st.subheader("Toneladas sugeridas por el algoritmo")
                fig = go.Figure(
                            data=[
                                go.Sankey(
                                    node=dict(
                                        pad=10,
                                        thickness=30,
                                        line=dict(color="white", width=0.0),
                                        label=productores,
                                        ),
                                    link=dict(
                                        source = list(range(1, len(productores))),
                                        target=list(np.zeros(len(productores)-1, dtype=int)),                        
                                        value=cantidades,
                                        ),
                                )
                            ]
                        )
                st.plotly_chart(fig)
            
                
####################################################
    else:

        #Ubicacion de los filtros
        Ciudad, Año, Grupo= st.columns([5, 5, 5])
        
        #filtro de grupo, ciudad y año
        
        with Ciudad:
            Ciudad_choice = st.selectbox(
                  'Seleccione una ciudad con central de abastos',
                  ("Armenia","Barranquilla","Bogotá","Bucaramanga","Cali",
                          "Cartagena de Indias","Cúcuta","Ibagué","Ipiales","Manizales",
                          "Medellín","Montería","Neiva","Pasto","Pereira","Popayán",
                          "Santa Marta","Sincelejo","Tunja","Valledupar","Villavicencio"))
            
        with Año:
             Año_choice = st.selectbox(
                   'Seleccione un año',
                   (2019,2020,2021))
            
        Grupo_lista = pd.read_excel('Optimo_alimento.xlsx')
        Filtro_grupo = Grupo_lista[(Grupo_lista.Nombre_ciudad == Ciudad_choice)]
        Filtro_grupo = Filtro_grupo[(Filtro_grupo.Año == Año_choice)]
        
        grupo_ciudad=list(Filtro_grupo["Grupo"])
        grupo_ciudad=pd.unique(grupo_ciudad)
        grupo_ciudad=list(grupo_ciudad)    
        
    
        with Grupo:
            Grupo_choice = st.selectbox(
                  'Seleccione un alimento',
                  (grupo_ciudad))
        
        st.subheader("")
        
        if Año_choice!=2021:
            
            indicadores = pd.read_excel('Indicadores_alimento.xlsx')
            
            indicadores_filtro = indicadores[(indicadores.Central == Ciudad_choice)]
            indicadores_filtro = indicadores_filtro[(indicadores_filtro.Grupo == Grupo_choice)]
            indicadores_filtro = indicadores_filtro[(indicadores_filtro.Año == Año_choice)]
    
            col1, col2, col3 = st.columns(3)
            col1.metric("Toneladas necesarias", round(indicadores_filtro["Toneladas_necesarias"],2))
            col2.metric("Horas de abastecimiento", indicadores_filtro["Tiempo_antes"])
            col3.metric("Centrales de abasto", indicadores_filtro["Numero_centrales"])
            style_metric_cards()

            #leer datos
            Coordenadas = pd.read_excel('abastecimiento_real.xlsx')
            
            #filtrar datos
            Total_filtro = Coordenadas[(Coordenadas.Nombre_ciudad == Ciudad_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Grupo == Grupo_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Año == Año_choice)]
            
            Productor=list(zip(Total_filtro["Lat_productor"],Total_filtro["Lon_productor"]))
            
            Coord_productor=[]
            
            for p in Productor:
                a=list(p)
                Coord_productor.append(a)
              
                
            Central=list(zip(Total_filtro["Lat_central"],Total_filtro["Lon_central"]))
            Central=Central[0]  
            Coord_central=list(Central)
            
            st.divider()
            
	    

            Mapa, espacio, Sankey= st.columns([10, 2, 10])
            
            ###############
            with Mapa:
                
    		    st.subheader("Rutas de distribución de xxxxxxxxxxxxxxxx")
                
                m = folium.Map(location=Coord_central,zoom_start=8,width="100%",height="100%",tiles = "Stamen Terrain")
                
                for i in Coord_productor:
                    
                    folium.PolyLine([Coord_central, i], color="orange").add_to(m)
                
                     
                    folium.Marker(
                    location=Coord_central,
                    popup="Some Other Location",
                    icon=folium.Icon(color="red"),
                    ).add_to(m)
                    
                    folium.Marker(
                    location=i,
                    popup="Some Other Location",
                    icon=folium.Icon(color="blue"),
                    ).add_to(m)
                    
                st_map=st_folium(m, width="90%")
            
            with espacio:
                st.subheader("    ")
                
            ##############SANKEY########################
            
            #leer datos
            Total = pd.read_excel('abastecimiento_real.xlsx')
            
            #filtrar datos
            Total_filtro = Total[(Total.Nombre_ciudad == Ciudad_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Grupo == Grupo_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Año == Año_choice)]
            
            productores=list(Total_filtro["Nombre_productor"])
            productores.insert(0, Ciudad_choice)
            cantidades=list(Total_filtro["Toneladas"])
            
            
            #crear graficos sankey     
            with Sankey:    
                st.subheader("Toneladas enviadas por municipios productores a xxxxxxxxxxxxxxx")
                fig = go.Figure(
                            data=[
                                go.Sankey(
                                    node=dict(
                                        pad=10,
                                        thickness=30,
                                        line=dict(color="white", width=0.0),
                                        label=productores,
                                        ),
                                    link=dict(
                                        source = list(range(1, len(productores))),
                                        target=list(np.zeros(len(productores)-1, dtype=int)),                        
                                        value=cantidades,
                                        ),
                                )
                            ]
                        )
                st.plotly_chart(fig)
        
        else:
            
            indicadores = pd.read_excel('Indicadores_alimento.xlsx')
            
            indicadores_filtro = indicadores[(indicadores.Central == Ciudad_choice)]
            indicadores_filtro = indicadores_filtro[(indicadores_filtro.Grupo == Grupo_choice)]
            indicadores_filtro = indicadores_filtro[(indicadores_filtro.Año == Año_choice)]
    
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Toneladas necesarias", round(indicadores_filtro["Toneladas_necesarias"],2))
            col2.metric("Horas de abastecimiento antes", indicadores_filtro["Tiempo_antes"])
            col3.metric("Horas de abastecimiento después", indicadores_filtro["Tiempo_despues"])
            col4.metric("Centrales de abasto", indicadores_filtro["Numero_centrales"])
            style_metric_cards()
            
            st.divider()

            st.header("Rutas de distribución de xxxxxxxxxxxxxxxx")

            Mapa1, espacio, Mapa2= st.columns([10,1, 10])
        
            #leer datos
            Coordenadas = pd.read_excel('abastecimiento_real.xlsx')
        
            #filtrar datos
            Total_filtro = Coordenadas[(Coordenadas.Nombre_ciudad == Ciudad_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Grupo == Grupo_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Año == Año_choice)]
            
            Productor=list(zip(Total_filtro["Lat_productor"],Total_filtro["Lon_productor"]))
            
            Coord_productor=[]
            
            for p in Productor:
                a=list(p)
                Coord_productor.append(a)
              
                
            Central=list(zip(Total_filtro["Lat_central"],Total_filtro["Lon_central"]))
            Central=Central[0]  
            Coord_central=list(Central)
            
            
            ###############
            with Mapa1:
                st.subheader("Rutas de la base de datos")
            
                m = folium.Map(location=Coord_central,zoom_start=8,width="100%",height="100%",tiles = "Stamen Terrain")
                
                for i in Coord_productor:
                    
                    folium.PolyLine([Coord_central, i], color="orange").add_to(m)
                
                     
                    folium.Marker(
                    location=Coord_central,
                    popup="Some Other Location",
                    icon=folium.Icon(color="red"),
                    ).add_to(m)
                    
                    folium.Marker(
                    location=i,
                    popup="Some Other Location",
                    icon=folium.Icon(color="blue"),
                    ).add_to(m)
                    
                st_map=st_folium(m, width="70%")
                
            with espacio:
                st.subheader("    ")
                
            #Mapa 2
            Optimizado = pd.read_excel('Optimo_alimento.xlsx')
            
            #filtrar datos
            Total_filtro_2 = Optimizado[(Optimizado.Nombre_ciudad == Ciudad_choice)]
            Total_filtro_2 = Total_filtro_2[(Total_filtro_2.Grupo == Grupo_choice)]
            Total_filtro_2 = Total_filtro_2[(Total_filtro_2.Año == Año_choice)]
            
            Productor=list(zip(Total_filtro_2["Lat_productor"],Total_filtro_2["Lon_productor"]))
            
            Coord_productor=[]
            
            for p in Productor:
                a=list(p)
                Coord_productor.append(a)
              
                
            Central=list(zip(Total_filtro_2["Lat_central"],Total_filtro_2["Lon_central"]))
            Central=Central[0]  
            Coord_central=list(Central)
            
            
            ###############
            with Mapa2:
                st.subheader("Rutas sugeridas por el algoritmo")
            
                m = folium.Map(location=Coord_central,zoom_start=8,width="100%",height="100%",tiles = "Stamen Terrain")
                for i in Coord_productor:
                    
                    folium.PolyLine([Coord_central, i], color="orange").add_to(m)
                
                     
                    folium.Marker(
                    location=Coord_central,
                    popup="Some Other Location",
                    icon=folium.Icon(color="red"),
                    ).add_to(m)
                    
                    folium.Marker(
                    location=i,
                    popup="Some Other Location",
                    icon=folium.Icon(color="blue"),
                    ).add_to(m)
                    
                st_map=st_folium(m, width="70%")
                
                
            st.divider()
            st.subheader("Toneladas enviadas por municipios productores a xxxxx") 
            ##############SANKEY########################
            Sankey1, Sankey2= st.columns([10, 10])
        
            #leer datos
            Total = pd.read_excel('abastecimiento_real.xlsx')
            
            #filtrar datos
            Total_filtro = Total[(Total.Nombre_ciudad == Ciudad_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Grupo == Grupo_choice)]
            Total_filtro = Total_filtro[(Total_filtro.Año == Año_choice)]
            
            productores=list(Total_filtro["Nombre_productor"])
            productores.insert(0, Ciudad_choice)
            cantidades=list(Total_filtro["Toneladas"])
            
            
            #crear graficos sankey     
            with Sankey1:    
                st.subheader("Toneladas enviadas según la base de datos")
                fig = go.Figure(
                            data=[
                                go.Sankey(
                                    node=dict(
                                        pad=10,
                                        thickness=30,
                                        line=dict(color="white", width=0.0),
                                        label=productores,
                                        ),
                                    link=dict(
                                        source = list(range(1, len(productores))),
                                        target=list(np.zeros(len(productores)-1, dtype=int)),                        
                                        value=cantidades,
                                        ),
                                )
                            ]
                        )
                st.plotly_chart(fig)
                
            #leer datos
            Total2 = pd.read_excel('Optimo_alimento.xlsx')
            
            #filtrar datos
            Total_filtro_2 = Total2[(Total2.Nombre_ciudad == Ciudad_choice)]
            Total_filtro_2 = Total_filtro_2[(Total_filtro_2.Grupo == Grupo_choice)]
            Total_filtro_2 = Total_filtro_2[(Total_filtro_2.Año == Año_choice)]
            
            productores=list(Total_filtro_2["Nombre_productor"])
            productores.insert(0, Ciudad_choice)
            cantidades=list(Total_filtro_2["Toneladas"])
            
            #crear graficos sankey     
            with Sankey2:    
                st.subheader("Toneladas sugeridas por el algoritmo")
                fig = go.Figure(
                            data=[
                                go.Sankey(
                                    node=dict(
                                        pad=10,
                                        thickness=30,
                                        line=dict(color="white", width=0.0),
                                        label=productores,
                                        ),
                                    link=dict(
                                        source = list(range(1, len(productores))),
                                        target=list(np.zeros(len(productores)-1, dtype=int)),                        
                                        value=cantidades,
                                        ),
                                )
                            ]
                        )
                st.plotly_chart(fig)
    
with pestaña2:
    
    st.subheader("Problema de optimización para red de abastecimiento")
    
    st.markdown('El problema de optimización se modeló y resolvió con PuLP, una biblioteca de Python que facilita el proceso mediante programación lineal, resolviendo la ecuación presentada a continuación')
    
    st.latex(r'''
    min T_{a,g}= \sum t_{i,j} 
    
    ''')
   
    st.latex(r'''
    s.a.
    
    ''')
    st.latex(r'''
    \sum q_{i,j} \geq d_j
    
    ''')
    st.latex(r'''
    \sum q_{i,j} \leq o_j
    
    ''')
    
    st.markdown('Donde:')
  
    st.markdown("$T_{a,g}$:  tiempo total de desplazamiento para el año, $a$ y el grupo de alimentos, $g$")
            
    st.markdown("$t_{i,j}$:  tiempo de desplazamiento entre cada par de municipios $i$, $j$")
           
    st.markdown("$q_{i,j}$:  cantidad en toneladas enviada desde cada municipio productor $i$ hacia cada ciudad central $j$")            
          
    st.markdown("$d_{j}$:  cantidad que necesita el municipio $j$ para satisfacer su demanda de alimento")
            
    st.markdown("$o_{j}$:  cantidad que produce cada municipio $j$,es decir, la oferta")

    st.divider()
    
    st.subheader("Clasificación de alimentos por grupo")
    
    
    selector_alimentos, vacio, alimentos=st.columns([8,5,15])
    
    with selector_alimentos:
            alimentos_choice = st.selectbox(
                  'Seleccione un grupo',
                      ("Annonaceas","Araceas","Caducifolios","Cereales","Cítricos","Condimentos","Cultivos Tropicales Tradicionales",
                       "Demas frutales","Hortalizas de Flor","Hortalizas de Fruto","Hortalizas de Hoja","Hortalizas de raíz","Hortalizas de Tallo",
                       "Leguminosas","Myrtaceas","Passifloraceas","Raíces y Tubérculos","Solanaceas "))
    with vacio:
        st.markdown("")
        
    with alimentos:
        st.markdown("Alimentos")
        if alimentos_choice=="Annonaceas":
            annotated_text(("Anón","","#fea"))
            annotated_text(("Chirimoya","","#fea"))
            annotated_text(("Guanábana","","#fea"))
        
        elif alimentos_choice=="Araceas":
            annotated_text(("Asaí","","#fea"))
            annotated_text(("Chontaduro","","#fea"))
            annotated_text(("Coco","","#fea"))
            annotated_text(("Corozo","","#fea"))
            annotated_text(("Dátil","","#fea"))
     
            
        elif alimentos_choice=="Caducifolios":
            annotated_text(("Ciruela","","#fea"))
            annotated_text(("Durazno","","#fea"))
            annotated_text(("Manzana","","#fea"))
            annotated_text(("Pera","","#fea"))

            
        elif alimentos_choice=="Cereales":
            annotated_text(("Arroz","","#fea"),"|",("Quinua","","#fea"))
            annotated_text(("Avena","","#fea"),"|",("Sorgo","","#fea"))
            annotated_text(("Cebada","","#fea"),"|",("Trigo","","#fea"))
            annotated_text(("Maíz","","#fea"),"|",("Millo","","#fea"))

            
        elif alimentos_choice=="Cítricos":
            annotated_text(("Lima","","#fea"),"|",("Limón","","#fea"))
            annotated_text(("Mandarina","","#fea"),"|",("Naranja","","#fea"))
            annotated_text(("Pomelo","","#fea"),"|",("Tangelo","","#fea"))
            annotated_text(("Toronja","","#fea"))

            
        elif alimentos_choice=="Condimentos":
            annotated_text(("Achiote","","#fea"),"|",("Cardamomo","","#fea"))
            annotated_text(("Cimarrón","","#fea"),"|",("Jengibre","","#fea"))
            annotated_text(("Laurel","","#fea"),"|",("Oregano","","#fea"))
            annotated_text(("Perejil","","#fea"),"|",("Pimienta","","#fea"))
            annotated_text(("Tomillo","","#fea"))

            
        elif alimentos_choice=="Cultivos Tropicales Tradicionales":
            annotated_text(("Algodón","","#fea"),"|",("Cacao","","#fea"))
            annotated_text(("Café","","#fea"),"|",("Caña","","#fea"))
            annotated_text(("Fique","","#fea"),"|",("Iraca","","#fea"))
            annotated_text(("Tabaco","","#fea"))

            
        elif alimentos_choice=="Demas frutales":
            annotated_text(("Agraz","","#fea"),"|",("Aguacate","","#fea"),"|",("Arándano","","#fea"),"|",("Uva","","#fea"))
            annotated_text(("Banano","","#fea"),"|",("Borojó","","#fea"),"|",("Brevo","","#fea"),"|",("Caímo","","#fea"))
            annotated_text(("Carambolo","","#fea"),"|",("Copoazú","","#fea"),"|",("Frambuesa","","#fea"),"|",("Fresa","","#fea"))
            annotated_text(("Higo","","#fea"),"|",("Macadamia","","#fea"),"|",("Mamoncillo","","#fea"),"|",("Mango","","#fea"))
            annotated_text(("Mangostino","","#fea"),"|",("Marañón","","#fea"),"|",("Mora","","#fea"),"|",("Níspero","","#fea"))
            annotated_text(("Noni","","#fea"),"|",("Papaya","","#fea"),"|",("Papayuela","","#fea"),"|",("Piña","","#fea"))
            annotated_text(("Pitahaya","","#fea"),"|",("Plátano","","#fea"),"|",("Rambután","","#fea"),"|",("Tamarindo","","#fea"))
            annotated_text(("Zapote","","#fea"))           
            
        elif alimentos_choice=="Hortalizas de Flor":
            annotated_text(("Brócoli","","#fea"))
            annotated_text(("Coliflor","","#fea"))

            
        elif alimentos_choice=="Hortalizas de Fruto":
            annotated_text(("Ahuyama","","#fea"),"|",("Ají","","#fea"))
            annotated_text(("Berenjena","","#fea"),"|",("Calabacín","","#fea"))
            annotated_text(("Guatila","","#fea"),"|",("Melón","","#fea"))
            annotated_text(("Patilla","","#fea"),"|",("Pepino","","#fea"))
            annotated_text(("Pimentón","","#fea"),"|",("Tomate","","#fea"))            
                       
        elif alimentos_choice=="Hortalizas de Hoja":
            annotated_text(("Acelga","","#fea"),"|",("Cilantro","","#fea"))
            annotated_text(("Col","","#fea"),"|",("Espinaca","","#fea"))
            annotated_text(("Lechuga","","#fea"),"|",("Repollo","","#fea"))
            
        elif alimentos_choice=="Hortalizas de raíz":
            annotated_text(("Ajo","","#fea"),"|",("Batata","","#fea"))
            annotated_text(("Cebolla","","#fea"),"|",("Rábano","","#fea"))
            annotated_text(("Remolacha","","#fea"),"|",("Zanahoria","","#fea"))

            
        elif alimentos_choice=="Hortalizas de Tallo":
            annotated_text(("Apio","","#fea"))
            annotated_text(("Cebolla","","#fea"))
            annotated_text(("Esparrago","","#fea"))
            annotated_text(("Palmito","","#fea"))
            
            
        elif alimentos_choice=="Leguminosas":
            annotated_text(("Arveja","","#fea"),"|",("Fríjol","","#fea"))
            annotated_text(("Garbanzo","","#fea"),"|",("Guama","","#fea"))
            annotated_text(("Guandul","","#fea"),"|",("Haba","","#fea"))
            annotated_text(("Habichuela","","#fea"),"|",("Maní","","#fea"))

            
        elif alimentos_choice=="Myrtaceas":
            annotated_text(("Arazá","","#fea"))
            annotated_text(("Chamba","","#fea"))
            annotated_text(("Feijoa","","#fea"))
            annotated_text(("Guayaba","","#fea"))

            
        elif alimentos_choice=="Passifloraceas":
            annotated_text(("Badea","","#fea"))
            annotated_text(("Curuba","","#fea"))
            annotated_text(("Granadilla","","#fea"))
            annotated_text(("Gulupa","","#fea"))
            annotated_text(("Maracuyá","","#fea"))

            
            
        elif alimentos_choice=="Raíces y Tubérculos":
            annotated_text(("Achira","","#fea"),"|",("Arracacha","","#fea"))
            annotated_text(("Cúrcuma","","#fea"),"|",("Malanga","","#fea"))
            annotated_text(("Nabo","","#fea"),"|",("Ñame","","#fea"))
            annotated_text(("Papa","","#fea"),"|",("Ulluco","","#fea"))
            annotated_text(("Yuca","","#fea"))
            
        else:  
            annotated_text(("Lulo","","#fea"))
            annotated_text(("Tomate de árbol","","#fea"))
            annotated_text(("Uchuva","","#fea"))

    #Boton de descarga informe
    st.divider()
    st.subheader("Informe metodológico")

    with open("marzo.pdf", "rb") as pdf_file: 
        PDFbyte = pdf_file.read() 
        
    st.download_button(label="Pulse para descargar el informe", data=PDFbyte, file_name="marzo.pdf")
    
st.markdown("*Desarrollado por: Unidad de Científicos de Datos - Dirección de Desarrollo Digital*")



