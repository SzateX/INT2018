from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
import json
from rest_framework import status
from INT.models import Place, PartnerStatus, Company, Picture, Speaker, Lecture, News, Change
from restapi.serializers import PlaceSerializer, PartnerStatusSerializer, CompanySerializer, SpeakerSerializer, LectureSerializer, NewsSerializer, ChangeSerializer


class GetAllPlacesTest(TestCase):
    def setUp(self):
        Place.objects.create(building_name='PRZ A', room_name='A61')
        Place.objects.create(building_name='PRZ V', room_name='V17')

    def test_get_all_places(self):
        response = self.client.get('/restapi/place/')
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSinglePlaceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Place.objects.create(building_name='PRZ A', room_name='A61')
        Place.objects.create(building_name='PRZ V', room_name='V17')

    def test_get_valid_single_place(self):
        response = self.client.get('/restapi/place/'
                                   + str(Place.objects.get(building_name='PRZ A').pk)
                                   + '/')
        place = Place.objects.get(building_name='PRZ A')
        serializer = PlaceSerializer(place)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_place(self):
        response = self.client.get('/restapi/place/99/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAllPartnerStatusesTest(TestCase):
    def setUp(self):
        PartnerStatus.objects.create(name='test_status')
        PartnerStatus.objects.create(name='second_test_status')

    def test_get_all_partner_statuses(self):
        response = self.client.get('/restapi/partner-status/')
        statuses = PartnerStatus.objects.all()
        serializer = PartnerStatusSerializer(statuses, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSinglePartnerStatusTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PartnerStatus.objects.create(name='test_status')
        PartnerStatus.objects.create(name='second_test_status')

    def test_get_valid_single_partner_status(self):
        response = self.client.get('/restapi/partner-status/'
                                   + str(PartnerStatus.objects.get(name='test_status').pk)
                                   + '/')
        partner_status = PartnerStatus.objects.get(name='test_status')
        serializer = PartnerStatusSerializer(partner_status)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_partner_status(self):
        response = self.client.get('/restapi/partner-status/99/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAllCompaniesTest(TestCase):
    def setUp(self):
        partner_status = PartnerStatus.objects.create(name='test_status')
        picture = Picture.objects.create(source='pic')
        Company.objects.create(name='Firma pierwsza', description='test',
                               status_id=partner_status, picture_id=picture)
        Company.objects.create(name='Firma druga', description='test',
                               status_id=partner_status, picture_id=picture)

    def test_get_all_companies(self):
        response = self.client.get('/restapi/company/')
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleCompanyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        partner_status = PartnerStatus.objects.create(name='test_status')
        picture = Picture.objects.create(source='pic')
        Company.objects.create(name='Firma pierwsza', description='test',
                               status_id=partner_status, picture_id=picture)
        Company.objects.create(name='Firma druga', description='test',
                               status_id=partner_status, picture_id=picture)

    def test_get_valid_single_company(self):
        response = self.client.get('/restapi/company/'
                                   + str(Company.objects.get(name='Firma pierwsza').pk)
                                   + '/')
        company = Company.objects.get(name='Firma pierwsza')
        serializer = CompanySerializer(company)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_company(self):
        response = self.client.get('/restapi/company/99/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAllSpeakersTest(TestCase):
    def setUp(self):
        partner_status = PartnerStatus.objects.create(name='test_status')
        picture = Picture.objects.create(source='pic')
        company = Company.objects.create(name='Firma', description='opis',
                                         status_id=partner_status,
                                         picture_id=picture)
        Speaker.objects.create(name='Pierwszy', surname='Speaker',
                               description='opis', picture_id=picture,
                               company_id=company)
        Speaker.objects.create(name='Drugi', surname='Speaker',
                               description='opis', picture_id=picture,
                               company_id=company)

    def test_get_all_speakers(self):
        response = self.client.get('/restapi/speaker/')
        speakers = Speaker.objects.all()
        serializer = SpeakerSerializer(speakers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleSpeakerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        partner_status = PartnerStatus.objects.create(name='test_status')
        picture = Picture.objects.create(source='pic')
        company = Company.objects.create(name='Firma', description='opis',
                                         status_id=partner_status,
                                         picture_id=picture)
        Speaker.objects.create(name='Pierwszy', surname='Speaker',
                               description='opis', picture_id=picture,
                               company_id=company)
        Speaker.objects.create(name='Drugi', surname='Speaker',
                               description='opis', picture_id=picture,
                               company_id=company)

    def test_get_valid_single_speaker(self):
        response = self.client.get('/restapi/speaker/'
                                   + str(Speaker.objects.get(name='Pierwszy').pk)
                                   + '/')
        speaker = Speaker.objects.get(name='Pierwszy')
        serializer = SpeakerSerializer(speaker)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_speaker(self):
        response = self.client.get('/restapi/speaker/99/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAllLecturesTest(TestCase):
    def setUp(self):
        place = Place.objects.create(building_name='PRZ', room_name='A61')
        partner_status = PartnerStatus.objects.create(name='test_status')
        picture = Picture.objects.create(source='pic')
        company = Company.objects.create(name='Firma', description='opis',
                                         status_id=partner_status,
                                         picture_id=picture)
        s1 = Speaker.objects.create(name='Pierwszy', surname='Speaker',
                                    description='opis', picture_id=picture,
                                    company_id=company)
        s2 = Speaker.objects.create(name='Drugi', surname='Speaker',
                                    description='opis', picture_id=picture,
                                    company_id=company)
        l1 = Lecture.objects.create(begin_time=now(),
                                    end_time=now(),
                                    description='opis',
                                    title='title',
                                    place_id=place)
        l1.save()
        l2 = Lecture.objects.create(begin_time=now(),
                                    end_time=now(),
                                    description='opis',
                                    title='title2',
                                    place_id=place)
        l2.save()
        l1.speakers.add(s1, s2)
        l2.speakers.add(s2)

    def test_get_all_lectures(self):
        response = self.client.get('/restapi/lecture/')
        lectures = Lecture.objects.all()
        serializer = LectureSerializer(lectures, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleLectureTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        place = Place.objects.create(building_name='PRZ', room_name='A61')
        partner_status = PartnerStatus.objects.create(name='test_status')
        picture = Picture.objects.create(source='pic')
        company = Company.objects.create(name='Firma', description='opis',
                                         status_id=partner_status,
                                         picture_id=picture)
        s1 = Speaker.objects.create(name='Pierwszy', surname='Speaker',
                                    description='opis', picture_id=picture,
                                    company_id=company)
        s2 = Speaker.objects.create(name='Drugi', surname='Speaker',
                                    description='opis', picture_id=picture,
                                    company_id=company)
        l1 = Lecture.objects.create(begin_time=now(),
                                    end_time=now(),
                                    description='opis',
                                    title='title',
                                    place_id=place)
        l1.save()
        l2 = Lecture.objects.create(begin_time=now(),
                                    end_time=now(),
                                    description='opis',
                                    title='title2',
                                    place_id=place)
        l2.save()
        l1.speakers.add(s1, s2)
        l2.speakers.add(s2)

    def test_get_valid_single_lecture(self):
        response = self.client.get('/restapi/lecture/'
                                   + str(Lecture.objects.get(title='title').pk)
                                   + '/')
        lecture = Lecture.objects.get(title='title')
        serializer = LectureSerializer(lecture)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_lecture(self):
        response = self.client.get('/restapi/lecture/99/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAllNewsTest(TestCase):
    def setUp(self):
        picture = Picture.objects.create(source='pic')
        News.objects.create(content='tresc', title='title1',
                            picture_id=picture)
        News.objects.create(content='tresc', title='title2',
                            picture_id=picture)

    def test_get_all_news(self):
        response = self.client.get('/restapi/news/')
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleNewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        picture = Picture.objects.create(source='pic')
        News.objects.create(content='tresc', title='title1',
                            picture_id=picture)
        News.objects.create(content='tresc', title='title2',
                            picture_id=picture)

    def test_get_valid_single_news(self):
        response = self.client.get('/restapi/news/'
                                   + str(News.objects.get(title='title1').pk)
                                   + '/')
        news = News.objects.get(title='title1')
        serializer = NewsSerializer(news)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_news(self):
        response = self.client.get('/restapi/news/99/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAllChangesTest(TestCase):
    def setUp(self):
        Change.objects.create(model='News', type_of_change='CREATE', content='xyz')
        Change.objects.create(model='Place', type_of_change='READ', content='xyz')
        Change.objects.create(model='Lecture', type_of_change='UPDATE', content='xyz')
        Change.objects.create(model='Speaker', type_of_change='DELETE', content='xyz')

    def test_get_all_changes(self):
        response = self.client.get('/restapi/change/')
        changes = Change.objects.all()
        serializer = ChangeSerializer(changes, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleChangeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Change.objects.create(model='News', type_of_change='CREATE', content='xyz')
        Change.objects.create(model='Place', type_of_change='READ', content='xyz')
        Change.objects.create(model='Lecture', type_of_change='UPDATE', content='xyz')
        Change.objects.create(model='Speaker', type_of_change='DELETE', content='xyz')

    def test_get_valid_single_change(self):
        response = self.client.get('/restapi/change/'
                                   + str(Change.objects.get(model='News').pk)
                                   + '/')
        change = Change.objects.get(model='News')
        serializer = ChangeSerializer(change)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_change(self):
        response = self.client.get('/restapi/change/99/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)