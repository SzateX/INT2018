import urllib.parse

from django.test import TestCase
from django.test import RequestFactory
import factory.django
from django.contrib.auth.models import User
from django.urls import reverse

from dashboard.forms import SpeakerForm
from dashboard.views import DashboardView, Speaker


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
        for i in range(30):
            name = "Speaker %d" % i
            surname = "Surname %d" % i
            descripton = "Test descripton %d" % i
            Speaker.objects.create(name=name, surname=surname, description = descripton)

    def test_redirects_if_not_logged(self):
        resp = self.client.get(reverse('speaker_list'), follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(reverse('speaker_list'), ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('speaker_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/speakers/list.html')

    def test_is_return_correct_data(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('speaker_list'))
        obj_list = Speaker.objects.all().order_by('name')
        self.assertQuerysetEqual(resp.context['speakers'].order_by('name'), map(repr, obj_list))


class DashboardSpeakerDetailViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        Speaker.objects.create(name='Speaker', surname='Surname', description='Description', pk=1)

    def test_redirects_if_not_logged(self):
        resp = self.client.get(reverse('speaker_detail', args=[1]), follow=True)
        self.assertRedirects(resp, reverse('login') + "?next=" + urllib.parse.quote(reverse('speaker_detail', args=[1]), ""))

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('speaker_detail', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.user)
        self.assertTemplateUsed(resp, 'dashboard/speakers/detail.html')

    def test_returns_correct_data(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('speaker_detail', args=[1]))
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