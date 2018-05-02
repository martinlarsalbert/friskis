from selenium import webdriver as webdriver
import os.path
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import helper_methods
import time
sleep = 1

passwords = helper_methods.load_passwords(file_path='passwords.json')

user_key = 'martin'
user = passwords.get(user_key,None)
if user is None:
    raise ValueError('No user:%s' % user_key)

browser = webdriver.Chrome()
browser.implicitly_wait(100) # seconds

browser.get('https://onlinebokning.pastelldata.com/1000/')
helper_methods.switch_to_frame(browser=browser)

#time.sleep(10)
helper_methods.click_logga_in(browser=browser)
time.sleep(sleep)

helper_methods.fill_in_username(browser=browser,user=user)

helper_methods.fill_in_password(browser=browser,user=user)

helper_methods.click_login2(browser=browser)




monday_button = None
for day_button in day_buttons:
    if day_button.text == 'MÅNDAG':
        monday_button = day_button
        break
        
if monday_button is None:
    raise ValueError('Cannot find monday button')

monday_button.click()

rows = browser.find_elements_by_class_name('PGridRow')


inspiration = None
for row in rows:
    if (('Inspiration med tränare' in row.text) and
        'Västra Hamngatan' in row.text):
        
        inspiration = row
        print(row.text)
        break
        
if inspiration is None:
    raise ValueError('Cannot find inspiration')

inspiration.click()


book_button = browser.find_element_by_class_name('ModalBookButton')
book_button.click()


try:
    book_status = browser.find_element_by_class_name('BookStatus')
except:
    pass
else:
    raise ValueError(book_status.text)

browser.switch_to_frame('PASTELLDATA_WRAPPER_IFRAME_0')
bokningar = browser.find_element_by_xpath(r'//*[@id="bs-example-navbar-collapse-1"]/div/div[1]/div[1]/div/div/div[3]/div')

bokningar.click()

rows = browser.find_elements_by_class_name('PGridRow')

inspiration = None
for row in rows:
    if (('Inspiration med tränare' in row.text) and
        'Västra Hamngatan' in row.text):
        
        inspiration = row
        print(row.text)
        break
        
if inspiration is None:
    raise ValueError('Failed to book inspiration')
else:
    print('You are now booked on inspiration')



browser.quit()





