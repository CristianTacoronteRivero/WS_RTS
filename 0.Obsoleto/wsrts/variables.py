# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 12:36:56 2022

@author: crist
"""

"""
Script donde se almacenan todos los identificadores y variables fijas
"""

url_basica = 'https://www.reactivetrainingsystems.com/Authentication/LoginPage'
ur_calendar_central = 'https://www.reactivetrainingsystems.com/AppHome/Calendar'

user = 'tacoronteriveracristian@gmail.com'
password = '12345678A.'

# ELEMENTOS
id_username = 'Username'
id_password = 'Password'
id_icono_burger = 'AppIconCont_M'
id_close_popup = 'PopupCancel'
id_date_workout = 'WorkoutDateText'
id_list_exercise = 'IExerciseList'

xpath_login_submit = '//*[@id="LoginForm2"]/div[3]/button[1]'
xpath_calendar_central = '//*[@id="AppMenuDD"]/div/div/div[2]/ul/li[1]/a'
xpath_new_workout = {'id1': '//*[@id="Calendar"]/tbody/tr[',
				  'id2': ']/td[',
				  'id3': ']/div[',
				  'id4': ']'}
xpath_workout = {'id1' : '//*[@id="IExerciseList"]/li[',
							 'id2': ']/div[',
							 'id3': ']/div[',
							 'id4': ']'}
xpath_workout_sets = {'id1' : '//*[@id="IExerciseList"]/li[',
							 'id2': ']/div[',
							 'id3': ']/div[',
							 'id4': ']/span[',
							 'id5': ']'}
xpath_name_set = {'id1' : '//*[@id="IExerciseList"]/li[',
							 'id2': ']/div[',
							 'id3': ']/div[',
							 'id4': ']/a'}
xpath_workout_target = {'id1' : '//*[@id="IExerciseList"]/li[',
							 'id2': ']/div[',
							 'id3': ']/div[',
							 'id4': ']/div[',
							 'id5': ']'}
xpath_text_target_actual = {'id1' : '//*[@id="IExerciseList"]/li[',
							 'id2': ']/div[',
							 'id3': ']/div[',
							 'id4': ']/div[',
							 'id5': ']/div[',
							 'id6': ']'}





class_dashborad_central = 'ActiveIconText'
class_calendar_month = 'CalText'
class_calendar_month_click = 'Clickable'
class_item_text = 'CalItemText'


