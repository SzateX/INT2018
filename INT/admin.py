from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Place, Lecture, PartnerStatus, Picture, Company, Speaker])
#admin.site.regisre(SpeakerLecture)

from martor.widgets import AdminMartorWidget


class YourModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


admin.site.register(News, YourModelAdmin)
