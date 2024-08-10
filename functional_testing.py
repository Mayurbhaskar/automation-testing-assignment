from browser.BrowserUtil import FirefoxBrowserUtil
from selenium.webdriver.common.by import By
import os
from time import sleep

URL = "https://demo.dealsdray.com/"
USER_NAME_CSS_SELECTOR = 'input[id="mui-1"]'
USER_PASSWORD_CSS_SELECTOR = 'input[id="mui-2"]'
SUBMIT_BUTTON_CSS_SELECTOR='button[type="submit"]'
USERNAME="prexo.mis@dealsdray.com"
USER_PASSWORD="prexo.mis@dealsdray.com"
MAX_RETRY = 3
ORDER_SUB_MENU_CSS_SELECTOR = ".has-submenu"
ORDERS_MENU_XPATH_SELECTOR = '//button/span[text()="Orders"]'
ADD_BULK_ORDER_MENU_BUTTON_XPATH_SELECTOR = '//button[text()="Add Bulk Orders"]'
UPLOAD_BULK_ORDER_FILE_CSS_SELECTOR = 'input[id="mui-7"]'
FILE_LOCATION = os.path.join(os.getcwd(),"demo-data.xlsx")
IMPORT_ORDER_BUTTON_XPATH_SELECTOR ='//button[text()="Import"]'
DATA_VALIDATE_BUTTON_XPATH_SELECTOR ='//button[text()="Validate Data"]'

browser = FirefoxBrowserUtil(".")
browser.maximise_browser_window()

browser.getPage(URL)
try:
    while MAX_RETRY>0:
        user_name_input = browser.getElement(By.CSS_SELECTOR,USER_NAME_CSS_SELECTOR)
        password_input = browser.getElement(By.CSS_SELECTOR,USER_PASSWORD_CSS_SELECTOR)
        browser.sendTextToElement(user_name_input,USERNAME)
        browser.sendTextToElement(password_input,USER_PASSWORD)
        browser.clickElement(By.CSS_SELECTOR,SUBMIT_BUTTON_CSS_SELECTOR)
        sleep(5)
        if browser.getCurrentUrl() == "https://demo.dealsdray.com/mis/dashboard":
            break
        MAX_RETRY-=1

    assert MAX_RETRY > 0

    browser.clickElement(By.CSS_SELECTOR,ORDER_SUB_MENU_CSS_SELECTOR)
    browser.clickElement(By.XPATH,ORDERS_MENU_XPATH_SELECTOR)
    browser.clickElement(By.XPATH,ADD_BULK_ORDER_MENU_BUTTON_XPATH_SELECTOR)
    upload_button = browser.getElement(By.CSS_SELECTOR,UPLOAD_BULK_ORDER_FILE_CSS_SELECTOR)
    browser.sendTextToElement(upload_button,FILE_LOCATION)
    browser.clickElement(By.XPATH,IMPORT_ORDER_BUTTON_XPATH_SELECTOR)
    browser.clickElement(By.XPATH,DATA_VALIDATE_BUTTON_XPATH_SELECTOR)
    browser.acceptAlert()
    browser.scrollToElement(By.XPATH,'//td[text()="10"]')
    sleep(10)
    browser.takeScreenShot()

except Exception as e:
    print(e)
finally:
    browser.closeBrowser(".")



