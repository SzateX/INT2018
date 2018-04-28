from django.db import models


class Place(models.Model):
    building_name = models.CharField(max_length=100)
    room_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return "%s %s %s" % (self.pk, self.building_name, self.room_name)


class Lecture(models.Model):
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.CharField(max_length=4000, null=True)
    title = models.CharField(max_length=200)
    place_id = models.ForeignKey('Place')

    def __str__(self):
        return "%s %s" % (self.pk, self.title)


class Picture(models.Model):
    source = models.ImageField(null=True) #TODO: check the field type, correct if needed

    def __str__(self):
        return "%s" % self.pk


class PartnerStatus(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return "%s %s" % (self.pk, self.name)


class Company(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=4000, null=True)
    status_id = models.ForeignKey('PartnerStatus', null=True)
    picture_id = models.ForeignKey('Picture', null=True)

    def __str__(self):
        return "%s %s" % (self.pk, self.name)


class Speaker(models.Model):
    name = models.CharField(max_length=80)
    surname = models.CharField(max_length=160)
    description = models.CharField(max_length=4000, null=True)
    picture_id = models.ForeignKey('Picture', null=True)
    company_id = models.ForeignKey('Company', null=True)

    def __str__(self):
        return "%s %s %s" % (self.pk, self.name, self.surname)


class SpeakerLecture(models.Model):
    speaker_id = models.ForeignKey('Speaker')
    lecture_id = models.ForeignKey('Lecture')

    def __str__(self):
        return "%s %s %s" % (self.pk, self.speaker_id, self.lecture_id)
