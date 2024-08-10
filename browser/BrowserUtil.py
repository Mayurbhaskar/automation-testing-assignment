from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import glob
import os,time,platform
from selenium.webdriver.chrome.options import  ChromiumOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

class _BaseBrowserUtil:

    def __init__(self,driver):
        self.driver=driver

    def maximise_browser_window(self):
        self.driver.maximize_window()

    def setBrowserResolution(self,width,height):
        self.driver.set_window_size(width,height)

    def getPage(self,url):
        self.driver.get(url)

    def getTab(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def closeTab(self,tab=1):
        for tab in self.driver.window_handles[:tab]:
            try:
                self.driver.switch_to.window(tab)
                self.driver.close()
            except Exception as e:
                print("---------------------")
                print(e,tab)
                print("--------------------")
        self.switchToWindow(self.driver.window_handles[-1])

    def scrollTillElementDisplayed(self,by,selector):
        print("Scrolling")
        element = self.driver.find_element(by,selector)
        while not element.is_displayed():
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        print("done",element.is_displayed())

    def scrollToElement(self,by, selector):
        element = self.driver.find_element(by, selector)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def clickElement(self,by,element):
        try:
            # self.waitUntilElementIsDisplayed(by,element)
            # self.waitUntilElementIsClickable(by,element)
            self.driver.find_element(by,element).click()
            return True
        except Exception as e:
            print(e)
            return False

    def getCurrentUrl(self):
        return self.driver.current_url

    def getElement(self,by,element):
        # self.waitUntilElementIsDisplayed(by,element)
        return self.driver.find_element(by,element)

    def getElements(self,by,element):
        return self.driver.find_elements(by,element)

    def sendTextToElement(self,element : WebElement,text : str):
        try:
            element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            print(e)
            return False

    def selectOptions(self,by,element,textVal):
        ele = self.driver.find_element(by,element)
        select = Select(ele)
        select.select_by_visible_text(textVal)

    def waitUntilElementIsDisplayed(self,by,element):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((by, element)))


    def waitUntilElementIsClickable(self,by,element):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((by, element)))

    def waitUntilElementIsDisplayed(self,by,element,timeout=20):
        wait = WebDriverWait(self.driver,timeout)
        wait.until(EC.visibility_of_element_located((by,element)))

    def getSelectOptions(self,by,element):
        ele = self.driver.find_element(by,element)
        select = Select(ele)
        options = []
        for opts in select.options:
            options.append(opts.text)
        return options

    def exeJavascript(self,script):
        self.driver.execute_script(script)

    def getCurrentWindow(self):
        return self.driver.current_window_handle

    def getAllWindows(self):
        return self.driver.window_handles

    def switchToWindow(self,window_id):
        self.driver.switch_to.window(window_id)


    def closeBrowser(self,download_dir="."):
        while len(glob.glob(os.path.join(download_dir,"*.crdownload")))!=0:
            time.sleep(10)
        self.driver.quit()

    def acceptAlert(self):
        wait = WebDriverWait(self.driver,60)
        wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

    def takeScreenShot(self,screenshot_path=None,screenshot_file_name="test-screenshot.png",full_page=True):
        if screenshot_path ==None:
            png_path = os.path.join(os.getcwd(),screenshot_file_name)
        else:
            try:
                if not os.path.exists(screenshot_path):
                    os.makedirs(screenshot_path,exist_ok=True)
                png_path = os.path.join(screenshot_path,screenshot_file_name)
            except Exception as e:
                return e
        if full_page:
            flag = self.driver.save_full_page_screenshot(png_path)
        else:
            flag = self.driver.save_screenshot(png_path)
        return flag



class ChromeBrowserUtil(_BaseBrowserUtil):

    def __init__(self,download_dir="."):
        chrome_options = ChromiumOptions()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        super().__init__(self.driver)


class SafariBrowserUtil(_BaseBrowserUtil):

    def __init__(self,download_dir="."):
        if platform.system() != "Darwin":
            raise Exception("required mac platform to run test case")
        self.driver = webdriver.Safari()
        self.driver.implicitly_wait(10)
        super().__init__(self.driver)


class FirefoxBrowserUtil(_BaseBrowserUtil):

    def __init__(self,download_dir="."):
        firefox_options = Options()
        firefox_options.set_preference("browser.download.folderList", 2)
        firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_options.set_preference('browser.download.dir', download_dir)
        firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                       "application/octet-stream,application/vnd.ms-excel")  # Replace with your file MIME types
        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.implicitly_wait(10)

        super().__init__(self.driver)

