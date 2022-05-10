# External Libraries
from bs4 import BeautifulSoup as bs, SoupStrainer
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
	ser = Service(executable_path="D:\chromedriver_win32\chromedriver.exe")
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

	pattern = re.compile("https://[a-z]*\.hashnode\.dev/.*")
	links = SoupStrainer('a', href = pattern)
	soup = bs(browser.page_source, "html.parser", parse_only = links)

	urls = []
	for item in soup.find_all("a", href = True) :
		if pattern.match(item["href"]) :
			urls.append(item["href"])

	urls = list(set(urls))

	browser.close()
	return  urls

def get_text_from_url(url: str) -> str:
	page = req.get(url).text
	para = SoupStrainer('p')
	soup = bs(page, "html.parser", parse_only = para)

	text = ""
	for elem in soup.find_all("p", text=True):
		text = text + " " + elem.getText()

	return text
