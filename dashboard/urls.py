from django.conf.urls import url
from .views import DashboardView

urlpatterns = [
    url('^$', DashboardView.as_view())
]