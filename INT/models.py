from django.db import models
from django.utils import timezone
from martor.models import MartorField


class Place(models.Model):
    building_name = models.CharField(max_length=100)
    room_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return "%s %s %s" % (self.pk, self.building_name, self.room_name)


class Picture(models.Model):
    source = models.ImageField(null=True, blank=True)

    """def __str__(self):
        return "%s" % self.pk"""

    def __str__(self):
        return '{}'.format(self.source)


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


class Lecture(models.Model):
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=200)
    place_id = models.ForeignKey('Place', on_delete=models.CASCADE)
    speakers = models.ManyToManyField(Speaker, related_name='lectures')

    def __str__(self):
        return "%s %s" % (self.pk, self.title)


class News(models.Model):
    content = MartorField()
    title = models.CharField(max_length=512)
    creation_date = models.DateTimeField(default=timezone.now)
    publish_date = models.DateTimeField(null=True, blank=True)
    picture_id = models.ForeignKey('Picture', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "News"

    def __str__(self):
        return "%s" % self.title


class Change(models.Model):
    model = models.CharField(max_length=256)
    type_of_change = models.CharField(max_length=20)
    content = models.TextField()

    def __str__(self):
        return "%s %s %s" % (self.model, self.type_of_change, self.content)