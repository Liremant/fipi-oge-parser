from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://oge.fipi.ru/bank/index.php?proj=B24AFED7DE6AB5BC461219556CCA4F9B")
    print('Page detected! Name:',driver.title)
    sleep(5)
    print(find_by_class('id-text',driver))

def loader_wait(driver):
    # Ждем пока исчезнет спиннер/лоадер
    try:
        WebDriverWait(driver, 20).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, "loader"))
        )
        print('loader over!')
    except:
        print('loader not over :(')
        pass

def find_by_class(class_name, driver):
    try:
        element = driver.find_element(By.CSS_SELECTOR, "div.id-text")
        return element
    except Exception as e:
        return 0, e 
main()



