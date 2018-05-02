from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json

wait = 30 #[s]

def load_passwords(file_path = 'passwords.json'):
    with open(file_path,'r') as file:
        passwords = json.load(file)

    return passwords

def switch_to_frame(browser):
    try:
        element = WebDriverWait(browser, wait).until(
            EC.frame_to_be_available_and_switch_to_it('PASTELLDATA_WRAPPER_IFRAME_0')
        )
    except:
        raise

def click_logga_in(browser):
    try:
        logga_in1 = WebDriverWait(browser,wait).until(
            EC.element_to_be_clickable((By.XPATH,r'//*[@id="UserLoginInfoButton"]/div')))
    except:
        raise

    logga_in1.click()

class log_on_popup_is_present(object):

  def __init__(self):
      pass

  def __call__(self, browser):
    elements = browser.find_elements_by_id('UserName')

    if len(elements) > 1:
        return elements
    else:
        return False

class key_sent(object):

  def __init__(self,element,key):
      self.element = element
      self.key = key

  def __call__(self, browser):

    try:
        self.element.send_keys(self.key)
    except:
        return False
    else:
        return True

def fill_in_username(browser,user):

    try:
        user_names = WebDriverWait(browser,wait).until(
            log_on_popup_is_present())
    except:
        raise
    else:
        user_name = user_names[1]
        user_name.click()

    try:
        WebDriverWait(browser,wait).until(
            key_sent(element=user_name,key = user['user_name']))
    except:
        raise

def fill_in_password(browser,user):

    password = browser.find_elements_by_id('Password')[1]
    password.click()

    try:
        WebDriverWait(browser,wait).until(
            key_sent(element=password,key = user['password']))
    except:
        raise

def click_login2(browser):

    try:
        logga_in2 = WebDriverWait(browser,wait).until(
            EC.element_to_be_clickable((By.XPATH,'//*[@id="QuickLoginForm"]/div[6]/div[1]/div/div'))
        )
    except:
        raise

    logga_in2.click()

def find_day_buttons(browser):
    try:
        day_buttons = WebDriverWait(browser,wait).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME,))
            day_buttons = browser.find_elements_by_class_name("DayButton")
