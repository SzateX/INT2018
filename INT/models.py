from django.db import models
from django.utils import timezone
from martor.models import MartorField


class Place(models.Model):
    building_name = models.CharField(max_length=100)
    room_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return "%s %s %s" % (self.pk, self.building_name, self.room_name)


class Lecture(models.Model):
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=200)
    place_id = models.ForeignKey('Place', on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.pk, self.title)


class Picture(models.Model):
    source = models.ImageField(null=True, blank=True) #TODO: check the field type, correct if needed

    def __str__(self):
        return "%s" % self.pk


class PartnerStatus(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return "%s %s" % (self.pk, self.name)


class Company(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True)
    status_id = models.ForeignKey('PartnerStatus', null=True, blank=True, on_delete=models.CASCADE)
    picture_id = models.ForeignKey('Picture', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.pk, self.name)


class Speaker(models.Model):
    name = models.CharField(max_length=80)
    surname = models.CharField(max_length=160)
    description = models.TextField(null=True, blank=True)
    picture_id = models.ForeignKey('Picture', null=True, blank=True, on_delete=models.CASCADE)
    company_id = models.ForeignKey('Company', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s" % (self.pk, self.name, self.surname)


class SpeakerLecture(models.Model):
    speaker_id = models.ForeignKey('Speaker', on_delete=models.CASCADE)
    lecture_id = models.ForeignKey('Lecture', on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s" % (self.pk, self.speaker_id, self.lecture_id)


class News(models.Model):
    #content = models.TextField()
    content = MartorField()
    title = models.CharField(max_length=512)
    creation_date = models.DateField(default=timezone.now)
    publish_date = models.DateField(null=True, blank=True)
    picture_id = models.ForeignKey('Picture', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "News"

    def __str__(self):
        return "%s" % self.title
