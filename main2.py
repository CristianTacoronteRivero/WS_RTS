# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 16:32:00 2022

@author: crist
"""
#%% LIBRERIAS
from ctrWS import ctrWS
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import calendar, re
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
import pandas as pd


#%% VARIABLES
url_rts = 'https://www.reactivetrainingsystems.com/Authentication/LoginPage'
url_calendario = 'https://www.reactivetrainingsystems.com/AppHome/Calendar'
workout_monthly = list()

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
            bot.find_element(By.XPATH, xpath_popup).click()
            return True
        else:
            return False
    except NoSuchElementException:
        return False

def normalize_datetime(date):
    "Funcion encargada de coger la fecha, eliminar los sufijos y darle el formato de datetime"
    ind=2
    date = date.split()
    if 'st' in date[ind]:
        date[ind] = re.sub(r'st', '', date[ind])
    if 'th' in date[ind]:
        date[ind] = re.sub(r'th', '', date[ind])
    if 'rd' in date[ind]:
        date[ind] = re.sub(r'rd', '', date[ind])
    if 'nd' in date[ind]:
        date[ind] = re.sub(r'nd', '', date[ind])

    date = ' '.join(date)
    date = datetime.strptime(date, '%A, %b %d, %Y')
    date = date.strftime('%Y-%m-%d')
    return date

def open_or_close_workout(li):
    "Funcion encargada de abrir o cerrar la lista de un ejercicio en concreto (darle al + o -)"
    bot.find_element(By.XPATH, f"//*[@id='IExerciseList']/li[{li}]/div[1]/div[1]").click()

def data_serie(li, div2):
    weight = bot.find_element(By.XPATH, f"//*[@id='IExerciseList']/li[{li}]/div[2]/div[1]").text.lower().split('\n')
    if 'weight reps rpe' in weight:
        data = bot.find_element(By.XPATH, f"//*[@id='IExerciseList']/li[{li}]/div[2]/div[{div2}]").text.split(' ')
        if data.count('kgs') > 0:
            for dl in range(0, data.count('kgs')):
                data.remove('kgs')
    else:
        data = bot.find_element(By.XPATH, f"//*[@id='IExerciseList']/li[{li}]/div[2]/div[{div2}]").text.split(' ')
        if data.count('h') > 0:
            for dl in range(0, data.count('h')):
                data.remove('h')
        if data.count('m') > 0:
            for dl in range(0, data.count('m')):
                data.remove('m')
        if data.count('s') > 0:
            for dl in range(0, data.count('s')):
                data.remove('s')
        data.insert(0, np.nan)
        data.insert(3, np.nan)
    return data

def scraping_workout():
    # creo la lista donde guardo la informacion diaria
    workout_daily = list()

    lista_ejercicios =len(bot.find_element(By.ID, 'IExerciseList').text.split('\n'))
    # recorro cada ejercicio a traves del li
    for li in range(1, lista_ejercicios+1):
        bot.implicitly_wait(0.5)
        # aqui obtengo el nombre del ejercicio y el numero de sets y ya luego lo abro
        name_set = bot.find_element(By.XPATH, f"//*[@id='IExerciseList']/li[{li}]/div[1]/div[2]/a").text
        sets = int(bot.find_element(By.XPATH, f"//*[@id='IExerciseList']/li[{li}]/div[1]/div[4]/span[2]").text)
        # abro la lista de ese ejercicio y espero a que se complete la apertura
        open_or_close_workout(li)
        bot.wait_presence_text('xpath', f"//*[@id='IExerciseList']/li[{li}]/div[2]/div[1]/div[1]", 'Target')

        # observo una condicion que por ahora no entiendo
        if len(bot.find_element(By.XPATH, f'//*[@id="IExerciseList"]/li[{li}]/div[2]/div[1]/div[1]').text.split('\n')) < 2 or len(bot.find_element(By.XPATH, f'//*[@id="IExerciseList"]/li[{li}]/div[2]/div[1]/div[2]').text.split('\n')) < 2:
            open_or_close_workout(li)
            continue

        bot.implicitly_wait(0.15)
        # una vez cargado voy serie por serie de ese mismo ejer cogiendo los datos
        for div2 in range(2, sets+2):
            # saco los datos de cada serie
            data = data_serie(li, div2)
            # y añado el nombre y la fecha del ejercicio
            data.insert(0, name_set)
            data.insert(0, workout_fecha)

            workout_daily.append(data)
    return workout_daily

def close_popup():
    bot.find_element(By.ID, 'PopupCancel').click()

def report(workout, save=True):
    df = pd.DataFrame(workout, columns = ['Date', 'Name', 'kgs', 'Reps', 'RPE', 'kgs', 'Reps', 'RPE'])
    df = df.drop_duplicates()
    if save:
        df.to_excel(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_RTS.xlsx")
    return df


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
    if True:
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

#%%% bucle foward del calendario
    # bucle while donde mientras hayan New Workout o Daily Workout, hago scrapping en el total del calendario 6 filas x 8 columnas y paso al siguiente mes hasta que no se cumpla el condicional del while
    while find_workout('New Workout') or find_workout('Daily Workout') or find_workout('Nuevo Entrenamiento'):
        for tr in range(1,6):
            for td in range(1,8):
                if not open_popup('New Workout', tr, td):
                    if not open_popup('Daily Workout', tr, td):
                        if not open_popup('Nuevo Entrenamiento', tr, td):
                            continue

                # una vez abierto el popup, espero a que aparezca la ventana
                bot.wait_presence_text('id', 'PopupCancel', 'Close')

#%%% scraping del workout
                # rescato la fecha del workout
                workout_fecha = normalize_datetime(bot.find_element(By.ID, 'WorkoutDateText').text)

                # obtengo el entreno de esa semana
                work_daily = scraping_workout()
                workout_monthly.extend(work_daily)

                # una vez finalizado la recabacion de datos de este dia, cierro el popup y voy al siguiente dia
                bot.implicitly_wait(0.15)
                close_popup()
                bot.implicitly_wait(0.15)

                # clica para ir hacia delante y espero que se cargue el calendario
        bot.find_elements(By.CLASS_NAME, 'Clickable')[1].click()
        month = get_month(past=False)
        bot.wait_presence_text('class_name', 'CalText', month)

#%%% creacion del archivo xlsx
    df = report(workout_monthly)
