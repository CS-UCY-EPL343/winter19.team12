# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestLogoutTest():
	print("\nTestLogoutTest successfully passed")
	def setup_method(self, method):
		self.driver = webdriver.Chrome()
		self.vars = {}
  
	def teardown_method(self, method):
		self.driver.quit()
  
	def test_logoutTest(self):
		# Test name: Logout Test
		# Step # | name | target | value
		# 1 | open | / | 
		self.driver.get("http://fitbit1.eastus.cloudapp.azure.com:8080/")
		# 2 | setWindowSize | 1552x880 | 
		self.driver.set_window_size(1552, 880)
		# 3 | click | css=.q-item:nth-child(1) .q-item__label | 
		self.driver.find_element(By.CSS_SELECTOR, ".q-item:nth-child(1) .q-item__label").click()
		# 4 | runScript | window.scrollTo(0,0) | 
		self.driver.execute_script("window.scrollTo(0,0)")
		# 5 | click | css=.q-item:nth-child(8) .q-item__label | 
		self.driver.find_element(By.CSS_SELECTOR, ".q-item:nth-child(8) .q-item__label").click()

