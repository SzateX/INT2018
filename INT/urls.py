from django.conf.urls import url
from .views import HomepageView, NewsListView, NewsDetailView, SpeakerDetailView, CompanyDetailView, KodziarzeView

urlpatterns = [
    url(r"^$", HomepageView.as_view(), name="Homepage"),
    url(r"^news$", NewsListView.as_view(), name="NewsList"),
    url(r"^news/(?P<pk>\d+)$", NewsDetailView.as_view(), name="NewsDetail"),
    url(r"^speakers/(?P<pk>\d+)$", SpeakerDetailView.as_view(), name="SpeakerDetail"),
    url(r"^company/(?P<pk>\d+)$", CompanyDetailView.as_view(), name="CompanyDetail"),
    url(r"^kodziarze$", KodziarzeView.as_view(), name="Kodziarze")
]
