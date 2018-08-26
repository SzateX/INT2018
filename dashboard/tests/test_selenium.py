from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.utils.timezone import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from INT2018 import settings
import os

from INT import models

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
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Prelegenci")]')))

    def test_logout(self):
        self.driver.get('%s%s' % (self.live_server_url, '/dashboard/login'))
        login(self.driver)
        logout_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Wyloguj')))
        logout_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Zostałeś wylogowany")]')))


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
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//a[(contains(text(), "Prelegenci")) and (contains(@class, "breadcrumb"))]')))

    def test_working_list(self):
        company = models.Company.objects.create(name="Testowa Firma", description="Fajny opis")
        speaker = models.Speaker.objects.create(name="Testowy", surname="Prelegent", description="Fajny opis",
                                                company_id=company)
        speakers_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Prelegenci")]')))
        speakers_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Prelegenci")) and (contains(@class, "breadcrumb"))]')))
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


class LecturesTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(LecturesTests, cls).setUpClass()
        cls.driver = webdriver.Firefox(executable_path=os.path.join(PATH_TO_DRIVERS_DIR, FIREFOX_EXE_NAME))
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(LecturesTests, cls).tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.driver.get('%s%s' % (self.live_server_url, '/dashboard/'))
        login(self.driver)
        super(LecturesTests, self).setUp()

    def test_button_work(self):
        lectures_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Prelekcje")]')))

        lectures_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//a[(contains(text(), "Prelekcje")) and (contains(@class, "breadcrumb"))]')))

    def test_working_list(self):
        t = datetime.strptime('2011-01-21 12:37:21', '%Y-%m-%d %H:%M:%S')
        place = models.Place.objects.create(building_name='PRZ', room_name='A61')
        lecture = models.Lecture.objects.create(begin_time=t, end_time=t,
                                                description='opis', title='title',
                                                place_id=place)
        lectures_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Prelekcje")]')))
        lectures_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Prelekcje")) and (contains(@class, "breadcrumb"))]')))
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = False
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if columns[2].text == lecture.title:
                self.assertEqual(columns[0].text, lecture.begin_time.strftime('%b. %d, %Y, %I:%M p.m.'))
                self.assertEqual(columns[1].text, lecture.end_time.strftime('%b. %d, %Y, %I:%M p.m.'))
                self.assertEqual(columns[3].text, str(place.building_name + ' ' + place.room_name))
                found = True
        self.assertTrue(found, "Could not find lecture on the list")


class CompaniesTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(CompaniesTests, cls).setUpClass()
        cls.driver = webdriver.Firefox(executable_path=os.path.join(PATH_TO_DRIVERS_DIR, FIREFOX_EXE_NAME))
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(CompaniesTests, cls).tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.driver.get('%s%s' % (self.live_server_url, '/dashboard/'))
        login(self.driver)
        super(CompaniesTests, self).setUp()

    def test_button_work(self):
        companies_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Firmy")]')))

        companies_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//a[(contains(text(), "Firmy")) and (contains(@class, "breadcrumb"))]')))

    def test_working_list(self):
        partner_status = models.PartnerStatus.objects.create(name='test_status')
        company = models.Company.objects.create(name="Testowa Firma", status_id=partner_status)
        companies_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Firmy")]')))
        companies_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Firmy")) and (contains(@class, "breadcrumb"))]')))
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = False
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if columns[1].text == company.name:
                self.assertEqual(columns[2].text, partner_status.name)
                found = True
        self.assertTrue(found, "Could not find company on the list")


class PlacesTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(PlacesTests, cls).setUpClass()
        cls.driver = webdriver.Firefox(executable_path=os.path.join(PATH_TO_DRIVERS_DIR, FIREFOX_EXE_NAME))
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(PlacesTests, cls).tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.driver.get('%s%s' % (self.live_server_url, '/dashboard/'))
        login(self.driver)
        super(PlacesTests, self).setUp()

    def test_button_work(self):
        places_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Miejsca")]')))

        places_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//a[(contains(text(), "Miejsca")) and (contains(@class, "breadcrumb"))]')))

    def test_working_list(self):
        place = models.Place.objects.create(building_name='PRZ', room_name='A61')
        places_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Miejsca")]')))
        places_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Miejsca")) and (contains(@class, "breadcrumb"))]')))
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = False
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if columns[0].text == place.building_name:
                self.assertEqual(columns[1].text, place.room_name)
                found = True
        self.assertTrue(found, "Could not find place on the list")


class StatusesTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(StatusesTests, cls).setUpClass()
        cls.driver = webdriver.Firefox(executable_path=os.path.join(PATH_TO_DRIVERS_DIR, FIREFOX_EXE_NAME))
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(StatusesTests, cls).tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.driver.get('%s%s' % (self.live_server_url, '/dashboard/'))
        login(self.driver)
        super(StatusesTests, self).setUp()

    def test_button_work(self):
        statuses_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Statusy")]')))

        statuses_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//a[(contains(text(), "Statusy")) and (contains(@class, "breadcrumb"))]')))

    def test_working_list(self):
        status = models.PartnerStatus.objects.create(name='test status')
        statuses_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Statusy")]')))
        statuses_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Statusy")) and (contains(@class, "breadcrumb"))]')))
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = False
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if columns[0].text == status.name:
                found = True
        self.assertTrue(found, "Could not find status on the list")


class NewsTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(NewsTests, cls).setUpClass()
        cls.driver = webdriver.Firefox(executable_path=os.path.join(PATH_TO_DRIVERS_DIR, FIREFOX_EXE_NAME))
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(NewsTests, cls).tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.driver.get('%s%s' % (self.live_server_url, '/dashboard/'))
        login(self.driver)
        super(NewsTests, self).setUp()

    def test_button_work(self):
        news_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Newsy")]')))

        news_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//a[(contains(text(), "News")) and (contains(@class, "breadcrumb"))]')))

    def test_working_list(self):
        t = datetime.strptime('2011-01-21 12:37:21', '%Y-%m-%d %H:%M:%S')
        news = models.News.objects.create(content='NEWS', title='title', creation_date=t, publish_date=t)
        news_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Newsy")]')))
        news_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Newsy")) and (contains(@class, "breadcrumb"))]')))
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = False
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if columns[0].text == news.title:
                self.assertEqual(columns[1].text, news.creation_date.strftime('%b. %d, %Y, %I:%M p.m.'))
                self.assertEqual(columns[2].text, news.publish_date.strftime('%b. %d, %Y, %I:%M p.m.'))
                found = True
        self.assertTrue(found, "Could not find news on the list")
