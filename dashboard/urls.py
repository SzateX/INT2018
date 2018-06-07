from django.conf.urls import url
from .views import DashboardView, SpeakersView, SpeakerDetailView, \
    SpeakerCreateView, SpeakerUpdateView, SpeakerDeleteView, LecturesView, \
    LectureCreateView, LectureDetailView, LectureUpdateView, LectureDeleteView, \
    CompanyView, CompanyCreateView, CompanyDetailView, CompanyUpdateView, \
    CompanyDeleteView

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^speakers/$', SpeakersView.as_view(), name='speaker_list'),
    url(r'^speakers/(?P<pk>\d+)$', SpeakerDetailView.as_view(), name='speaker_detail'),
    url(r'^speakers/create$', SpeakerCreateView.as_view(), name='speaker_create'),
    url(r'^speakers/(?P<pk>\d+)/edit$', SpeakerUpdateView.as_view(), name='speaker_edit'),
    url(r'^speakers/(?P<pk>\d+)/delete$', SpeakerDeleteView.as_view(), name='speaker_delete'),
    url(r'^lectures/$', LecturesView.as_view(), name='lecture_list'),
    url(r'^lectures/create$', LectureCreateView.as_view(), name='lecture_create'),
    url(r'^lectures/(?P<pk>\d+)$', LectureDetailView.as_view(), name='lecture_detail'),
    url(r'^lectures/(?P<pk>\d+)/edit$', LectureUpdateView.as_view(), name='lecture_edit'),
    url(r'^lectures/(?P<pk>\d+)/delete$', LectureDeleteView.as_view(), name='lecture_delete'),
    url(r'^companies/$', CompanyView.as_view(), name='company_list'),
    url(r'^companies/create$', CompanyCreateView.as_view(), name='company_create'),
    url(r'^companies/(?P<pk>\d+)$', CompanyDetailView.as_view(), name='company_detail'),
    url(r'^companies/(?P<pk>\d+)/edit$', CompanyUpdateView.as_view(), name='company_edit'),
    url(r'^companies/(?P<pk>\d+)/delete$', CompanyDeleteView.as_view(), name='company_delete')

]
