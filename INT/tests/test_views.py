from unittest import mock
from django.core.files import File
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from INT.views import NewsDetailView, NewsListView, CompanyDetailView, SpeakerDetailView, HomepageView, KodziarzeView
from INT.models import Place, Lecture, Picture, PartnerStatus, Company, Speaker, SpeakerLecture, News


class NewsListViewTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            content = "Content %d" % i
            title = "Title %d" % i
            News.objects.create(content=content, title=title)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/news')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('FrontNewsList'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'INT/news/list.html')

    def test_returns_correct_data(self):
        resp = self.client.get(reverse('FrontNewsList'))
        obj_list = News.objects.all().order_by('creation_date')
        self.assertQuerysetEqual(resp.context['news_list'].order_by('creation_date'),
                                 map(repr, obj_list))


class NewsDetailViewTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        News.objects.create(content="content", title="title")

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/news/1')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('FrontNewsDetail', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'INT/news/detail.html')

    def test_returns_correct_data(self):
        resp = self.client.get(reverse('FrontNewsDetail', args=[1]))
        obj = News.objects.get(pk=1)
        self.assertEqual(resp.context['news'], obj)


class CompanyDetailViewTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Company.objects.create(name="name")

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/company/1')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('FrontCompanyDetail', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'INT/company/detail.html')

    def test_returns_correct_data(self):
        resp = self.client.get(reverse('FrontCompanyDetail', args=[1]))
        obj = Company.objects.get(pk=1)
        self.assertEqual(resp.context['company'], obj)


class SpeakerDetailViewTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        s = Speaker.objects.create(name="name", surname="surname")
        p = Place.objects.create(building_name="V", room_name="1")
        l = Lecture.objects.create(begin_time=timezone.now(), end_time=timezone.now(), title="title", place_id=p)
        SpeakerLecture.objects.create(speaker_id=s, lecture_id=l)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/speakers/1')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('FrontSpeakerDetail', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'INT/speakers/detail.html')

    def test_returns_correct_data(self):
        resp = self.client.get(reverse('FrontSpeakerDetail', args=[1]))
        obj = Speaker.objects.get(pk=1)
        ls = SpeakerLecture.objects.filter(speaker_id=obj)
        self.assertEqual(resp.context['speaker'], obj)
        self.assertQuerysetEqual(resp.context['lectures'], map(repr, ls.order_by('lecture_id')))


class HomepageViewTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            title = "Title %d" % i
            p = Place.objects.create(building_name="building %d" % i, room_name="%d" % i)
            Lecture.objects.create(begin_time=timezone.now(), end_time=timezone.now(), title=title, place_id=p)
            name = "Name %d" % i
            Company.objects.create(name=name)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('FrontHomepage'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'INT/index.html')

    def test_returns_correct_data(self):
        resp = self.client.get(reverse('FrontHomepage'))
        lecture_list = Lecture.objects.all().order_by('begin_time')
        partner_list = Company.objects.all().order_by('name')
        self.assertQuerysetEqual(resp.context['lectures'].order_by('begin_time'),
                                 map(repr, lecture_list))
        self.assertQuerysetEqual(
            resp.context['partners'].order_by('name'),
            map(repr, partner_list))


class KodziarzeViewTestClass(TestCase):
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/kodziarze')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('FrontKodziarze'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'INT/kodziarze_detail.html')