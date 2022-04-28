from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
import ext.config as cfg
import re
#init parameters
home_url=cfg.pk_home_url
circular_url=cfg.pk_circular_url
circular_title=cfg.pk_circular_title
form_url=cfg.pk_form_url
UserLogin=cfg.pk_UserLogin
UserPassword=cfg.pk_UserPassword
#init browser
options = Options()
options.add_argument('ignore-certificate-errors')
browser = webdriver.Chrome('./ext/chromedriver', options=options)
browser.maximize_window()
#go home_url
browser.get(home_url)
browser.find_element_by_id('UserLogin').send_keys(UserLogin)
browser.find_element_by_id('UserPassword').send_keys(UserPassword)
browser.find_element_by_id('login_btn').click()
#go circular
browser.get(circular_url)
today_date = datetime.date.today().isoformat().replace("-","",2)
links=browser.find_elements_by_css_selector("a.tablebluelink")
for li in links:
    if li.text== circular_title % today_date:
        continue_link = browser.find_element_by_link_text(circular_title % today_date)
        continue_link=re.search("\d+", continue_link.get_attribute("href")).group(0)
        continue_link=form_url % continue_link
        #go form
        browser.get(continue_link)
        if "已簽"  in browser.find_element_by_class_name('form_table_v30').text:
            pass
        else:
            browser.find_element_by_id('FF01_2').click()
            browser.find_element_by_id('FF02_0').click()
            browser.find_element_by_id('FF03_2').click()
            #browser.find_element_by_id('submitbtn').click()
#release
time.sleep(100)
browser.quit()
