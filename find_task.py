from selenium.webdriver.common.by import By

def loader_wait(driver):
    try:
        WebDriverWait(driver, 20).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, "loader"))
        )
        print('loader end')
    except Exception as e:
        print(f'error:{e}')
        pass

def find_tasks(name, driver):
    try:
        element = driver.find_element(By.ID,name)
        title = element.text
        print("текст",title)
    except Exception as e:
        return (f'error!reason:{e}') 