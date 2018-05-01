from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json

def load_passwords(file_path = 'passwords.json'):
    with open(file_path,'r') as file:
        passwords = json.load(file)

    return passwords

def switch_to_frame(browser):
    try:
        element = WebDriverWait(browser, 10).until(
            EC.frame_to_be_available_and_switch_to_it('PASTELLDATA_WRAPPER_IFRAME_0')
        )
    except:
        raise
