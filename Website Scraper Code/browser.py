from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
def web_driver(
        chromedriver_path = r"D:\chromedriver-win64\chromedriver-win64\chromedriver.exe",
        browser_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        headless: bool = False
):
    service = Service(executable_path=chromedriver_path)
    option = Options()
    option.binary_location = browser_path
    if headless:
        option.add_argument("--headless=new")
    return webdriver.Chrome(service = service, options= option)
