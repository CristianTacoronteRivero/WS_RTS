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
	# cargo pagina web y me logeo
	bot.get_url(variables.url_basica)
	bot.login()
	
	# en el caso de que se haya cargado ya la pagina web, accedo a la zona de "Calendario Central"
	if bot.wait_presence_text('class_name', variables.class_dashborad_central, 'Dashboard Central'):
		bot.get_url(variables.ur_calendar_central)
		
	workout_monthly = list()
	
	if False:
		# mientras hayan casillas con 'New Workout'...
		while bot.find_workout('New Workout') or bot.find_workout('Daily Workout'):
			# clica para ir hacia atras
			bot.find_elements(By.CLASS_NAME, variables.class_calendar_month_click)[0].click()
			
			# estas funcion se encarga de obtener cual debe ser el mes anterior y no sigue con el bucle hasta que se cargue el calendrio correcto
			bot.wait_month()
			
		# como se va un mes de más, le obligo que vuelva hacia delante. PENSAR EN COMO OPTIMIZAR ESTO.
		bot.find_elements(By.CLASS_NAME, variables.class_calendar_month_click)[1].click()
		
		time.sleep(1)
	
	while bot.find_workout('New Workout') or bot.find_workout('Daily Workout'):
		# con este bucle recorro todo el calendario, tanto todas las columnas como filas
		for tr in range(1,6):
			for td in range(1,8):
				# en el caso de que el dia tenga como texto 'New Workout', abre ese dia para recabar la informacion, sino el bucle sigue al dia siguiente
				if not bot.open_popup('New Workout', tr, td):
					if not bot.open_popup('Daily Workout', tr, td):
						continue
				
				# como se tarda en abrir las pestañas, se ejecuta de nuevo esta funcion para que siga con el ciclo hasta que vea que por pantalla se muestra 'Close' en el popup, ya que eso significa que ya se ha abierto correctamente
				bot.wait_presence_text('id', variables.id_close_popup, 'Close')
				
				
				work_daily = bot.scraping_workout()
				workout_monthly.extend(work_daily)
				
				# una vez finalizada la recabacion de la informacion, se cierra el popup y se va al siguiente
				time.sleep(0.25)
				bot.close_popup()
				
				# TODO: hago scraping con el TRAC
				if bot.open_popup('TRAC', tr, td, pop_workout=False):
					
		
		# clica para ir hacia delante
		bot.find_elements(By.CLASS_NAME, variables.class_calendar_month_click)[1].click()
		
		# estas funcion se encarga de obtener cual debe ser el mes anterior y no sigue con el bucle hasta que se cargue el calendrio correcto
		bot.wait_month(past = False)
		
	df = bot.report(workout_monthly)

