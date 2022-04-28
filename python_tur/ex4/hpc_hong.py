import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import json
import time
import datetime
from ext.hpc_hong_cfg import cfg
"""
class ExtConfig():
    def __init__(self):
        self.phc_url="https://myclass.ntu.edu.mo"   #edit
        self.phc_home_url=r"%s/templates/" % self.phc_url
        self.phc_circular_url=r"%s/home/eService/circular/" % self.phc_url
        self.phc_circular_title=r"-%s-"             #edit
        self.phc_form_url=r"{}/home/eService/circular/sign.php?CircularID=%s".format(self.phc_url)
        self.Users_JSON=r'[{"USR":"","SEC":""},{"USR":"","SEC":""}]'
cfg=ExtConfig()
"""    
import re
#init parameters

def sign_hpc(cfg,UserLogin,UserPassword):
    #init browser
    home_url=cfg.phc_home_url
    circular_url=cfg.phc_circular_url
    circular_title=cfg.phc_circular_title
    form_url=cfg.phc_form_url    
    if len(UserPassword)>10 and "=" in UserPassword:
        UserPassword=base64.b64decode(UserPassword.encode('ascii')).decode('ascii')
    elif len(UserPassword)>20:
        int_=[]
        for i in range(int(len(UserPassword)/4)):
            int_.append(int(UserPassword[i*4+2:(i+1)*4],16))
        UserPassword=base64.b64decode(bytes(int_)).decode('ascii')
    else:
        UserPassword_=base64.b64encode(UserPassword.encode('ascii')).decode('ascii')
        print(UserPassword_)
        b_=base64.b64encode(UserPassword.encode('ascii'))
        str_=[]
        for b__ in b_:
            str_.append(hex(b__))
        print("".join(str_))
    browser_driver_type="Firefox"
    browser=None
    if browser_driver_type=="Firefox":
        options = FirefoxOptions()
        options.add_argument('ignore-certificate-errors')
        browser = webdriver.Firefox( options=options)
    if browser_driver_type=="Chrome":
        options = ChromeOptions()
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
    #for links in browser.find_elements_by_css_selector('td.main_content a.tablelink'):
    #    if circular_title % today_date in links.text :
    #        pass          
    if browser_driver_type=="Firefox": #Chrome
        if  circular_title % today_date in browser.find_element_by_css_selector('td.main_content').text:
            continue_link = browser.find_element_by_link_text(circular_title % today_date)
            continue_link=re.search("\d+", continue_link.get_attribute("href")).group(0)
            continue_link=form_url % continue_link
            #go form
            browser.get(continue_link)
            if "已簽回"  in browser.find_element_by_id('html_body_frame').text:
                pass
            else:
                browser.find_element_by_id('FF01_2').click()
                browser.find_element_by_id('FF02_0').click()
                browser.find_element_by_id('FF03_2').click()
                browser.find_element_by_id('submitbtn').click()
    #release
    time.sleep(3)
    browser.quit()

if __name__ == '__main__':
    users = json.loads(cfg.Users_JSON)
    for _u in users:
        sign_hpc(cfg, _u["USR"], _u["SEC"])
