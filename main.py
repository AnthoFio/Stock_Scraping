import time 
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

#set to true if you want to see the robot in action
DEBUG = False

logging.basicConfig(filename="boursorama_scrap.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(funcName)s %(levelname)s %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger()


def get_driver(debug):

    logger.info(f"Debug mode : {debug}")
    options = Options()
    prefs = {
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": False,
        "download.directory_upgrade": True,
        "useAutomationExtension":False
    }

    options.add_argument("start-maximized"); 
    options.add_argument("enable-automation"); 
    options.add_argument("--no-sandbox"); 
    options.add_argument("--disable-dev-shm-usage"); 
    options.add_argument("--disable-browser-side-navigation"); 
    options.add_argument("--disable-gpu");
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--enable-unsafe-swiftshader")

    if(not debug):
        options.add_argument("--headless")
        options.add_argument("--window-size=1325x744")
        
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Edge(options=options)
    
    return driver


def click_first_search_icon(driver):
    driver.find_elements(By.CLASS_NAME, "u-display-block")[1].click()

def click_element(element):
    if(element != None):
        element.click()

def fill_element(element,value):
    if(value != None):
        element.send_keys(value)
        element.send_keys(u'\ue007')

if __name__ == "__main__":
    driver = get_driver(DEBUG)

    driver.get('https://www.boursorama.com/')

    wait = WebDriverWait(driver, 20)

    if DEBUG == True:
        logger.info("Waiting for cookie modal to be clickable...")
        cookie_modal = wait.until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")))
        cookie_modal.click()


    stocks = ["BNP", "AIR", "MC", "CA", "DG", "OR", "EN", "ENGI", "ML", "VIV"]
    for stock in stocks:    
        time.sleep(1)
        click_first_search_icon(driver)
        fill_element(driver.find_elements(By.NAME, "search[keywords]")[0], stock)
        time.sleep(1)
        zone_data = driver.find_element(By.CLASS_NAME, "c-faceplate__body")
        value = zone_data.find_element(By.CLASS_NAME, "c-instrument").text
        currency = zone_data.find_element(By.CLASS_NAME, "c-faceplate__price-currency").text
        variation = zone_data.find_element(By.CLASS_NAME, "c-instrument--variation").text
        logger.info(f"Value read for {stock} : {value} {currency} - variation : {variation}")
