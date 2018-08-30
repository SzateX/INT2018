from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.utils.timezone import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait, Select
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

    def test_create_speaker(self):
        speakers_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Prelegenci")]')))
        speakers_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Prelegenci")) and (contains(@class, "breadcrumb"))]')))
        create_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[contains(text(), "Dodaj")]')))
        create_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Dodawanie prelegenta")) and (contains(@class, "breadcrumb"))]')))
        form: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'form')))
        name = form.find_element_by_name('name')
        name.send_keys('Janusz')
        surname = form.find_element_by_name('surname')
        surname.send_keys('Kowal')
        description = form.find_element_by_name('description')
        description.send_keys('Opis')
        submit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(), "Zatwierdź")]')))
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Prelegenci")) and (contains(@class, "breadcrumb"))]')))
        speaker = models.Speaker.objects.get(name='Janusz')
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
                found = True
        self.assertTrue(found, "Not found speaker in list")

    def test_edit_speaker(self):
        speaker = models.Speaker.objects.create(name="Testowy", surname="Prelegent", description="Fajny opis")
        speakers_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Prelegenci")]')))
        speakers_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Prelegenci")) and (contains(@class, "breadcrumb"))]')))
        edit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//i[contains(text(), "edit")]')))
        edit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Edytowanie prelegenta")) and (contains(@class, "breadcrumb"))]')))
        form: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'form')))
        name = form.find_element_by_name('name')
        name.send_keys('Janusz')
        surname = form.find_element_by_name('surname')
        surname.send_keys('Kowal')
        description = form.find_element_by_name('description')
        description.send_keys('Opis')
        submit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(), "Zatwierdź")]')))
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Prelegenci")) and (contains(@class, "breadcrumb"))]')))
        speaker2 = models.Speaker.objects.get(pk=speaker.pk)
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = False
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if int(columns[0].text) == speaker2.pk:
                self.assertEqual(columns[2].text, speaker2.name)
                self.assertEqual(columns[3].text, speaker2.surname)
                found = True
        self.assertTrue(found, "Not found speaker in list")

    def test_delete_speaker(self):
        speaker = models.Speaker.objects.create(name="Testowy", surname="Prelegent", description="Fajny opis")
        speakers_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Prelegenci")]')))
        speakers_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Prelegenci")) and (contains(@class, "breadcrumb"))]')))
        delete_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//i[contains(text(), "remove_circle")]')))
        delete_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Usuwanie prelegenta")) and (contains(@class, "breadcrumb"))]')))
        submit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(), "Potwierdzam")]')))
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Prelegenci")) and (contains(@class, "breadcrumb"))]')))
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = True
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if int(columns[0].text) == speaker.pk:
                found = False
        self.assertTrue(found, "Speaker found on the list")


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

    # def test_create_lecture(self):
    #     speaker = models.Speaker.objects.create(name="Testowy", surname="Prelegent", description="Fajny opis")
    #     place = models.Place.objects.create(building_name='PRZ', room_name='A61')
    #     lectures_button: WebElement = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH, '//span[contains(text(), "Prelekcje")]')))
    #     lectures_button.click()
    #     WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH, '//a[(contains(text(), "Prelekcje")) and (contains(@class, "breadcrumb"))]')))
    #     create_button: WebElement = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH, '//a[contains(text(), "Dodaj")]')))
    #     create_button.click()
    #     WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH, '//a[(contains(text(), "Dodawanie prelekcji")) and (contains(@class, "breadcrumb"))]')))
    #     form: WebElement = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.TAG_NAME, 'form')))
    #     begin_time_0 = form.find_element_by_name('begin_time_0')
    #     begin_time_0.send_keys('2018-08-27')
    #     begin_time_1 = form.find_element_by_name('begin_time_1')
    #     begin_time_1.send_keys('12:45:00')
    #     end_time_0 = form.find_element_by_name('end_time_0')
    #     end_time_0.send_keys('2018-08-27')
    #     end_time_1 = form.find_element_by_name('end_time_1')
    #     end_time_1.send_keys('13:45:00')
    #     description = form.find_element_by_name('description')
    #     description.send_keys('Opis')
    #     title = form.find_element_by_name('title')
    #     title.send_keys('Tytul')
    #     # select_place = Select(self.driver.find_element_by_xpath("//select[@name='place_id']"))
    #     select_place: WebElement = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH, '//select[@name="place_id"]')))
    #     select_place.click()
    #     select_place.select_by_visible_text('1 PRZ A61')
    #     select_speaker = Select(self.driver.find_element_by_xpath("//select[@name='speakers']"))
    #     select_speaker.select_by_visible_text(str(speaker))
    #     submit_button: WebElement = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH, '//button[contains(text(), "Zatwierdź")]')))
    #     submit_button.click()
    #     WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH, '//a[(contains(text(), "Prelekcje")) and (contains(@class, "breadcrumb"))]')))
    #     lecture = models.Lecture.objects.get(title='Tytul')
    #     table: WebElement = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.TAG_NAME, 'table')))
    #     tbody = table.find_element_by_tag_name('tbody')
    #     rows = tbody.find_elements_by_tag_name('tr')
    #     found = False
    #     for row in rows:
    #         columns = row.find_elements_by_tag_name('td')
    #         if columns[2].text == lecture.title:
    #             self.assertEqual(columns[0].text, lecture.begin_time.strftime('%b. %d, %Y, %I:%M p.m.'))
    #             self.assertEqual(columns[1].text, lecture.end_time.strftime('%b. %d, %Y, %I:%M p.m.'))
    #             self.assertEqual(columns[3].text, str(place.building_name + ' ' + place.room_name))
    #             found = True
    #     self.assertTrue(found, "Not found speaker in list")


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

    def test_create_company(self):
        companies_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Firmy")]')))
        companies_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Firmy")) and (contains(@class, "breadcrumb"))]')))
        create_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[contains(text(), "Dodaj")]')))
        create_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Dodawanie firmy")) and (contains(@class, "breadcrumb"))]')))
        form: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'form')))
        name = form.find_element_by_name('name')
        name.send_keys('Firma')
        description = form.find_element_by_name('description')
        description.send_keys('testowa')
        submit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(), "Zatwierdź")]')))
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Firmy")) and (contains(@class, "breadcrumb"))]')))
        company = models.Company.objects.get(name='Firma')
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = False
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if columns[1].text == company.name:
                found = True
        self.assertTrue(found, "Could not find company on the list")

    def test_edit_company(self):
        company = models.Company.objects.create(name="Firma")
        companies_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Firmy")]')))
        companies_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Firmy")) and (contains(@class, "breadcrumb"))]')))
        edit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//i[contains(text(), "edit")]')))
        edit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Edytowanie firmy")) and (contains(@class, "breadcrumb"))]')))
        form: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'form')))
        name = form.find_element_by_name('name')
        name.send_keys('EDIT')
        description = form.find_element_by_name('description')
        description.send_keys('testowa')
        submit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(), "Zatwierdź")]')))
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Firmy")) and (contains(@class, "breadcrumb"))]')))
        company2 = models.Company.objects.get(pk=company.pk)
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = False
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if columns[1].text == company2.name:
                found = True
        self.assertTrue(found, "Could not find company on the list")

    def test_delete_company(self):
        company = models.Company.objects.create(name="Firma")
        companies_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Firmy")]')))
        companies_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Firmy")) and (contains(@class, "breadcrumb"))]')))
        delete_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//i[contains(text(), "remove_circle")]')))
        delete_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Usuwanie firmy")) and (contains(@class, "breadcrumb"))]')))
        submit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(), "Potwierdzam")]')))
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Firmy")) and (contains(@class, "breadcrumb"))]')))
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = True
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if int(columns[1].text) == company.name:
                found = False
        self.assertTrue(found, "Company found on the list")


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

    def test_create_place(self):
        places_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Miejsca")]')))
        places_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Miejsca")) and (contains(@class, "breadcrumb"))]')))
        create_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[contains(text(), "Dodaj")]')))
        create_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Dodawanie miejsca")) and (contains(@class, "breadcrumb"))]')))
        form: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'form')))
        building_name = form.find_element_by_name('building_name')
        building_name.send_keys('PRZ')
        room_name = form.find_element_by_name('room_name')
        room_name.send_keys('A61')
        submit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(), "Zatwierdź")]')))
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Miejsca")) and (contains(@class, "breadcrumb"))]')))
        place = models.Place.objects.get(building_name='PRZ')
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

    def test_edit_place(self):
        place = models.Place.objects.create(building_name='PRZ', room_name='A61')
        places_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Miejsca")]')))
        places_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Miejsca")) and (contains(@class, "breadcrumb"))]')))
        edit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//i[contains(text(), "edit")]')))
        edit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Edytowanie miejsca")) and (contains(@class, "breadcrumb"))]')))
        form: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'form')))
        building_name = form.find_element_by_name('building_name')
        building_name.send_keys('EDIT')
        room_name = form.find_element_by_name('room_name')
        room_name.send_keys('EDIT')
        submit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(), "Zatwierdź")]')))
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Miejsca")) and (contains(@class, "breadcrumb"))]')))
        place2 = models.Place.objects.get(pk=place.pk)
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = False
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if columns[0].text == place2.building_name:
                self.assertEqual(columns[1].text, place2.room_name)
                found = True
        self.assertTrue(found, "Could not find place on the list")

    def test_delete_place(self):
        place = models.Place.objects.create(building_name='PRZ', room_name='A61')
        places_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Miejsca")]')))
        places_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Miejsca")) and (contains(@class, "breadcrumb"))]')))
        delete_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//i[contains(text(), "remove_circle")]')))
        delete_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Usuwanie miejsca")) and (contains(@class, "breadcrumb"))]')))
        submit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(), "Potwierdzam")]')))
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Miejsca")) and (contains(@class, "breadcrumb"))]')))
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = True
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if int(columns[0].text) == place.building_name:
                found = False
        self.assertTrue(found, "Place found on the list")


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

    def test_create_status(self):
        statuses_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Statusy")]')))
        statuses_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Statusy")) and (contains(@class, "breadcrumb"))]')))
        create_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[contains(text(), "Dodaj")]')))
        create_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Dodawanie statusu")) and (contains(@class, "breadcrumb"))]')))
        form: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'form')))
        name = form.find_element_by_name('name')
        name.send_keys('ZAKONCZONE')
        submit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(), "Zatwierdź")]')))
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Statusy")) and (contains(@class, "breadcrumb"))]')))
        status = models.PartnerStatus.objects.get(name='ZAKONCZONE')
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

    def test_edit_status(self):
        status = models.PartnerStatus.objects.create(name='ZAKONCZONE')
        statuses_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Statusy")]')))
        statuses_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Statusy")) and (contains(@class, "breadcrumb"))]')))
        edit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//i[contains(text(), "edit")]')))
        edit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Edytowanie statusu")) and (contains(@class, "breadcrumb"))]')))
        form: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'form')))
        name = form.find_element_by_name('name')
        name.send_keys('EDIT')
        submit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(), "Zatwierdź")]')))
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Statusy")) and (contains(@class, "breadcrumb"))]')))
        status2 = models.PartnerStatus.objects.get(pk=status.pk)
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = False
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if columns[0].text == status2.name:
                found = True
        self.assertTrue(found, "Could not find status on the list")

    def test_delete_status(self):
        status = models.PartnerStatus.objects.create(name='ZAKONCZONE')
        statuses_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Statusy")]')))
        statuses_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Statusy")) and (contains(@class, "breadcrumb"))]')))
        delete_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//i[contains(text(), "remove_circle")]')))
        delete_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Usuwanie statusu")) and (contains(@class, "breadcrumb"))]')))
        submit_button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(), "Potwierdzam")]')))
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[(contains(text(), "Statusy")) and (contains(@class, "breadcrumb"))]')))
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table')))
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        found = True
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            if int(columns[0].text) == status.name:
                found = False
        self.assertTrue(found, "Status found on the list")


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
        news = models.News.objects.create(content='NEWS', title='title', publish_date=t)
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
                self.assertEqual(columns[2].text, news.publish_date.strftime('%b. %d, %Y, %I:%M p.m.'))
                found = True
        self.assertTrue(found, "Could not find news on the list")
