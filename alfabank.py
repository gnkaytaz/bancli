#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display


def GetBalance(username, password):
  driver = webdriver.Firefox()
  #assert "Интернет-банк" in driver.title
  
  driver.get("https://click.alfabank.ru")
  try:
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
  except:
    print "username form is not found"
    driver.quit()
  
  elem.send_keys(username)
  
  try:
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
  except:
    print "password form is not found"
    driver.quit()
  
  elem.send_keys(password)
  
  elem.send_keys(Keys.RETURN)
  
  #### USSD #####
  
  try:
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pt1:password_key::content"))
    )
  except:
    print "USSD password form is not found"
    driver.quit()

  ussd_code = raw_input('USSD password:')
  elem.send_keys(ussd_code)
  
  try:
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pt1:next_button::button"))
    )
  except:
    print "Next button is not found."
    driver.quit()
  elem.click()

  # Go to balance page
  try:
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pt1:menu:ATP2_r1:0:i1:0:cl2"))
    )
  except:
    print "Next button is not found."
    driver.quit()
  elem.click()

  # Balance cell searching
  try:
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pt2:i1:1:s10:cf12"))
    )
  except:
    print "Table is not found"
    driver.quit()

  print elem.text

  
  return driver
  # get html source 
  #source=driver.page_source

def main():
  display = Display(visible=0, size=(1366, 768))

  # now Firefox will run in a virtual display. 
  # you will not see the browser.
  display.start()

  username = raw_input("Username:")
  password = getpass.getpass("Password:")
  driver = GetBalance(username, password)
  driver.close()
  display.stop()

if __name__ == "__main__":
    main()
#assert "No results found." not in driver.page_source
#driver.close()


