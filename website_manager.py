# External Libraries
from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests as req

# Built-in Libraries
import re
import time

def get_url_list(url: str, downs = 100) -> list:
	"""
	
	"""
	ser = Service()
	# options.add_argument('--headless')
	# options.add_argument('--disable-gpu') 
	browser = Chrome(service = ser)
	browser.get(url)
	time.sleep(1)
	body = browser.find_element(By.TAG_NAME, "body")

	while downs :
		body.send_keys(Keys.PAGE_DOWN)
		time.sleep(0.1)
		downs = downs - 1

	soup = bs(browser.page_source, "html.parser")

	pattern = re.compile("https://[a-z]*\.hashnode\.dev/.*")
	urls = []
	for item in soup.find_all("a", href = True, class_ = "block") :
		if pattern.match(item["href"]) :
			urls.append(item["href"])

	urls = list(set(urls))

	browser.close()
	return  urls

def get_text_from_url(url: str) -> str:
	page = req.get(url).text
	soup = bs(page, "html.parser")

	text = ""
	for elem in soup.find_all("p", text=True):
		text = text + " " + elem.getText()

	return text
