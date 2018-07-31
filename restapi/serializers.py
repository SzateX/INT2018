from rest_framework import serializers
from INT.models import *


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'building_name', 'room_name')


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('id', 'source')


class PartnerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerStatus
        fields = ('id', 'name')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'status_id', 'picture_id')


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ('id', 'name', 'surname', 'description', 'picture_id', 'company_id')


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('id', 'begin_time', 'end_time', 'description', 'title', 'place_id', 'speakers')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'content', 'title', 'creation_date', 'publish_date', 'picture_id')


class ChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Change
        fields = ('id', 'type_of_change', 'model', 'content')