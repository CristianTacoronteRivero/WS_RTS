# -*- coding: utf-8 -*-
"""
Created on Wed Feb  18 12:36:56 2022

@author: crist
"""

from wsrts.rts import Rts
import wsrts.variables as variables
import time
from selenium.webdriver.common.by import By

with Rts() as bot:
#%% LOGIN TO CALENDAR
	# cargo pagina web y me logeo
	bot.get_url(variables.url_basica)
	bot.login()
	
	# en el caso de que se haya cargado ya la pagina web, accedo a la zona de "Calendario Central"
	if bot.wait_presence_text('class_name', variables.class_dashborad_central, 'Dashboard Central'):
		bot.get_url(variables.ur_calendar_central)
		
	workout_monthly = list()
	
#%% GO TO BACK 
	if True:
		# mientras hayan casillas con 'New Workout'...
		while bot.find_workout('New Workout') or bot.find_workout('Daily Workout'):
			# obtenemos el mes que hay que esperar
			month = bot.get_month()
			
			# clica para ir hacia ATRAS.OJO. SI QUIERO IR HACIA DELANTE ES [1]
			bot.find_elements(By.CLASS_NAME, variables.class_calendar_month_click)[0].click()
			
			# espero a que se cargue el mes que debe de aparecer y sigo con el bucle
			bot.wait_presence_text('class_name', variables.class_calendar_month, month)
			
		# como se va un mes de más, le obligo que vuelva hacia delante. PENSAR EN COMO OPTIMIZAR ESTO.
		bot.find_elements(By.CLASS_NAME, variables.class_calendar_month_click)[1].click()
		
		time.sleep(1)
	
#%% SCRAPING
	while bot.find_workout('new workout') or bot.find_workout('daily workout') or bot.find_workout('nuevo entrenamiento'):
		# con este bucle recorro todo el calendario, tanto todas las columnas como filas
		for tr in range(1,6):
			for td in range(1,8):
#%%% GO TO WORKOUT
				# en el caso de que el dia tenga como texto 'New Workout' o 'Daily Workout' o 'Nuevo Entrenamiento', abre ese dia para recabar la informacion, sino el bucle sigue al dia siguiente
				if not bot.open_popup('new workout', tr, td):
					if not bot.open_popup('daily workout', tr, td):
						if not bot.open_popup('nuevo entrenamiento', tr, td):
							continue
				
				# como se tarda en abrir las pestañas, se ejecuta de nuevo esta funcion para que siga con el ciclo hasta que vea que por pantalla se muestra 'Close' en el popup, ya que eso significa que ya se ha abierto correctamente
				bot.wait_presence_text('id', variables.id_close_popup, 'Close')
				
				work_daily = bot.scraping_workout()
				workout_monthly.extend(work_daily)
				
				# una vez finalizada la recabacion de la informacion, se cierra el popup y se va al siguiente
				time.sleep(0.25)
				bot.close_popup()
				
#%%% GO TO TRAC (JUSTO ANTES DEL REPORT DATAFRAME?)
# 				if bot.open_popup('trac', tr, td, pop = 'trac'):
# 					bot.scraping_trac()
					
		# clica para ir hacia delante
		bot.find_elements(By.CLASS_NAME, variables.class_calendar_month_click)[1].click()
		
		# esta funcion se encarga de obtener cual debe ser el mes anterior y no sigue con el bucle hasta que se cargue el calendrio correcto
		bot.wait_month(past = False)
		
#%% REPORT TO DATAFRAME
	df = bot.report(workout_monthly)

