from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import sys
import time


username = sys.argv[1]
password = sys.argv[2]
url_post = sys.argv[3]

SCROLL_PAUSE_TIME = 1.5


def invitar_pagina(my_driver):
    try:

        mostrar = my_driver.find_element_by_xpath('//span[@role="toolbar"]/following-sibling::div//div[@role="button"]')
        mostrar.click()
        time.sleep(1.5)
        container_reacciones = my_driver.find_element_by_xpath('//div[@role="dialog"]/div[3]')
        container_scrolls = my_driver.find_element_by_xpath('//div[@role="dialog"]/div[3]/div[1]')

        last_height = container_scrolls.size

        while True:
            container_reacciones.send_keys(Keys.PAGE_DOWN)

            time.sleep(SCROLL_PAUSE_TIME)

            new_height = container_scrolls.size
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(2)
    except Exception as e:
        print(e)
        pass
    user_container_reaccion = container_reacciones.find_elements_by_css_selector('div[data-visualcompletion="ignore-dynamic"]')
    for reaccion_i in user_container_reaccion:
        try:
            button_follow = reaccion_i.find_element_by_css_selector('div[role="button"]')
            label = button_follow.get_attribute('aria-label')
            if label.startswith("Inv"):
                button_follow.click()
        except Exception as e:
            print(e)
            pass
        time.sleep(1.5)
        


my_driver = webdriver.Firefox()
my_driver.get('https://www.facebook.com/')
time.sleep(3)

try:
    text_username = my_driver.find_element_by_css_selector('input#email')
    text_username.send_keys(username)
    text_password = my_driver.find_element_by_css_selector('input#pass')
    text_password.send_keys(password)
    text_password.send_keys(Keys.RETURN)
    time.sleep(5)
    my_driver.get(url_post)
    time.sleep(5)
except Exception as e:
    print(e)
    pass

invitar_pagina(my_driver)
my_driver.close()