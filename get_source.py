from selenium import webdriver
from selenium.webdriver.chrome.options import Options
def get_src(url):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url) 
    try:
        # i found <iframe id="name="questions_container" src="questions.php?proj=B24AFED7DE6AB5BC461219556CCA4F9B&init_filter_themes=1"></iframe> <!--  --> in source,need get it
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
