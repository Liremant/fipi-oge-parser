from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from find_task import loader_wait, find_tasks
url = 'https://oge.fipi.ru/bank/index.php?proj=B24AFED7DE6AB5BC461219556CCA4F9B'

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url) # open page with tasks1
    print(find_tasks("checkform4D1B4F",driver))
    print('end main')

main() # run code



