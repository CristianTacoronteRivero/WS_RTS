# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 16:42:37 2022

@author: crist
"""

from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime, timedelta
import calendar
import re
import pandas as pd

class ctrWS(webdriver.Chrome):
    def __init__(self, driver_path = os.getcwd(), teardown = False):
        self.driver_path = driver_path
        self.teardown = teardown

        if not driver_path in os.environ['PATH']:
            os.environ['PATH'] += os.pathsep + self.driver_path

        super(ctrWS, self).__init__()

        self.maximize_window()

    def __exit__(self, exce_type, exce_val, exce_tb):
        if self.teardown:
            self.quit()

    def get_url(self, url):
        self.get(url)

    def login(self, *arg):
        self.find_element(By.ID, 'Username').send_keys(arg[0])
        self.find_element(By.ID, 'Password').send_keys(arg[1])
        self.find_element(By.XPATH, '//*[@id="LoginForm2"]/div[3]/button[1]').click()

    def wait_presence_text(self, selector, locator , text, time = 100 ):
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
