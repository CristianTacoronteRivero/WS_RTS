# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 16:32:00 2022

@author: crist
"""
#%% LIBRERIAS
from ctrWS import ctrWS
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import calendar
from selenium.common.exceptions import TimeoutException, NoSuchElementException


#%% VARIABLES
url_rts = 'https://www.reactivetrainingsystems.com/Authentication/LoginPage'
url_calendario = 'https://www.reactivetrainingsystems.com/AppHome/Calendar'

#%% FUNCIONES PERSONALIZADAS
def find_workout(text):
    "Aqui coge el elemento correspondiente a los encabezados y mira si tiene al menos un string que se especifica con el parametro text, si lo tiene rompe el bucle y devuelve un True, sino un False"
    for txt in bot.find_elements(By.CLASS_NAME, 'CalItemText'):
        if txt.text.lower() == text.lower():
            return True
            break
    return False

def change_month(month, past):
    "se encarga de encontrar el mes anterior si se le pasa past=True, sino te devuelve el mes posterior"
    month2 = datetime.strptime(month, '%B %Y')
    if past:
        mes_delta = month2 - timedelta(days = 5)
        mes_delta = datetime.strftime(mes_delta, '%B %Y')
    else:
        monthRange = calendar.monthrange(year=month2.year, month=month2.month)
        mes_delta = month2 + timedelta(days = monthRange[1]+1)
        mes_delta = datetime.strftime(mes_delta, '%B %Y')
    return mes_delta

def get_month(past):
    "Aqui se coge el mes de la pagina actual del calendario y lo que hace es devolver el mes pasado empleando la funcion anterior"
    month = bot.find_element(By.CLASS_NAME, 'CalText').text
    month = change_month(month, past)
    return month

def open_popup(text, tr, td):
    "Funcion encargada de encontrar el popup correcto y abrirlo para que el DOM aparezca y se pueda realizar WS"
    xpath_popup = f"//*[@id='Calendar']/tbody/tr[{tr}]/td[{td}]/div[2]"

    try:
        if text.lower() in bot.find_element(By.XPATH, xpath_popup).text.lower():
            bot.find_element(By)

#%% CODIGO
with ctrWS() as bot:
#%%% inicio y login
    bot.get_url(url_rts)
    bot.login('tacoronteriveracristian@gmail.com', '12345678A.')
#%%% cargado del calendario
    # en el caso de que se haya cargado ya la pagina web, accedo a la zona de "Calendario Central"
    if bot.wait_presence_text('class_name', 'ActiveIconText', 'Dashboard Central'):
        bot.get_url(url_calendario)

#%%% retroceso en el calendario
    # mientras hayan casillas con 'New Workout', 'Daily workout', etc.
    while find_workout('New Workout') or find_workout('Daily Workout') or find_workout('Nuevo Entrenamiento'):
        # obtenemos el mes anterior
        month = get_month(past=True)
        # clicamos para ir hacia atras
        bot.find_elements(By.CLASS_NAME, 'Clickable')[0].click()
        # y esperamos hasta que aparezca el mes que hemos obtenido en la linea anterior
        bot.wait_presence_text('class_name', 'CalText', month)

    # y como se va un mes de mas para comprobar, lo vuelvo a mandar hacia delante. [0] hacia detras, [1] hacia delante
    bot.find_elements(By.CLASS_NAME, 'Clickable')[1].click()
    # y volvemos a esperar
    month = get_month(past=False)
    bot.wait_presence_text('class_name', 'CalText', month)

#%%% comienzo de ws para cada dia
    # bucle while donde mientras hayan New Workout o Daily Workout, hago scrapping en el total del calendario 6 filas x 8 columnas y paso al siguiente mes hasta que no se cumpla el condicional del while
    while find_workout('New Workout') or find_workout('Daily Workout') or find_workout('Nuevo Entrenamiento'):
        for tr in range(1,6):
            for td in range(1,8):
