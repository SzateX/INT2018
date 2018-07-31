from django.conf.urls import url, include
from rest_framework import routers
from .viewsets import *

router = routers.DefaultRouter()
router.register(r'^place', PlaceViewSet, base_name='place')
router.register(r'^picture', PictureViewSet, base_name='picture')
router.register(r'^partner-status', PartnerStatusViewSet, base_name='partner-status')
router.register(r'^company', CompanyViewSet, base_name='company')
router.register(r'^speaker', SpeakerViewSet, base_name='speaker')
router.register(r'^lecture', LectureViewSet, base_name='lecture')
router.register(r'^news', NewsViewSet, base_name='news')
router.register(r'^change', ChangeViewSet, base_name='change')

urlpatterns = [
    url(r'^', include(router.urls)),
]
