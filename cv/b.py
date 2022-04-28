from selenium import webdriver
from selenium.webdriver.chrome.options import Options
home_url="chrome://dino"
options = Options()
options.add_argument('ignore-certificate-errors')
browser = webdriver.Chrome('./ext/chromedriver', options=options)
browser.set_window_size(650,350)  #browser.maximize_window()
browser.get(home_url)