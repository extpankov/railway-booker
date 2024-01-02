import os
import time

from dotenv import load_dotenv
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from scripts.generate_email import generate_email
from scripts.generate_person import generate_person
from scripts.generate_phone import generate_phone

load_dotenv()
months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

class Driver:
    def __init__(self):
        self.driver = None
    
    def init(self):
        service = Service("chromedriver/chromedriver")
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
        options.add_argument("--ignore-certificate-errors")
        print(os.getenv("PROXY"))
        proxy_options = {
            "proxy": {
                "https": os.getenv("PROXY"),
                "http": os.getenv("PROXY")
            }
        }
        self.driver = webdriver.Chrome(service=service, seleniumwire_options=proxy_options, options=options)

    def push(self, date, train_number, direction, carriage, location):
        driver = self.driver
        driver.get("https://psq-online.ru")
        time.sleep(1000)
        wait = WebDriverWait(driver, 10)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.find_element(By.ID, "passDepartureStation").send_keys(direction.split('-')[0].strip())
        time.sleep(0.5)
        driver.find_element(By.ID, "passDepartureStation").send_keys(Keys.ENTER)
        driver.find_element(By.ID, "passArrivalStation").send_keys(direction.split('-')[1].strip())
        time.sleep(0.5)
        driver.find_element(By.ID, "passArrivalStation").send_keys(Keys.ENTER)
        driver.find_element(By.ID, "thereDate").click()
        current_month = driver.find_element(By.CLASS_NAME, "ui-datepicker-month").text
        while driver.find_element(By.CLASS_NAME, "ui-datepicker-month").text != (months[int(date.split('.')[1]) - 1] if current_month != months[-1] else months[0]) and\
                driver.find_element(By.CLASS_NAME, "ui-datepicker-year").text != date.split('.')[2]:
            driver.find_element(By.CLASS_NAME, "ui-datepicker-next").click()
        for el in driver.find_element(By.CLASS_NAME, "ui-datepicker-calendar").find_elements(By.CSS_SELECTOR, "a.ui-state-default"):
            if int(el.text) == int(date.split('.')[0]):
                el.click()
                break
        time.sleep(0.5)
        for _ in range(2):
            driver.find_element(By.CLASS_NAME, "c-ticket-search__btn").click()
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        train = 0

        for el in driver.find_elements(By.CLASS_NAME, "c-run_short_re__train-number"):
            if el.text == train_number:
                train = el.find_element(By.XPATH, "./../../..")
                break
        train.find_element(By.CLASS_NAME, "c-run_short_re__price-block").find_element(By.TAG_NAME, "a").click()
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        carriage_el = 0
        for el in driver.find_elements(By.CLASS_NAME, "coach-list__chnum"):
            if el.find_element(By.XPATH, "./..").get_attribute("class") == "coach-list__bdcol_mob_wrapp":
                try:
                    if int(el.text.split(" ")[0]) == int(carriage):
                        carriage_el = el.find_element(By.XPATH, "./../../../..")
                        break
                except ValueError as e:
                    print(el.text)
                    print(e)
                    return 0
        els = carriage_el.find_element(By.CLASS_NAME, "coach-list__bdbrow").find_element(By.TAG_NAME, "form").find_element(By.CLASS_NAME, "coach-list__bdbschemas-cut").\
            find_elements(By.CSS_SELECTOR, "label.c-simple-check_ufs-place__field")
        for el in els:
            print(int(el.text.strip()))
            if int(el.text.strip()) == int(location):
                el.click()
                break
        time.sleep(1200)
        driver.find_elements(By.CLASS_NAME, "trwin__btn")[0].click()
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        person = generate_person()
        driver.find_element(By.CSS_SELECTOR, 'input#surname_1').send_keys(person.surname)
        driver.find_element(By.CSS_SELECTOR, 'input#name_1').send_keys(person.name)
        driver.find_element(By.CSS_SELECTOR, 'input#lastname_1').send_keys(person.lastname)
        driver.find_element(By.CSS_SELECTOR, 'input#birthdate_1').send_keys(Keys.BACKSPACE, person.birthdate)
        driver.find_element(By.CSS_SELECTOR, 'input#documentNumber_1').send_keys(person.passport)
        Select(driver.find_element(By.CSS_SELECTOR, 'select#sex_1')).select_by_value("F" if person.gender == "female" else "M")
        driver.find_element(By.CSS_SELECTOR, 'input#email').send_keys(generate_email())
        driver.find_element(By.CSS_SELECTOR, 'input#phone').send_keys(generate_phone())
        for el in driver.find_elements(By.CSS_SELECTOR, "label.c-chk__check"):
            el.click()
        driver.find_element(By.CSS_SELECTOR, 'input#notice-phone_1').send_keys(generate_phone())
        driver.find_element(By.CSS_SELECTOR, 'input#notice-email_1').send_keys(generate_email())
        time.sleep(10)
        driver.find_element(By.CLASS_NAME, "trwin__btn").click()
        time.sleep(30)

        driver.close()
        driver.quit()


driver = Driver()
driver.init()
driver.push("02.01.2024", "727М", "Москва - Нижний Новгород", "03", "04")
time.sleep(1200)
