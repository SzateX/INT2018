from django.contrib import admin
from .models import  TypeOfNotification, CommunicationChannel
# Register your models here.
admin.site.register([CommunicationChannel, TypeOfNotification])
