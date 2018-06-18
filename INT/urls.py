from django.conf.urls import url
#from INT.views import HomepageView, NewsListView, NewsDetailView, SpeakerDetailView, CompanyDetailView, KodziarzeView
import INT.views as v

urlpatterns = [
    url(r"^$", v.HomepageView.as_view(), name="FrontHomepage"),
    url(r"^news$", v.NewsListView.as_view(), name="FrontNewsList"),
    url(r"^news/(?P<pk>\d+)$", v.NewsDetailView.as_view(), name="FrontNewsDetail"),
    url(r"^speakers/(?P<pk>\d+)$", v.SpeakerDetailView.as_view(), name="FrontSpeakerDetail"),
    url(r"^company/(?P<pk>\d+)$", v.CompanyDetailView.as_view(), name="FrontCompanyDetail"),
    url(r"^kodziarze$", v.KodziarzeView.as_view(), name="FrontKodziarze")
]
