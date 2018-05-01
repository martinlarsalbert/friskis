from selenium import webdriver as webdriver
import os.path
import json

with open('passwords.json','r') as file:
    passwords = json.load(file)

user_key = 'martin'
user = passwords.get(user_key,None)
if user is None:
    raise ValueError('No user:%s' % user_key)

browser = webdriver.Chrome()

browser.get('https://onlinebokning.pastelldata.com/1000/')

browser.switch_to_frame('PASTELLDATA_WRAPPER_IFRAME_0')



logga_in1 = browser.find_element_by_xpath(r'//*[@id="UserLoginInfoButton"]/div')
logga_in1.click()

user_name = browser.find_elements_by_id('UserName')[1]
user_name.click()
user_name.send_keys(user['user_name'])


password = browser.find_elements_by_id('Password')[1]
password.click()
password.send_keys(user['password'])

logga_in2 = browser.find_element_by_xpath('//*[@id="QuickLoginForm"]/div[6]/div[1]/div/div')
logga_in2.click()


day_buttons = browser.find_elements_by_class_name("DayButton")


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





