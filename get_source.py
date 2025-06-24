from selenium import webdriver
from selenium.webdriver.chrome.options import Options
def get_src(url):
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')
    options.add_argument('--ignore-certificate-errors-spki-list')
    driver = webdriver.Chrome(options=options)
    driver.get(url) 
    try:
        driver.switch_to.frame("questions_container")
        with open("source_frame.html", "w") as f:
            source = driver.page_source
            f.write(source)
            print('source saved')
            return source
            

    except Exception as e:
        print('error!')
        return e
def get_url():
    #source = int(input('Paste here link to FIPI with task list'))
    return 'https://oge.fipi.ru/bank/index.php?proj=B24AFED7DE6AB5BC461219556CCA4F9B' # return source # rn just for test
