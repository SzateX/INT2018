"""from django import template
from INT.models import Speaker, SpeakerLecture
register = template.Library()


def get_related_speakers(obj):
    sl = SpeakerLecture.objects.filter(lecture_id=obj)
    return sl


register.filter(get_related_speakers)"""
