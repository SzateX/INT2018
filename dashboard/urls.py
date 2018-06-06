from django.conf.urls import url
from .views import DashboardView, SpeakersView, SpeakerDetailView, \
    SpeakerCreateView, SpeakerUpdateView, SpeakerDeleteView, LecturesView, \
    LectureCreateView, LectureDetailView, LectureUpdateView, LectureDeleteView

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

]
