import datetime
from browser.BrowserUtil import ChromeBrowserUtil, SafariBrowserUtil
from browser.BrowserUtil import FirefoxBrowserUtil
import os
from selenium.webdriver.common.by import By

if not os.path.exists("./firefox"):
    os.mkdir("./firefox")

site_link = "https://www.getcalley.com/page-sitemap.xml"

def takeScreenOfDifferentResolution(browser,browser_name):
    mobile_resolutions = {"galaxy note 3": {"height": 360, "width": 640}, "iphone6-7-8": {"height": 375, "width": 667},
                          "iphone xr-11": {"height": 414, "width": 896}}
    desktop_resolutions = {"Dell XPS": {"height": 1920, "width": 1080},
                           "HP Pavillion 151": {"height": 1366, "width": 768},
                           "Acer Aspire series": {"height": 1536, "width": 864}}

    browser.maximise_browser_window()

    for link in topFiveSiteLinks:
        browser.getPage(link)
        for (mobile, resolution) in mobile_resolutions.items():
            browser.setBrowserResolution(resolution["height"], resolution["width"])
            dir_path = os.path.join(os.getcwd(), browser_name, mobile, f"{resolution['height']}x{resolution['width']}")
            png_name = f"screenshot_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            print("taken screen shot for device", mobile,
                  browser.takeScreenShot(dir_path, png_name, full_page=False))

        for (desktop, resolution) in desktop_resolutions.items():
            browser.setBrowserResolution(resolution["height"], resolution["width"])
            dir_path = os.path.join(os.getcwd(), browser_name, desktop, f"{resolution['height']}x{resolution['width']}")
            png_name = f"screenshot_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            print(browser.takeScreenShot(dir_path, png_name, full_page=False))


firefox_browser = FirefoxBrowserUtil(".")

firefox_browser.getPage(site_link)

topFiveSiteLinks = []

try:
    for a_tag in  firefox_browser.getElements(By.CSS_SELECTOR,'td a[href*="https://"]')[:5]:
        topFiveSiteLinks.append(a_tag.get_attribute("href"))

    takeScreenOfDifferentResolution(firefox_browser,"firefox")

    firefox_browser.closeBrowser(".")
except Exception as e:
    print(e)

try:
    chrome_browser = ChromeBrowserUtil()
    if not os.path.exists("./chrome"):
        os.mkdir("./chrome")
    takeScreenOfDifferentResolution(chrome_browser,"chrome")
except Exception as e:
    print(e)


try:
    if not os.path.exists("./safari"):
        os.mkdir("./safari")
    safari_browser = SafariBrowserUtil()
    takeScreenOfDifferentResolution(safari_browser,"safari")
except Exception as e:
    print(e)