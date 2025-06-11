from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from time import sleep
def get_source(url):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url) 
    try:
        print('page loaded!')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'cell_0')))
        with open('путь/к/файлу.html', 'r', encoding='utf-8') as f: source = f.write(driver.page_source)
    except Exception as e:
        print(driver.page_source) #for test
        for _ in range(10): print('\n')
        print(f'error:\n{e}')
def get_url():
    #source = int(input('Paste here link to FIPI with task list'))
    return 'https://oge.fipi.ru/bank/index.php?proj=B24AFED7DE6AB5BC461219556CCA4F9B' # return source

def main():
    url = get_url()
    get_source(url)

if __name__ == "__main__":
    main()



