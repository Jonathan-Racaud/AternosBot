import os
import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from load_conf import load_yaml

conf = load_yaml("conf.yaml")
USER = conf['user']['username']
PASSWORD = conf['user']['password']
SERVER = conf['host']['aternos']

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(options=options)
async def start_server(ctx):
    driver.get(SERVER)

    __login(driver)
    await ctx.send("Connected to the server administration")
    time.sleep(3)
    
    __accept_learn_more(driver)
    __start(driver)
    await ctx.send("Asked to start the server")
    time.sleep(3)
    
    __accept_notifications(driver)
    await ctx.send("Accepted notifications")
    
    state = False
    while state == False:
        print("working")
        status = driver.find_element_by_xpath('//*[@id="nope"]/main/section/div[3]/div[2]/div/div/span[2]/span')
        
        if status.text == "Waiting in queue":
            await ctx.send("Waiting in queue")
            try:
                element = driver.find_element_by_xpath('//*[@id="confirm"]')
                print("found")
                element.click()
                state = True
                await ctx.send("Confirmed server creation. The server will be online shortly")
            except:
                print("except")
                pass
        
        time.sleep(30)
    driver.close()

def __login(driver):
    e = driver.find_element_by_xpath('//*[@id="user"]')
    e.send_keys(USER)

    e = driver.find_element_by_xpath('//*[@id="password"]')
    e.send_keys(PASSWORD)
    
    e = driver.find_element_by_xpath('//*[@id="login"]')
    e.click()

def __start(driver):
    e = driver.find_element_by_xpath('//*[@id="start"]')
    e.click()
 
def __accept_learn_more(driver):
    e = driver.find_element_by_xpath('//*[@id="sncmp-popup-ok-button"]')
    e.click()

def __accept_notifications(driver):
    e = driver.find_element_by_xpath('//*[@id="nope"]/main/div/div/div/main/div/a[1]')
    e.click()
 
