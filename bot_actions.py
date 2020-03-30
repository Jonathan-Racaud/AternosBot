import os
import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from load_conf import load_yaml
import AternosParsingError

conf = load_yaml("/home/jracaud/.discord/bots/aternos/conf.yaml")
USER = conf['user']['username']
PASSWORD = conf['user']['password']
ATERNOS = conf['host']['aternos']
SERVER = conf['host']['server']

async def start_server(ctx):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(options=options)
    driver.get(ATERNOS)

    __login(driver)
    await ctx.send("Step 01/05: Logged in to the administration panel.")
    time.sleep(3)
    
    __accept_learn_more(driver)
    __start(driver)
    await ctx.send("Step 02/05: Started the server.")
    time.sleep(3)
    
    __accept_notifications(driver)
    await ctx.send("Step 03/05: Accepted rules.")
    
    status = "Waiting in queue"
    while status != "Online":
#        status = driver.find_element_by_xpath('//*[@id="nope"]/main/section/div[3]/div[2]/div/div/span[2]/span')
        status = __get_status(driver)

        if status == "Waiting in queue" and __confirm_start(driver):
            await ctx.send("Step 04/05: Confirmed server creation.")
        elif status == "Online":
            break
        elif status == "Offline":
            raise AternosParsingError("Something stopped the server")
        else:
            await ctx.send("[Info] Server status: {0}".format(status))
        time.sleep(30)
    await ctx.send("Step 05/05: Server is now ONLINE and ready for you to join")
    driver.close()

def get_status():
    page = requests.get(SERVER)
    tree = html.fromstring(page.content)
    status = tree.xpath('/html/body/div/div[3]/div/div/div[1]/span/text()')
    return status[0]

def get_number_of_players():
    page = requests.get(SERVER)
    tree = html.fromstring(page.content)
    status = tree.xpath('/html/body/div/div[4]/div/div/div/span[1]/text()')
    return status[0]

def __login(driver):
    e = driver.find_element_by_id('user')
    e.send_keys(USER)

    e = driver.find_element_by_id('password')
    e.send_keys(PASSWORD)
    
    e = driver.find_element_by_id('login')
    e.click()

def __start(driver):
    e = driver.find_element_by_id('start')
    e.click()
 
def __accept_learn_more(driver):
    e = driver.find_element_by_id('sncmp-popup-ok-button')
    e.click()

def __accept_notifications(driver):
    e = driver.find_element_by_xpath('//*[@id="nope"]/main/div/div/div/main/div/a[1]')
    e.click()

def __get_status(driver):
    e = driver.find_element_by_class_name('statuslabel-label')
    return e.text

def __confirm_start(driver):
    #TODO: Improve error checking so we don't rely on Excpetion for that
    try:
        e = driver.find_element_by_id('confirm')
        e.click()
        return True
    except ElementNotInteractableException as e:
        print(e)
        return False
