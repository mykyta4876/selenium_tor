"""
pip install selenium
pip install pandas
pip install requests
pip3 install 2captcha-python
"""
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, os
import json
from enum import Enum
from datetime import datetime, timedelta
from twocaptcha import TwoCaptcha
import argparse

class OrderedEnum(Enum):
	def __ge__(self, other):
		if self.__class__ is other.__class__:
			return self.value >= other.value
		return NotImplemented
	def __gt__(self, other):
		if self.__class__ is other.__class__:
			return self.value > other.value
		return NotImplemented
	def __le__(self, other):
		if self.__class__ is other.__class__:
			return self.value <= other.value
		return NotImplemented
	def __lt__(self, other):
		if self.__class__ is other.__class__:
			return self.value < other.value
		return NotImplemented

class Errs(OrderedEnum):
	ErrorNoEmailValidate = -3
	Nothing= 0
	Fail = 1
	Ok = 2
	ErrorUsernameInstead = 3
	ErrorJunkEmail = 4
	ErrorNoExist = 5
	Other = 6

def check_exist_element_by_xpath(parent, browser, xapth):
	try:
		#button_job_title = browser.find_element(By.XPATH, xapth)
		button_job_title = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, xapth)))
	except NoSuchElementException:
		return False
	except TimeoutException:
		return False
	except StaleElementReferenceException:
		parent.refresh()
		ss = input("[--] check_exist_element_by_xpath: StaleElementReferenceException stoped **** press any key.")
		return False

	return True

def check_exist_element_by_class(browser, class_name):
	try:
		element = browser.find_element(By.CLASS_NAME, class_name)
	except NoSuchElementException:
		return False
	except StaleElementReferenceException:
		return False

	return True

def check_exist_element_by_name(browser, name):
	try:
		element = browser.find_element(By.NAME, name)
	except NoSuchElementException:
		return False

	return True

def login_func(url, flag_proxy, url_list, Sponsored_url_list, credentials_filename, sheet_name):
	func_text = "login_func"

	browser = None

	username = 'spqw1oair8'
	password = 'Datacenterproxy99_'
	endpoint = 'gate.dc.smartproxy.com'
	port = '20000'
	try:
		chrome_options = webdriver.ChromeOptions()

		if flag_proxy == True:
			proxies_extension = proxies(username, password, endpoint, port)
			chrome_options.add_extension(proxies_extension)

		#chrome_options.add_argument("--headless=new")

		browser = webdriver.Chrome(options=chrome_options)
		browser.get(url)
		browser.maximize_window()
	except WebDriverException:
		print(f"[-] {func_text}: selenium.common.exceptions.WebDriverException")
		time.sleep(5)
		return None
	
	try:
		browser.get(url)

	except TimeoutException:
		print(f"[-] {func_text}: selenium.common.exceptions.TimeoutException ")
		time.sleep(5)
		browser.close()
		browser.quit()
		return None
	except WebDriverException:
		print(f"[-] {func_text}: browser.get() selenium.common.exceptions.WebDriverException ")
		time.sleep(5)
		browser.quit()
		return None
		
	time.sleep(5)

	html_content = browser.page_source

	while True:
		try:
			username = browser.find_element(By.NAME, "username")
			username.send_keys("james064623")
			break
		except NoSuchElementException:
			print(f"[-] {func_text}: fail username (Element not found) ")
		except TimeoutException:
			print(f"[-] {func_text}: fail username TimeoutException ")
		except WebDriverException:
			print(f"[-] {func_text}: fail username WebDriverException.")
			browser.close()
			browser.quit()
			return None

	while True:
		try:
			password = browser.find_element(By.NAME, "password")
			password.send_keys("4esz%RDX^TFC")
			break
		except NoSuchElementException:
			print(f"[-] {func_text}: fail password (Element not found) ")
		except TimeoutException:
			print(f"[-] {func_text}: fail password TimeoutException ")
		except WebDriverException:
			print(f"[-] {func_text}: fail password WebDriverException.")
			browser.close()
			browser.quit()
			return None
	
	print(f"[-] {func_text}: waiting for your login")

	"""
	captcha_img_url = ""
	while True:
		try:
			captcha_img = browser.find_element(By.XPATH, "//img[@class='captcha']")
			captcha_img_url = captcha_img.get_attribute("src")
			time.sleep(5)
			break
		except NoSuchElementException:
			print(f"[-] {func_text}: fail login button (Element not found)")
		except WebDriverException:
			print(f"[-] {func_text}: fail login button WebDriverException.")
			browser.close()
			browser.quit()
			return None

	solver = TwoCaptcha(captcha_api_key)
	result = solver.normal(captcha_img_url)
	if result == None:
		print(f"[-] {func_text}: captcha not solved")
		browser.close()
		browser.quit()
		return None

	print(f"[-] {func_text}: captcha solved: {result['code']}")
	input()

	while True:
		try:
			captcha_response = browser.find_element(By.NAME, "captcha_1")
			captcha_response.send_keys(result['code'])
			break
		except NoSuchElementException:
			print(f"[-] {func_text}: fail captcha_response (Element not found) ")
		except TimeoutException:
			print(f"[-] {func_text}: fail captcha_response TimeoutException ")
		except WebDriverException:
			print(f"[-] {func_text}: fail captcha_response WebDriverException.")
			browser.close()
			browser.quit()
			return None
	

	while True:
		try:
			button = browser.find_element(By.XPATH, "//input[@type='submit']")
			browser.execute_script("arguments[0].click();", button)
			time.sleep(5)
			break

		except NoSuchElementException:
			print(f"[-] {func_text}: fail login button (Element not found)")
		except WebDriverException:
			print(f"[-] {func_text}: fail login button WebDriverException.")
			browser.close()
			browser.quit()
			return None
	"""
	return browser



def read_file(filepath):
	str_content = ""
	if os.path.isfile(filepath):
		f = open(filepath, mode="r", encoding="utf-8")
		str_content = f.read()
		f.close()
	else:
		print("[-] error: no exist " + filepath)
		exit(0)

	return str_content

def parse_arguments():
	parser = argparse.ArgumentParser(description="THREAT HOUND")

	# Add arguments
	parser.add_argument("--proxy", "-p", action="store_true", help="Set if do you use proxy", required=False)

	args = parser.parse_args()

	return args


start_url = "http://briansclcfyc5oe34hgxnn3akr4hzshy3edpwxsilvbsojp2gwxr57qd.onion/cvv/search/9145dac763362e4c99122c01d33f5d170b65aa03/"
#start_url = "http://briansclcfyc5oe34hgxnn3akr4hzshy3edpwxsilvbsojp2gwxr57qd.onion/cvv/search/b98ea8b0c64147ac5bb850e08b686cb2bfeb0dfc/"
#start_url = "http://briansclcfyc5oe34hgxnn3akr4hzshy3edpwxsilvbsojp2gwxr57qd.onion/dumps/"

if __name__ == "__main__":
	func_text = "main"

	# Parse command-line arguments
	args = parse_arguments()

	print("[-] start buying bins")

	browser = None
	while(True):
		if browser == None:
			browser = login_func(start_url, args.proxy, None, None, "", "")

			html_content = browser.page_source
			while html_content.find("Current server time:") == -1:
				time.sleep(1)
				html_content = browser.page_source
			
			print(f"[-] {func_text}: login success")
			browser.get(start_url)

		html_content = browser.page_source
		if html_content.find("all cards were sold") != -1:
			print(f"[-] {func_text}: no bins, refresh")
			browser.refresh()
			time.sleep(1)
			continue

		while True:
			while True:
				try:
					checkbox = browser.find_element(By.XPATH, "//input[@type='checkbox' and @onclick='selectAll(this.checked);']")
					time.sleep(1)
					browser.execute_script("arguments[0].click();", checkbox)
					print(f"[-] {func_text}: selected all bins in a page")
					break
				except NoSuchElementException:
					print(f"[-] {func_text}: fail checkbox (Element not found)")
				except WebDriverException:
					print(f"[-] {func_text}: fail checkbox WebDriverException.")
					browser.close()
					browser.quit()
					browser = None
					break
			
			if browser == None:
				break

			time.sleep(1)
			if check_exist_element_by_xpath(browser, browser, "//button[@onclick='addToCartSelected();']") == False:
				print(f"[-] {func_text}: no cart button, retry")
				continue

			try:
				button = browser.find_element(By.XPATH, "//button[@onclick='addToCartSelected();']")
				browser.execute_script("arguments[0].click();", button)
				print(f"[-] {func_text}: clicked cart button")
			except WebDriverException:
				print(f"[-] {func_text}: fail cart button WebDriverException.")
				browser.close()
				browser.quit()
				browser = None
				break
			
			if browser == None:
				break
			
			html_content = browser.page_source
			if html_content.find("all cards were sold") != -1:
				print(f"[-] {func_text}: putted all bins to cart")
				break

			if html_content.find("all items already added to the cart") != -1:
				print(f"[-] {func_text}: all items already added to the cart")
				break
		
		if browser == None:
			continue

		print(f"[-] {func_text}: going to cart")
		browser.get("http://briansclcfyc5oe34hgxnn3akr4hzshy3edpwxsilvbsojp2gwxr57qd.onion/cart/process/")
		print(f"[-] {func_text}: going to cart success")

		time.sleep(5)

		browser.get(start_url)
		print(f"[-] {func_text}: going to start url again")
