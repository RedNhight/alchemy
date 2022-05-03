# Faker
from faker import Faker

# Undetected selenium imports
import undetected_chromedriver.v2 as uc

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec

# Other imports
import os
import random
from time import sleep


class Alchemy:
    def __init__(self, data):
        self.name = ''
        self.surname = ''
        self.data = data.split(':')
        login = self.data[0]
        password = self.data[1]
        self.redir_status = 'Nope'
        self.status = 'successful'
        self.data = [login, password]
        print(self.data)
        self.link = 'https://auth.alchemyapi.io/signup'

        self.opt = uc.ChromeOptions()
        # self.opt = webdriver.ChromeOptions()
        # Основные настройки отпечатков.
        self.opt.add_argument('--load-extension=/home/penguin_nube/plugins/AntiCaptcha')
        self.opt.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.opt.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        self.opt.add_argument('--disable-dev-shm-usage')
        self.opt.add_argument("--disable-infobars")
        with open('proxies.txt', 'r') as proxy_list:
            proxies = proxy_list.readlines()
            if len(proxies) > 0:
                proxy = random.choice(proxies)
                self.opt.add_argument('--proxy-server=http://%s' % proxy)
            proxy_list.close()

        caps = webdriver.DesiredCapabilities.CHROME
        caps['acceptSslCerts'] = True
        self.driver = uc.Chrome(options=self.opt, desired_capabilities=caps)
        # self.driver = webdriver.Chrome(options=self.opt, desired_capabilities=caps)
        # Заменяем отпечатки, на манер операционной системы, названия GPU, CPU и так далее.
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.maximize_window()
        self.wait = lambda x: WebDriverWait(self.driver, x)

    def login(self):
        fake = Faker()
        name = fake.name().split(' ')
        self.name = name[0]
        self.surname = name[1]
        self.driver.get(self.link)
        first_name = self.wait(10).until(ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div[2]/div/div/div[2]/form/label[1]/input')))
        first_name.click()
        first_name.send_keys(name[0])
        sleep(2)

        last_name = self.wait(10).until(ec.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div[2]/div/div/div[2]/form/label[2]/input')))
        last_name.click()
        last_name.send_keys(name[1])
        sleep(2)

        mail = self.wait(10).until(ec.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div[2]/div/div/div[2]/form/label[3]/input')))
        mail.click()
        mail.send_keys(self.data[0])
        sleep(2)

        passwd = self.wait(10).until(ec.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div[2]/div/div/div[2]/form/label[4]/input')))
        passwd.click()
        passwd.send_keys(self.data[1])
        first_name.send_keys(Keys.TAB)
        first_name.send_keys(Keys.ENTER)

    def check_workable(self):
        txt = self.wait(5).until(ec.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div[2]/div/div/div/div[1]')))

    def driver_close(self):
        self.driver.close()

    def save_screen(self):
        self.driver.save_screenshot(f'files/{self.data[0]}.png')

    def save_status(self):
        if self.status == 'success':
            with open('successful.txt', 'a') as output:
                output.write(f'{self.data[0]}:{self.data[1]}:{self.name}:{self.surname}')
                output.close()
        else:
            with open('unsuccessful.txt', 'a') as output:
                output.write(f'{self.data[0]}:{self.data[1]}:{self.name}:{self.surname}')
                output.close()


if __name__ == '__main__':
    dc = Alchemy('')
    dc.login()

