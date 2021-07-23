from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from data import gosuslugi_password, gosuslugi_login, reference_year


options = webdriver.ChromeOptions()

profile = {
    "plugins.always_open_pdf_externally": True,
    "download.default_directory": os.getcwd(),
    }
options.add_experimental_option("prefs", profile)
options.add_argument("window-size=1200,900")
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0")

driver = webdriver.Chrome(
    executable_path=os.getcwd() + '/chromedriver',
    options=options
)

try:
    """Авторизация"""
    driver.get("https://esia.gosuslugi.ru/")
    time.sleep(3)

    username_input = driver.find_element_by_id("login")
    username_input.clear()
    username_input.send_keys(gosuslugi_login)

    password_input = driver.find_element_by_id("password")
    password_input.clear()
    password_input.send_keys(gosuslugi_password)

    password_input.send_keys(Keys.ENTER)
    time.sleep(3)

    """Копирование паспортных данных в отдельный текстовый файл"""
    passport_info = driver.find_elements_by_xpath("//div[@class='col span_6 dd']")[5].text
    with open('passport_info', 'a') as f:
        f.write(passport_info)

    """
    Заказ услуги 'Предоставление сведений из справки о доходах физического лица по форме 2-НДФЛ'. 
    В конце данного блока таймаут на 10 минут, так как справка выдается с задержкой.
    """
    if reference_year in range(2016, 2020):
        driver.get("https://www.gosuslugi.ru/358549/1/form")
        time.sleep(3)
        driver.find_element_by_xpath("//label[text()='Отчетный год']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//li[text()='" + str(reference_year) + "']").click()
        time.sleep(10)
        driver.find_element_by_xpath("//button[@id='Form.NavPanel.__nextStep']").click()
        time.sleep(600)

        """
        Скачивание запрашиваемой справки.
        """
        driver.get("https://lk.gosuslugi.ru/orders/all?type=ORDER,EQUEUE,APPEAL,CLAIM,COMPLEX_ORDER,SIGN")
        time.sleep(3)
        try:
            driver.find_element_by_class_name("close").click()
            time.sleep(2)
        except Exception as ex:
            print(ex)
        finally:
            driver.find_element_by_xpath("//div[@class='flex-1 flex-container-lg flex-container-md feed-content']").click()
            time.sleep(3)
            driver.find_element_by_xpath("//span[text()=' Ещё файлы ']").click()
            time.sleep(1)
            driver.find_element_by_xpath("//*[contains(text(), 'Cкачать в PDF')]").click()
            time.sleep(3)
    else:
        print("Недопустимый год для справки")

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
