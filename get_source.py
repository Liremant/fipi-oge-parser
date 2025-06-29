from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
from selenium.webdriver.support.ui import WebDriverWait
import os
logger = logging.getLogger(__name__)

def get_url():
    url = int(input('Paste here link to FIPI with task list or choose preloaded pages:\n1.Physic\n'))
    match url:
        case 1:
            return 'https://oge.fipi.ru/bank/index.php?proj=B24AFED7DE6AB5BC461219556CCA4F9B' 
        case _:
            return url

def init_driver(url):
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')
    options.add_argument('--ignore-certificate-errors-spki-list')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

def get_page_frame(driver,page_num):
    try:
        os.makedirs(".cache/frames", exist_ok=True )
        driver.switch_to.frame("questions_container")
        with open(f".cache/frames/frame_{page_num}.html", "w") as f:
            source = driver.page_source
            f.write(source)
            logger.info('source saved')
            return source
    except Exception as e:
        logger.error(e)


def get_current_page(driver):
    try:
        driver.switch_to.default_content()
        current_page = driver.find_element(By.CSS_SELECTOR, "li.active")     
        current_page_num = current_page.get_attribute("p")
        logger.debug(f'trying return current_page_num{current_page_num}')
        return current_page_num
    except Exception as e:
        logger.error(f"could not get current page. Error: {e}")
        return None

def go_to_next_page(driver, page_num):
    try:
        driver.switch_to.default_content()
        nxt_page=int(page_num)+1
        page = f'li.button[p="{nxt_page}"]'
        logger.debug(f'trying get page {page}')
        element = driver.find_element(By.CSS_SELECTOR, page)  
        element.click()
        logging.debug(f'page {nxt_page} clicked!')
        wait_for_loader_hidden(driver)
        logging.debug('waiting for loader')        
        return True
    except Exception as e: 
        logger.error(f"Failed to click on page {int(page_num)+1}. Error: {e}")
        return False

def wait_for_loader_hidden(driver, timeout=120):
    wait = WebDriverWait(driver, timeout)
    
    # wait before "style" is not  "display: none;"
    wait.until(lambda d: d.find_element(By.ID, "loader_container").get_attribute("style") == "display: none;")



def resume_prev(driver,count):
    ans = input('Do you wanna resume your previous parsing?Y if yes,N if no.(default N)\n')
    match ans:
        case "Y":
            logger.debug('resuming from previous parse stop')
            driver.switch_to.default_content()
            page = count // 10
            element = driver.find_element(By.CSS_SELECTOR, "i.filter-button-arrow:nth-child(2)")
            element.click()
            input_field = driver.find_element(By.CSS_SELECTOR, "#n_pager_pno")
            input_field.send_keys(page)
            input_field.send_keys(Keys.RETURN)
        case _:
            logger.debug('resume option skipped,checking from start')
            pass