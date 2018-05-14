#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import datetime
import time
import pdb

sleep = 3

import logging
logging.basicConfig(filename='friskis.log',level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')

wait = 20 #[s]

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
    #try:
    #    day_buttons = WebDriverWait(browser,wait).until(
    #        EC.presence_of_all_elements_located((By.CLASS_NAME,"DayButton")))#
    #except:
    #    raise

    day_buttons = browser.find_elements_by_class_name("DayButton")

    return day_buttons

def _get_day_button_name(day):
    days = ['MÅNDAG', 'TISDAG', 'ONSDAG', 'TORSDAG', 'FREDAG', 'LÖRDAG', 'SÖNDAG']

    if not day in days:
        raise ValueError('Invalid day format:%s' % day)

    date = datetime.datetime.now()
    today_i = date.weekday()
    day_i = days.index(day)

    if today_i == day_i:
        return 'IDAG'

    if (today_i + 1 == day_i) | (today_i + 1 == day_i + 7):
        return 'IMORGON'

    else:
        return day

def find_exercise_in_rows(rows,search_words):
    exercise = None
    for row in rows:
        for search_word in search_words:
            ok = True
            if not search_word in row.text:
                ok = False
                break
        if ok:
            exercise = row
            break

    return exercise

def book(browser,day,search_words):

    logging.info('Do the booking: %s at %s' % (search_words,day))

    logging.info('Get day button name...')
    day_button_name = _get_day_button_name(day)
    logging.info('Day button name is:%s' % day_button_name)

    logging.info('Find the day button...')
    #day_buttons = find_day_buttons(browser=browser)
    #day_buttons = browser.find_elements_by_class_name("DayButton")

    #ok = False
    #for i,day_button in enumerate(day_buttons):
    #    if day_button.text == day_button_name:
    #        ok = True
    #        real_day_button = day_button
    #        real_day_button.click()
    #        break
#
    #if not ok:
    #    raise ValueError('Cannot find %s button' % day_button_name)


    #pdb.set_trace()
    real_day_button = browser.find_element_by_xpath(r'//*[@id="viewtabcontrol"]/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div')
    real_day_button.click()

    logging.info('The following day buttons have been found: %s' % real_day_button.text)
    #time.sleep(5)

    logging.info('Click the day button')


    logging.info('Wait 20 s')
    time.sleep(5)

    #browser.switch_to_default_content()
    logging.info('Load all the rows...')
    try:
        rows = WebDriverWait(browser,wait).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME,'PGridRow'))
        )
    except:
        raise
    else:
        logging.info('Rows loaded. Now find the exercise...')
        exercise = find_exercise_in_rows(rows = rows,search_words = search_words)

    #rows = browser.find_elements_by_class_name('PGridRow')
    exercise = find_exercise_in_rows(rows = rows,search_words = search_words)

    if exercise is None:
        raise ValueError('Cannot find the exercise:%s on %s' % (search_words,day))

    logging.info('Exercise found, now click on it...')
    exercise.click()

    try:
        book_button = WebDriverWait(browser,wait).until(
            EC.element_to_be_clickable((By.CLASS_NAME,'ModalBookButton'))
        )
    except:
        raise

    logging.info('Now click the book button')
    browser.switch_to_default_content()
    switch_to_frame(browser=browser)

    book_button.click()

    #Check error status if present:
    try:
        book_status = browser.find_element_by_class_name('BookStatus')
    except:
        pass
    else:
        if (book_status.text == 'Bokning genomförd'):
            return exercise.text
        else:
            raise ValueError(book_status.text)

    logging.info('Check the booking...')
    #Check the booking:
    try:
        element = WebDriverWait(browser, wait).until(
           EC.frame_to_be_available_and_switch_to_it('PASTELLDATA_WRAPPER_IFRAME_0')
        )
    except:
        raise

    try:
        bokningar = WebDriverWait(browser,wait).until(
            EC.element_to_be_clickable((By.XPATH,r'//*[@id="bs-example-navbar-collapse-1"]/div/div[1]/div[1]/div/div/div[3]/div'))
        )
    except:
        raise

    bokningar.click()

    try:
        rows = WebDriverWait(browser,wait).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME,'PGridRow'))
        )
    except:
        raise

    exercise = find_exercise_in_rows(rows=rows,search_words = search_words)

    if exercise is None:
        raise ValueError('Failed to book the exercise:%s on %s' % (search_words,day))
    else:
        return exercise.text


def logon_user_and_book(browser,user,day,search_words):

    logging.info('Loging in:%s' % user['user_name'])

    logging.info('Go to friskis...')
    browser.get('https://onlinebokning.pastelldata.com/1000/')
    switch_to_frame(browser=browser)

    # time.sleep(10)
    logging.info('Logging in')
    click_logga_in(browser=browser)
    time.sleep(sleep)

    logging.info('Filling in user name')
    fill_in_username(browser=browser, user=user)

    logging.info('Filling in password')
    fill_in_password(browser=browser, user=user)

    logging.info('Click on the logon button')
    click_login2(browser=browser)
    logging.info('Logon for:%s, successfull!' % user['user_name'])

    # helper_methods.book(browser=browser,
    #                    day = 'MÅNDAG',
    #                    search_words=['Inspiration med tränare','Västra Hamngatan'])

    try:
        exercise_text = book(browser=browser,day=day,search_words=search_words)
    except:
        raise
    else:
        return_string =  '%s is now booked on the exercise:%s' % (user['user_name'],exercise_text)
        return return_string

