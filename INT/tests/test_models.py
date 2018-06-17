from unittest import mock
from django.core.files import File
from django.test import TestCase
from django.utils import timezone
from INT.models import Place, Lecture, Picture, PartnerStatus, Company, Speaker, SpeakerLecture, News


class PlaceTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Place.objects.create(building_name="Budynek V", room_name="V1")

    def test_building_name_max_length(self):
        place = Place.objects.get(id=1)
        max_length = place._meta.get_field('building_name').max_length
        self.assertEquals(max_length, 100)

    def test_room_name_max_length(self):
        place = Place.objects.get(id=1)
        max_length = place._meta.get_field('room_name').max_length
        self.assertEquals(max_length, 50)

    def test_room_name_nullable(self):
        place = Place.objects.get(id=1)
        self.assertTrue(place._meta.get_field('room_name').null)

    def test_room_name_blank(self):
        place = Place.objects.get(id=1)
        self.assertTrue(place._meta.get_field('room_name').blank)


class LectureTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        place = Place.objects.create(building_name="Budynek V", room_name="V1")
        Lecture.objects.create(begin_time=timezone.now(), end_time=timezone.now(), description="aaa", title="aaa", place_id=place)

    def test_description_nullable(self):
        lecture = Lecture.objects.get(id=1)
        self.assertTrue(lecture._meta.get_field('description').null)

    def test_description_blank(self):
        lecture = Lecture.objects.get(id=1)
        self.assertTrue(lecture._meta.get_field('description').blank)

    def test_title_max_length(self):
        lecture = Lecture.objects.get(id=1)
        max_length = lecture._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)


class PictureTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        #file_mock = mock.MagicMock(spec=File, name='FileMock')
        Picture.objects.create()

    def test_source_nullable(self):
        picture = Picture.objects.get(id=1)
        self.assertTrue(picture._meta.get_field('source').null)

    def test_source_blank(self):
        picture = Picture.objects.get(id=1)
        self.assertTrue(picture._meta.get_field('source').blank)


class PartnerStatusTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        PartnerStatus.objects.create(name="srebrny")

    def test_name_max_length(self):
        status = PartnerStatus.objects.get(id=1)
        max_length = status._meta.get_field('name').max_length
        self.assertEquals(max_length, 64)


class CompanyTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Company.objects.create(name="firma")

    def test_name_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('name').max_length
        self.assertEquals(max_length, 256)

    def test_description_nullable(self):
        company = Company.objects.get(id=1)
        self.assertTrue(company._meta.get_field('description').null)

    def test_status_nullable(self):
        company = Company.objects.get(id=1)
        self.assertTrue(company._meta.get_field('status_id').null)

    def test_status_blank(self):
        company = Company.objects.get(id=1)
        self.assertTrue(company._meta.get_field('status_id').blank)

    def test_picture_nullable(self):
        company = Company.objects.get(id=1)
        self.assertTrue(company._meta.get_field('picture_id').null)

    def test_picture_blank(self):
        company = Company.objects.get(id=1)
        self.assertTrue(company._meta.get_field('picture_id').blank)


class SpeakerTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Speaker.objects.create(name="Anna", surname="Kowalska")

    def test_name_max_length(self):
        speaker = Speaker.objects.get(id=1)
        max_length = speaker._meta.get_field('name').max_length
        self.assertEquals(max_length, 80)

    def test_surname_max_length(self):
        speaker = Speaker.objects.get(id=1)
        max_length = speaker._meta.get_field('surname').max_length
        self.assertEquals(max_length, 160)

    def test_description_nullable(self):
        speaker = Speaker.objects.get(id=1)
        self.assertTrue(speaker._meta.get_field('description').null)

    def test_description_blank(self):
        speaker = Speaker.objects.get(id=1)
        self.assertTrue(speaker._meta.get_field('description').blank)

    def test_company_nullable(self):
        speaker = Speaker.objects.get(id=1)
        self.assertTrue(speaker._meta.get_field('company_id').null)

    def test_company_blank(self):
        speaker = Speaker.objects.get(id=1)
        self.assertTrue(speaker._meta.get_field('company_id').blank)

    def test_picture_nullable(self):
        speaker = Speaker.objects.get(id=1)
        self.assertTrue(speaker._meta.get_field('picture_id').null)

    def test_picture_blank(self):
        speaker = Speaker.objects.get(id=1)
        self.assertTrue(speaker._meta.get_field('picture_id').blank)


class NewsTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        News.objects.create(content="aaa", title="aaa")

    def test_title_max_length(self):
        news = News.objects.get(id=1)
        max_length = news._meta.get_field('title').max_length
        self.assertEquals(max_length, 512)

    def test_publish_date_nullable(self):
        news = News.objects.get(id=1)
        self.assertTrue(news._meta.get_field('publish_date').null)

    def test_publish_date_blank(self):
        news = News.objects.get(id=1)
        self.assertTrue(news._meta.get_field('publish_date').blank)

    def test_picture_nullable(self):
        news = News.objects.get(id=1)
        self.assertTrue(news._meta.get_field('picture_id').null)

    def test_picture_blank(self):
        news = News.objects.get(id=1)
        self.assertTrue(news._meta.get_field('picture_id').blank)

