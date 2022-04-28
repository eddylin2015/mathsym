from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import ext.config as cfg
home_url=cfg.hpd_home_url
options = Options()
options.add_argument('ignore-certificate-errors')
browser = webdriver.Chrome('./ext/chromedriver', options=options)
browser.set_window_size(400,800)  #browser.maximize_window()
browser.get(home_url)
browser.switch_to.frame(0)
print(browser.find_element_by_class_name("bfg"))
browser.find_element_by_class_name("bfg").click()
browser.find_element_by_css_selector('input[name="agreement"]').click()
browser.find_element_by_class_name("check-agreement").click()
browser.find_element_by_css_selector('input[name="surname"]').send_keys(cfg.hpd_name)
browser.find_element_by_css_selector('select[name="sex"]').send_keys(cfg.hpd_sex)
browser.find_element_by_css_selector('select[name="dob_year"]').send_keys(cfg.hpd_dob_year)
select = Select(browser.find_element_by_css_selector('select[name="dob_month"]'))
select.select_by_visible_text(cfg.hpd_dob_month)
browser.find_element_by_css_selector('select[name="dob_day"]').send_keys(cfg.hpd_dob_day)
browser.find_element_by_css_selector('input[name="idType"][value="macauCard"]').click()
browser.find_element_by_css_selector('input[name="tel_type"][value="macau"]').click()
browser.find_element_by_css_selector('input[name="symptom"][value="99"]').click()
browser.find_element_by_css_selector('input[name="symptau"][value="N"]').click()
browser.find_element_by_css_selector('input[name="abefore_place"][value="no"]').click()
browser.find_element_by_css_selector('input[name="idNum"]').send_keys(cfg.hpd_idNum)
browser.find_element_by_css_selector('input[name="tel_macau"]').send_keys(cfg.hpd_tel_macau)
browser.find_element_by_id('btnSubmit').click()
browser.find_element_by_css_selector('input[name="select1"]').click()
browser.find_element_by_id('btnSubmit').click()
browser.find_element_by_css_selector("a.btn-success").click()
browser.find_element_by_id('no').click()
#browser.find_element_by_id('btnGenDeclaration').click()
browser.find_element_by_id('local').click()
time.sleep(3)
browser.save_screenshot(cfg.hpd_png)
browser.quit()

#from PIL import Image
#screenshot = Image.open(‘ss.png’)
#screenshot.show()
