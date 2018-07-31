from rest_framework import viewsets
from INT.models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import django_filters



class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PartnerStatusViewSet(viewsets.ModelViewSet):
    queryset = PartnerStatus.objects.all()
    serializer_class = PartnerStatusSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class SpeakerViewSet(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class ChangeFilter(django_filters.FilterSet):
    last = django_filters.NumberFilter(name="id", lookup_type='gte')

    class Meta:
        model = Change
        fields = ('id', 'type_of_change', 'model', 'content')


class ChangeFilterSet(django_filters.FilterSet):
    class Meta:
        model = Change
        fields = {
            'id': ['exact', 'gt']
        }


class ChangeViewSet(viewsets.ModelViewSet):
    queryset = Change.objects.all()
    serializer_class = ChangeSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = ChangeFilterSet
    #filter_fields = ('id',)
