from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from INT2018 import settings
import os

from INT import models

from time import sleep

PATH_TO_DRIVERS_DIR = os.path.join(settings.BASE_DIR, "drivers")
FIREFOX_EXE_NAME = "geckodriver.exe" if os.name == 'nt' else "geckodriver"

USERNAME = "automat"
PASSWORD = "automat1234"


def login(driver):
    login_sign = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//a[contains(text(), "Logowanie")]')))
    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'form')))
    username_field = form.find_element(By.NAME, 'username')
    password_field = form.find_element(By.NAME, 'password')
    submit_button = form.find_element(By.TAG_NAME, 'button')
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    submit_button.click()


class AuthTests(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=os.path.join(PATH_TO_DRIVERS_DIR, FIREFOX_EXE_NAME))
        self.driver.maximize_window()
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.user.save()
        super(AuthTests, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(AuthTests, self).tearDown()

    def test_login(self):
        self.driver.get('%s%s' % (self.live_server_url, '/dashboard/login'))
        login(self.driver)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Prelegenci")]')))

    def test_logout(self):
        self.driver.get('%s%s' % (self.live_server_url, '/dashboard/login'))
        login(self.driver)
        logout_button: WebElement = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Wyloguj')))
        logout_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Zostałeś wylogowany")]')))


class SpeakersTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(SpeakersTests, cls).setUpClass()
        cls.driver = webdriver.Firefox(executable_path=os.path.join(PATH_TO_DRIVERS_DIR, FIREFOX_EXE_NAME))
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(SpeakersTests, cls).tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.driver.get('%s%s' % (self.live_server_url, '/dashboard/'))
        login(self.driver)
        super(SpeakersTests, self).setUp()

    def test_button_work(self):
        speakers_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Prelegenci")]')))

        speakers_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[(contains(text(), "Prelegenci")) and (contains(@class, "breadcrumb"))]')))

    def test_working_list(self):
        company = models.Company.objects.create(name="Testowa Firma", description="Fajny opis")
        speaker = models.Speaker.objects.create(name="Testowy", surname="Prelegent", description="Fajny opis", company_id=company)
        speakers_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Prelegenci")]')))
        speakers_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[(contains(text(), "Prelegenci")) and (contains(@class, "breadcrumb"))]')))
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = False
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if int(columns[0].text) == speaker.pk:
                self.assertEqual(columns[2].text, speaker.name)
                self.assertEqual(columns[3].text, speaker.surname)
                self.assertEqual(columns[4].text, company.name)
                found = True
        self.assertTrue(found, "Not found speaker in list")