from selenium import webdriver as webdriver

import os.path
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import helper_methods
import time
import smtplib
sleep = 3
import logging
import sys
from logging import handlers

log = logging.getLogger('')
log.setLevel(logging.INFO)
format = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)

fh = handlers.RotatingFileHandler('friskis.log', maxBytes=(1048576*5), backupCount=7)
fh.setFormatter(format)
log.addHandler(fh)

logging.info('\n\n____________ Friskis is launched _____________')

passwords = helper_methods.load_passwords(file_path='passwords.json')

user_key = 'martin'
user = passwords.get(user_key,None)
if user is None:
    raise ValueError('No user:%s' % user_key)

try:
    logging.info('Create a browser...')
    browser = webdriver.Firefox()
    logging.info('Create a browser created')

    browser.implicitly_wait(100) # seconds

    return_string = helper_methods.logon_user_and_book(browser=browser,user = user,day = 'ONSDAG',search_words=['Yoga', 'Torslanda'])

except Exception as e:

    return_string = str(e)
    logging.error(return_string)

    filename = 'error.png'
    browser.save_screenshot(filename=filename)
    logging.info('screen shot has been saved to:%s' % filename)

finally:
    logging.info(return_string)
    browser.quit()

# mport smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

msg = EmailMessage()

me = "marale@kth.se"
you = "marale@kth.se"
msg['Subject'] = 'Friskis booking'
msg['From'] = me
msg['To'] = you
msg.set_content(return_string)

# Send the message via our own SMTP server.
try:
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
except:
    logging.error('Failed to email')
else:
    s.quit()
    logging.info('Email has been send')

logging.info('________________ Friskis has ended ______________')

browser.find