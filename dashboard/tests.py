import urllib.parse

import factory.django
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from INT.models import Place, PartnerStatus, News, Lecture, \
    Company
from dashboard.views import Speaker


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = 'test@test.com'
    username = 'testuser'
    passwords = factory.PostGenerationMethodCall('set_password', 'password')
    is_superuser = True
    is_staff = True
    is_active = True


# Create your tests here.
class DashboardHomeViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_redirects_if_not_logged(self):
        resp = self.client.get(reverse('dashboard'), follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(reverse('dashboard'), ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('dashboard'), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/dashboard.html')


class DashboardSpeakerListViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.reverse_url = reverse('speaker_list')
        for i in range(30):
            name = "Speaker %d" % i
            surname = "Surname %d" % i
            descripton = "Test descripton %d" % i
            Speaker.objects.create(name=name, surname=surname, description = descripton)

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/speakers/list.html')

    def test_is_return_correct_data(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        obj_list = Speaker.objects.all().order_by('name')
        self.assertQuerysetEqual(resp.context['speakers'].order_by('name'), map(repr, obj_list))


class DashboardSpeakerDetailViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.reverse_url = reverse('speaker_detail', args=[1])
        Speaker.objects.create(name='Speaker', surname='Surname', description='Description', pk=1)

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/speakers/detail.html')

    def test_returns_correct_data(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        obj = Speaker.objects.get(pk=1)
        self.assertEqual(resp.context['speaker'], obj)


class DashboardSpeakerCreateViewTest(TestCase):
    def setUp(self):
        self.instance_obj = Speaker(name='Speaker', surname='Surname', description='Description', pk=1)
        self.user = UserFactory()
        self.reverse_url = reverse('speaker_create')

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/speakers/create.html')

    def test_is_save_work(self):
        self.client.force_login(self.user)
        data_dict = {'name': self.instance_obj.name, 'surname': self.instance_obj.surname, 'description': self.instance_obj.description}
        resp = self.client.post(self.reverse_url, data_dict, follow=True)
        self.assertRedirects(resp, reverse('speaker_list'))
        obj = Speaker.objects.get(pk=1)
        self.assertEqual(self.instance_obj, obj)


class DashboardSpeakerEditViewTest(TestCase):
    def setUp(self):
        self.instance_obj = Speaker(name='Speaker', surname='Surname', description='Description', pk=1)
        Speaker.objects.create(name='Speaker', surname='Surname', description='Description', pk=1)
        self.instance_obj.name = 'Speaker2'
        self.user = UserFactory()
        self.reverse_url = reverse('speaker_edit', args=[1])

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/speakers/create.html')

    def test_is_save_work(self):
        self.client.force_login(self.user)
        data_dict = {'name': self.instance_obj.name, 'surname': self.instance_obj.surname, 'description': self.instance_obj.description}
        resp = self.client.post(self.reverse_url, data_dict, follow=True)
        self.assertRedirects(resp, reverse('speaker_list'))
        obj = Speaker.objects.get(pk=1)
        self.assertEqual(self.instance_obj, obj)


class DashboardPlacesListViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.reverse_url = reverse('place_list')
        for i in range(30):
            building = "b %d" % i
            room = "r %d" % i
            Place.objects.create(building_name=building, room_name=room)

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/places/list.html')

    def test_is_return_correct_data(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        obj_list = Place.objects.all().order_by('pk')
        self.assertQuerysetEqual(resp.context['places'].order_by('pk'), map(repr, obj_list))


class DashboardPlaceCreateViewTest(TestCase):
    def setUp(self):
        self.instance_obj = Place(building_name='a', room_name='3', pk=1)
        self.user = UserFactory()
        self.reverse_url = reverse('place_create')

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/places/create.html')

    def test_is_save_work(self):
        self.client.force_login(self.user)
        data_dict = {'building_name': self.instance_obj.building_name, 'room_name':self.instance_obj.room_name}
        resp = self.client.post(self.reverse_url, data_dict, follow=True)
        self.assertRedirects(resp, reverse('place_list'))
        obj = Place.objects.get(pk=1)
        self.assertEqual(self.instance_obj, obj)


class DashboardPlaceEditViewTest(TestCase):
    def setUp(self):
        self.instance_obj = Place(building_name='a', room_name='3', pk=1)
        Place.objects.create(building_name='a', room_name='3')
        self.instance_obj.building_name = 'b'
        self.user = UserFactory()
        self.reverse_url = reverse('place_edit', args=[1])

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/places/create.html')

    def test_is_save_work(self):
        self.client.force_login(self.user)
        data_dict = {'building_name': self.instance_obj.building_name,
                     'room_name': self.instance_obj.room_name}
        resp = self.client.post(self.reverse_url, data_dict, follow=True)
        self.assertRedirects(resp, reverse('place_list'))
        obj = Place.objects.get(pk=1)
        self.assertEqual(self.instance_obj, obj)


class DashboardStatusesListViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.reverse_url = reverse('partner_status_list')
        for i in range(30):
            name = "status %d" % i
            PartnerStatus.objects.create(name=name)

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/partner_statuses/list.html')

    def test_is_return_correct_data(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        obj_list = PartnerStatus.objects.all().order_by('pk')
        self.assertQuerysetEqual(resp.context['statuses'].order_by('pk'), map(repr, obj_list))


class DashboardStatusesCreateViewTest(TestCase):
    def setUp(self):
        self.instance_obj = PartnerStatus(pk=1, name='a')
        self.user = UserFactory()
        self.reverse_url = reverse('partner_status_create')

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/partner_statuses/create.html')

    def test_is_save_work(self):
        self.client.force_login(self.user)
        data_dict = {'name': self.instance_obj.name}
        resp = self.client.post(self.reverse_url, data_dict, follow=True)
        self.assertRedirects(resp, reverse('partner_status_list'))
        obj = PartnerStatus.objects.get(pk=1)
        self.assertEqual(self.instance_obj, obj)


class DashboardStatusesEditViewTest(TestCase):
    def setUp(self):
        self.instance_obj = PartnerStatus(pk=1, name='a')
        PartnerStatus.objects.create(pk=1, name='b')
        self.user = UserFactory()
        self.reverse_url = reverse('partner_status_edit', args=[1])

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/partner_statuses/create.html')

    def test_is_save_work(self):
        self.client.force_login(self.user)
        data_dict = {'name': self.instance_obj.name}
        resp = self.client.post(self.reverse_url, data_dict, follow=True)
        self.assertRedirects(resp, reverse('partner_status_list'))
        obj = PartnerStatus.objects.get(pk=1)
        self.assertEqual(self.instance_obj, obj)


class DashboardNewsListViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.reverse_url = reverse('news_list')
        for i in range(30):
            content = "content %d" % i
            title = "title %d" % i
            News.objects.create(title=title, content=content)

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/news/list.html')

    def test_is_return_correct_data(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        obj_list = News.objects.all().order_by('pk')
        self.assertQuerysetEqual(resp.context['newses'].order_by('pk'), map(repr, obj_list))


class DashboardNewsDetailViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.reverse_url = reverse('news_detail', args=[1])
        News.objects.create(title='a', content='b')

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/news/detail.html')

    def test_returns_correct_data(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        obj = News.objects.get(pk=1)
        self.assertEqual(resp.context['news'], obj)


class DashboardNewsCreateViewTest(TestCase):
    def setUp(self):
        self.instance_obj = News(title='a', content='b', publish_date='2012-01-01', pk=1)
        self.user = UserFactory()
        self.reverse_url = reverse('news_create')

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/news/create.html')

    def test_is_save_work(self):
        self.client.force_login(self.user)
        data_dict = {'title': self.instance_obj.title, 'content': self.instance_obj.content, 'publish_date': self.instance_obj.publish_date}
        resp = self.client.post(self.reverse_url, data_dict, follow=True)
        self.assertRedirects(resp, reverse('news_list'))
        obj = News.objects.get(pk=1)
        self.assertEqual(self.instance_obj, obj)


class DashboardNewsEditViewTest(TestCase):
    def setUp(self):
        self.instance_obj = News(title='a', content='b', publish_date='2012-01-01', pk=1)
        News.objects.create(title='a', content='c')
        self.user = UserFactory()
        self.reverse_url = reverse('news_edit', args=[1])

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/news/create.html')

    def test_is_save_work(self):
        self.client.force_login(self.user)
        data_dict = {'title': self.instance_obj.title,
                     'content': self.instance_obj.content,
                     'publish_date': self.instance_obj.publish_date}
        resp = self.client.post(self.reverse_url, data_dict, follow=True)
        self.assertRedirects(resp, reverse('news_list'))
        obj = News.objects.get(pk=1)
        self.assertEqual(self.instance_obj, obj)


class DashboardLectureListViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.reverse_url = reverse('lecture_list')
        for i in range(30):
            title = "title %d" % i
            description = "description %d" % i
            begin_time = timezone.now()
            end_time = timezone.now()
            place = Place.objects.create(building_name='a %d' % i, room_name='b %d' % i)
            Lecture.objects.create(title=title, description=description, begin_time=begin_time, end_time=end_time, place_id=place)

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/lectures/list.html')

    def test_is_return_correct_data(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        obj_list = Lecture.objects.all().order_by('pk')
        self.assertQuerysetEqual(resp.context['lectures'].order_by('pk'), map(repr, obj_list))


class DashboardLectureDetailViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.reverse_url = reverse('lecture_detail', args=[1])
        Lecture.objects.create(title='a', description='b',
                               begin_time=timezone.now(), end_time=timezone.now(),
                               place_id=Place.objects.create(building_name='a', room_name='b'))

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/lectures/detail.html')

    def test_returns_correct_data(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        obj = Lecture.objects.get(pk=1)
        self.assertEqual(resp.context['lecture'], obj)


class DashboardLectureCreateViewTest(TestCase):
    def setUp(self):
        self.instance_obj = Lecture(pk=1, title='a', description='b',
                               begin_time=timezone.now(), end_time=timezone.now(),
                               place_id=Place.objects.create(building_name='a', room_name='b'))
        self.speaker_obj = Speaker.objects.create(name='Speaker', surname='Surname', description='Description', pk=1)
        self.user = UserFactory()
        self.reverse_url = reverse('lecture_create')

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/lectures/create.html')

    def test_is_save_work(self):
        self.client.force_login(self.user)
        data_dict = {'title': self.instance_obj.title,
                     'description': self.instance_obj.description,
                     'begin_time': self.instance_obj.begin_time.strftime("%Y-%m-%d %H:%M:%S"),
                     'end_time': self.instance_obj.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                     'place_id': self.instance_obj.place_id.pk,
                     'speakers': [self.speaker_obj.pk]}
        resp = self.client.post(self.reverse_url, data_dict, follow=True)

        self.assertRedirects(resp, reverse('lecture_list'))
        obj = Lecture.objects.get(pk=1)
        self.assertEqual(self.instance_obj, obj)


class DashboardLectureEditViewTest(TestCase):
    def setUp(self):
        self.instance_obj = Lecture(pk=1, title='a', description='b',
                                                   begin_time=timezone.now(),
                                                   end_time=timezone.now(),
                                                   place_id=Place.objects.create(
                                                       building_name='a',
                                                       room_name='b'))
        self.speaker_obj = Speaker.objects.create(name='Speaker',
                                                  surname='Surname',
                                                  description='Description',
                                                  pk=1)
        Lecture.objects.create(title='aaaaaa', description='b',
                                                   begin_time=timezone.now(),
                                                   end_time=timezone.now(),
                                                   place_id=self.instance_obj.place_id)
        self.user = UserFactory()
        self.reverse_url = reverse('lecture_edit', args=[1])

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/lectures/create.html')

    def test_is_save_work(self):
        self.client.force_login(self.user)
        data_dict = {'title': self.instance_obj.title,
                     'description': self.instance_obj.description,
                     'begin_time': self.instance_obj.begin_time.strftime(
                         "%Y-%m-%d %H:%M:%S"),
                     'end_time': self.instance_obj.end_time.strftime(
                         "%Y-%m-%d %H:%M:%S"),
                     'place_id': self.instance_obj.place_id.pk,
                     'speakers': [self.speaker_obj.pk]}
        resp = self.client.post(self.reverse_url, data_dict, follow=True)
        self.assertRedirects(resp, reverse('lecture_list'))
        obj = Lecture.objects.get(pk=1)
        self.assertEqual(self.instance_obj, obj)


class DashboardCompanyListViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.reverse_url = reverse('company_list')
        for i in range(30):
            name = "name %d" % i
            description = "description %d" % i
            Company.objects.create(name = name, description = description,
                                status_id = PartnerStatus.objects.create(name="status %d" % i))

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/companies/list.html')

    def test_is_return_correct_data(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        obj_list = Company.objects.all().order_by('pk')
        self.assertQuerysetEqual(resp.context['companies'].order_by('pk'), map(repr, obj_list))


class DashboardCompanyDetailViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.reverse_url = reverse('company_detail', args=[1])
        Company.objects.create(name="name", description="desc",
                               status_id=PartnerStatus.objects.create(
                                   name="status"))

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/companies/detail.html')

    def test_returns_correct_data(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        obj = Company.objects.get(pk=1)
        self.assertEqual(resp.context['company'], obj)


class DashboardCompanyCreateViewTest(TestCase):
    def setUp(self):
        self.instance_obj = Company(pk = 1, name="name", description="desc",
                               status_id=PartnerStatus.objects.create(
                                   name="status"))
        self.user = UserFactory()
        self.reverse_url = reverse('company_create')

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/companies/create.html')

    def test_is_save_work(self):
        self.client.force_login(self.user)
        data_dict = {'name': self.instance_obj.name,
                     'description': self.instance_obj.description,
                     'status_id': self.instance_obj.status_id.pk}
        resp = self.client.post(self.reverse_url, data_dict, follow=True)
        self.assertRedirects(resp, reverse('company_list'))
        obj = Company.objects.get(pk=1)
        self.assertEqual(self.instance_obj, obj)


class DashboardCompanyEditViewTest(TestCase):
    def setUp(self):
        self.instance_obj = self.instance_obj = Company(pk = 1, name="name", description="desc",
                               status_id=PartnerStatus.objects.create(
                                   name="status"))
        Company.objects.create(name="name", description="desc",
                               status_id=PartnerStatus.objects.create(
                                   name="status"))
        self.user = UserFactory()
        self.reverse_url = reverse('company_edit', args=[1])

    def test_redirects_if_not_logged(self):
        resp = self.client.get(self.reverse_url, follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(self.reverse_url, ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.reverse_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/companies/create.html')

    def test_is_save_work(self):
        self.client.force_login(self.user)
        data_dict = {'name': self.instance_obj.name,
                     'description': self.instance_obj.description,
                     'status_id': self.instance_obj.status_id.pk}
        resp = self.client.post(self.reverse_url, data_dict, follow=True)
        self.assertRedirects(resp, reverse('company_list'))
        obj = Company.objects.get(pk=1)
        self.assertEqual(self.instance_obj, obj)