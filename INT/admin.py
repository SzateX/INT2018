from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Place, Lecture, PartnerStatus, Picture, Company, Speaker, News, SpeakerLecture])
