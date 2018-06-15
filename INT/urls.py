from django.conf.urls import url
from .views import HomepageView, NewsListView, NewsDetailView

urlpatterns = [
    url(r"^$", HomepageView.as_view(), name="Homepage"),
    url(r"^news$", NewsListView.as_view(), name="NewsList"),
    url(r"^news/(?P<pk>\d+)$", NewsDetailView.as_view(), name="NewsDetail")
]
