# -*- coding: utf-8 -*-
"""
Created on Wed Feb  18 12:36:56 2022

@author: crist
"""

from selenium import webdriver
import os
import wsrts.variables as variables
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import re
import pandas as pd

class Rts(webdriver.Chrome):
	def __init__(self, driver_path = os.getcwd(), teardown = False):
		self.driver_path = driver_path
		self.teardown = teardown
		
		if not driver_path in os.environ['PATH']:
			os.environ['PATH'] += os.pathsep + self.driver_path
		
		super(Rts, self).__init__()
		
		self.maximize_window()
		
	def __exit__(self, exce_type, exce_val, exce_tb):
		if self.teardown:
			self.quit()
		
	def get_url(self, url):
		self.get(url)
		
	def login(self):
		"""
		Funcion encargada de logearse en el area personal de la pagina RTS
		"""
		self.find_element(By.ID, variables.id_username).send_keys(variables.user)
		self.find_element(By.ID, variables.id_password).send_keys(variables.password)
		
		self.find_element(By.XPATH, variables.xpath_login_submit).click()
		
	def wait_presence_text(self, selector, locator , text, time = 100 ):
		"""
		Funcion encargada de permitir el flujo del programa en el caso de que
		se encuentre en la pagina web el texto deseado.
		
		Parameters
		----------
		selector : define el tipo de selector a emplear: class_name, name, tag_name, id, xpath,
		css_selector, partial_link_text, link_text.
		locator : especifica el identificador del elemento web.
		text : especifica el texto que se quiere encontrar. Debe ser exactamente igual.
		time : opcional. Por defecto se espera 100 segundos.

		Returns
		-------
		bool
			True en el caso de que este el texto del elemento web.
			False en el caso de que no este el texto del elemento web.

		"""
		try:
			if selector == 'class_name':
				WebDriverWait(self, time).until(
					EC.text_to_be_present_in_element((By.CLASS_NAME, locator), text)
					)
			elif selector == 'id':
				WebDriverWait(self, time).until(
					EC.text_to_be_present_in_element((By.ID, locator), text)
					)
			elif selector == 'xpath':
				WebDriverWait(self, time).until(
					EC.text_to_be_present_in_element((By.XPATH, locator), text)
					)
			elif selector == 'tag_name':
				WebDriverWait(self, time).until(
					EC.text_to_be_present_in_element((By.TAG_NAME, locator), text)
					)
			elif selector == 'name':
				WebDriverWait(self, time).until(
					EC.text_to_be_present_in_element((By.NAME, locator), text)
					)
			elif selector == 'css_selector':
				WebDriverWait(self, time).until(
					EC.text_to_be_present_in_element((By.CSS_SELECTOR, locator), text)
					)
			elif selector == 'link text':
				WebDriverWait(self, time).until(
					EC.text_to_be_present_in_element((By.LINK_TEXT, locator), text)
					)
			elif selector == 'partial_link_text':
				WebDriverWait(self, time).until(
					EC.text_to_be_present_in_element((By.PARTIAL_LINK_TEXT, locator), text)
					)
		except TimeoutException:
			return False
		return True
		
	def open_popup(self, text, tr, td, div = 2, pop_workout = True):
		"""
		Funcion encargada de abrir los elementos que se encuentran dentro del calendario. Por ejemplo, si se quiere abrir
		los elementos que contienen como titulo 'New Workout' abre esos, si es 'Daily Workour' abre esos...el string se
		especifica a traves de la variable text
		"""
		if pop_workout:
			xpath_popup_text = f"{variables.xpath_new_workout['id1']}{tr}{variables.xpath_new_workout['id2']}{td}{variables.xpath_new_workout['id4']}"
			xpath_popup = f"{variables.xpath_new_workout['id1']}{tr}{variables.xpath_new_workout['id2']}{td}{variables.xpath_new_workout['id3']}{div}{variables.xpath_new_workout['id4']}"
		else:
			xpath_popup_text = f'//*[@id="Calendar"]/tbody/tr[{tr}]/td[{td}]/div[3]/span'
			xpath_popup = f'//*[@id="Calendar"]/tbody/tr[{tr}]/td[{td}]/div[3]'
			
		if text in self.find_element(By.XPATH, xpath_popup_text).text:
			self.find_element(By.XPATH, xpath_popup).click()
			return True
		else:
			return False
		
	def scraping_TRAC(self):
		pass
		
	def open_and_close_workout(self, li):
		"""
		Funcion encargada de abrir o cerrar un ejercicio determinado (el '+' que tienen a la izquierda)
		"""
		self.find_element(By.XPATH, f"{variables.xpath_workout['id1']}{li}{variables.xpath_workout['id2']}1{variables.xpath_workout['id3']}1{variables.xpath_workout['id4']}").click()
		
	def close_popup(self):
		self.find_element(By.ID, variables.id_close_popup).click()
		
	def data_serie(self, li, div2):
		"""
		Esta funcion se encarga de obtener los datos objetivos de una serie determinada, se le pasa el elemento
		li que hace referencia al ejercicio y luego el elemento div2 que hace referencia a la serie.
		
		Hay casos donde hay ejercicios que si hay que añadir peso, en ese caso la longitud del vector serie
		es de 6. Sin embargo, hay ejercicios que se trabaja con el BW o en isometricos y la longitud del vector
		es de 4, para dar mayor uniformidad a este aspecto, se le añade el valor 'Null' en la posicion 0 y 3
		para que exista siempre la misma longitud.
		"""
		weight  = self.find_element(By.XPATH, f"{variables.xpath_workout['id1']}{li}{variables.xpath_workout['id2']}2{variables.xpath_workout['id3']}1{variables.xpath_workout['id4']}").text.split('\n')
		
		if 'Weight Reps RPE' in weight:
			data_serie = self.find_element(By.XPATH, f"{variables.xpath_workout['id1']}{li}{variables.xpath_workout['id2']}2{variables.xpath_workout['id3']}{div2} {variables.xpath_workout['id4']}").text.split(' ')
			
			if data_serie.count('kgs') > 0:
				for dl in range(0, data_serie.count('kgs')):
					data_serie.remove('kgs')
		else:
			data_serie = self.find_element(By.XPATH, f"{variables.xpath_workout['id1']}{li}{variables.xpath_workout['id2']}2{variables.xpath_workout['id3']}{div2} {variables.xpath_workout['id4']}").text.split(' ')
			
			if data_serie.count('h') > 0:
				for dl in range(0, data_serie.count('h')):
					data_serie.remove('h')
			if data_serie.count('m') > 0:
				for dl in range(0, data_serie.count('m')):
					data_serie.remove('m')
			if data_serie.count('s') > 0:
				for dl in range(0, data_serie.count('s')):
					data_serie.remove('s')
			
			data_serie.insert(0, 'Null')
			data_serie.insert(3, 'Null')
			
		return data_serie
	
	def normalize_datetime(self, date):
		"""
		Funcion encargada de coger la fecha del workout y pasarla a una variable
		del tipo datetime para manejar su formato de forma mas sencilla. Para
		eso se ha tenido que eliminar los sufijos de los numeros ya que eso no
		lo reconoce python.
		"""
		date = date.split(',')
		if 'st' in date[1]:
			date[1] = re.sub(r'st', '', date[1])
		elif 'th' in date[1]:
			date[1] = re.sub(r'th', '', date[1])
		elif 'rd' in date[1]:
			date[1] = re.sub(r'rd', '', date[1])
		elif 'nd' in date[1]:
			date[1] = re.sub(r'nd', '', date[1])
			
		date = ''.join(date)
		date = datetime.strptime(date, '%A %b %d %Y')
		date = date.strftime('%Y-%m-%d')
		
		return date
		
	def scraping_workout(self):
		# genero la lista que va a almacenar todas las series de ese dia
		workout_daily = list()
		
		# aqui obtengo la fecha de este workout
		workout_fecha = self.find_element(By.ID, variables.id_date_workout).text
		workout_fecha = self.normalize_datetime(workout_fecha)
		WebElement_ExerciseList = self.find_element(By.ID, variables.id_list_exercise)
		
		# obtengo el numero de ejercicios
		lista_ejercicios = WebElement_ExerciseList.text.split('\n')
		n_ejercicios = len(lista_ejercicios)
		
		# recoorro cada ejercicio a traves del elemento li
		for li in range(1, n_ejercicios+1):
			self.implicitly_wait(1)
			
			# obtengo el numero de series y el nombre del ejercicio
			sets = int(self.find_element(By.XPATH, f"{variables.xpath_workout_sets['id1']}{li}{variables.xpath_workout_sets['id2']}1{variables.xpath_workout_sets['id3']}4 {variables.xpath_workout_sets['id4']}2{variables.xpath_workout_sets['id5']}").text)
			name_set = self.find_element(By.XPATH, f"{variables.xpath_name_set['id1']}{li}{variables.xpath_name_set['id2']}1{variables.xpath_name_set['id3']}2{variables.xpath_name_set['id4']}").text
			
			# lo abro y espero hasta que se cargue bien del todo. Esta parte es importante ya que
			# si no se espera hasta el momento adecuado, da errores y se salta ejercicios
			self.open_and_close_workout(li)
			self.wait_presence_text('xpath', f"{variables.xpath_workout_target['id1']}{li}{variables.xpath_workout_target['id2']}2{variables.xpath_workout_target['id3']}1{variables.xpath_workout_target['id4']}1{variables.xpath_workout_target['id5']}", 'Target')
			
			if len(self.find_element(By.XPATH, f'//*[@id="IExerciseList"]/li[{li}]/div[2]/div[1]/div[1]').text.split('\n')) < 2 or len(self.find_element(By.XPATH, f'//*[@id="IExerciseList"]/li[{li}]/div[2]/div[1]/div[2]').text.split('\n')) < 2:
				continue
			
			# una vez cargado, voy serie por serie
			for div2 in range(2, sets + 2):
				
				# obtengo los datos de la serie
				data_serie = self.data_serie(li, div2)
				
				# y finalmente añado el nombre, la fecha del ejercicio y lo
				# agrego al vector final
				data_serie.insert(0, name_set)
				data_serie.insert(0, workout_fecha)
				
				workout_daily.append(data_serie)
				
		return workout_daily
	
	def find_workout(self, text):
		"""
		Esta funcion es la encargada de buscar si en el mes que se esta hay
		algun Workout. Desde que haya 1 ya para de buscar mas y devuelve True, si no 
		hay devuelve False
		"""
		cont = 0
		for txt in self.find_elements(By.CLASS_NAME, variables.class_item_text):
			if txt.text.lower() == text.lower():
				cont += 1
				break
		if cont > 0:
			return True
		else:
			return False
			
	def change_month(self, month, past = True):
		"""
		Esta funcion se encarga de devolver el mes anterior o posterior al que 
		se le pasa a la funcion. El objetuvo de esto es para que, a partir de otra funcion
		esperar a que encuentre el texto deseado; que en el caso de ir cambiando de meses
		pues se espera el mes anterior si se va al "pasado" donde past = True y sino al futuro 
		donde past  = False
		"""
		month2 = datetime.strptime(month, '%B %Y')
		
		if past:
			mes_delta = month2 - timedelta(days = 29)
			if month2.month == mes_delta.month:
				mes_delta = mes_delta - timedelta(weeks = 1)
			# pongo a dia 1 mes_delta
			mes_delta = mes_delta - timedelta(days= mes_delta.day -1)
			mes_delta = datetime.strftime(mes_delta, '%B %Y')
		else:
			mes_delta = month2 + timedelta(days = 29)
			if month2.month == mes_delta.month:
				mes_delta = mes_delta + timedelta(weeks = 1)
			# pongo a dia 1 mes_delta
			mes_delta = mes_delta - timedelta(days= mes_delta.day -1)
			mes_delta = datetime.strftime(mes_delta, '%B %Y')
		
		return mes_delta
	
	def wait_month(self, past = True):
		month = self.find_element(By.CLASS_NAME, variables.class_calendar_month).text
		month_delta = self.change_month(month, past)
		self.wait_presence_text('class_name', variables.class_calendar_month, month_delta)
		
	def report(self, workout):
		df = pd.DataFrame(workout, columns = ['Date', 'Name', 'kgs', 'Reps', 'RPE', 'kgs', 'Reps', 'RPE'])
		df.to_excel('RTS.xlsx')
		
		return df
