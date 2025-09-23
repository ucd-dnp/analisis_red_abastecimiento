# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 11:56:12 2023

@author: Mariana
"""

# -*- coding: utf-8 -*-


"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import pandas as pd

options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

driver_path= 'C:\\Users\\Mariana\\Downloads\\chromedriver_win32\\chromedriver.exe'

#Cargar municipios 
municipios = pd.read_excel("municipios.xlsx")
 
origen=municipios[['Origen']]
destino=municipios[['Destino']]


#Distancia en kilómetros 

km=[]

driver = webdriver.Chrome(driver_path, chrome_options=options)

for i in range(len(origen)):
    driver.get('http://es.distancias.himmera.com')

    #Dar clic e ingresar el nombre del municipio de origen
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'input#fr')))\
        .click()   
        
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                          'input#fr')))\
        .send_keys(origen.iloc[i]) 
        
        #Dar clic e ingresar el nombre del municipio de destino  
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'input#to')))\
        .click()
        
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                           'input#to')))\
        .send_keys(destino.iloc[i])

    #Dar clic en consultar distancia        
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'span.btq')))\
        .click()
  
    #Esperar a que aparezca el dato
    time.sleep(5)
    
    #Guardar el dato de kilometraje
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                          '/html/body/div[5]/div[5]/span[2]/span[1]')))

    kilometros = driver.find_element("xpath",'/html/body/div[5]/div[5]/span[2]/span[1]')
    kilometros_1 = [kilometros.text]
    
    km.append(kilometros_1)
      
