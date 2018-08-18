from INT.models import News, Speaker, Lecture, Picture, Company
from .models import CommunicationChannel, TypeOfNotification
#from INT.models import SpeakerLecture
from django import forms
from martor.fields import MartorFormField
from django.contrib.admin.widgets import AdminDateWidget


class MySplitDateTimeWidget(forms.SplitDateTimeWidget):
    def __init__(self, attrs=None, date_format=None, time_format=None):
        date_class = attrs.pop('date_class')
        time_class = attrs.pop('time_class')

        widgets = (forms.DateInput(attrs={'class' : date_class}, format=date_format),
                   forms.TimeInput(attrs={'class' : time_class}, format=time_format))
        super(forms.SplitDateTimeWidget, self).__init__(widgets, attrs)


class PictureSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option_dict = super(PictureSelect, self).create_option(name, value, label, selected, index, subindex, attrs)
        print(option_dict['value'])
        if option_dict['value']:
            option_dict['attrs']['data-icon'] = Picture.objects.get(
                id=option_dict['value']).source.url
        return option_dict


class NewsForms(forms.ModelForm):
    content = MartorFormField()
    picture_id = forms.ModelChoiceField(Picture.objects.all(), widget=PictureSelect(), required=False)
    publish_date = forms.SplitDateTimeField(widget=MySplitDateTimeWidget(attrs={'date_class': 'datepicker', 'time_class': 'timepicker'}))

    class Meta:
        model = News
        fields = ('title', 'picture_id', 'content', 'publish_date')


class LectureForm(forms.ModelForm):
    begin_time = forms.SplitDateTimeField(widget=MySplitDateTimeWidget(attrs={'date_class': 'datepicker', 'time_class': 'timepicker'}))
    end_time = forms.SplitDateTimeField(widget=MySplitDateTimeWidget(attrs={'date_class': 'datepicker', 'time_class': 'timepicker'}))

    class Meta:
        model = Lecture
        fields = ('begin_time', 'end_time', 'description', 'title', 'place_id', 'speakers')


class SpeakerForm(forms.ModelForm):
    picture_id = forms.ModelChoiceField(Picture.objects.all(), widget=PictureSelect(), required=False)

    class Meta:
        model = Speaker
        fields = ('name', 'surname', 'description', 'picture_id', 'company_id')


class CompanyForm(forms.ModelForm):
    picture_id = forms.ModelChoiceField(Picture.objects.all(), widget=PictureSelect(), required=False)

    class Meta:
        model = Company
        fields = ('name', 'description', 'picture_id', 'status_id')


class NotifyForm(forms.Form):
    channel = forms.ModelChoiceField(CommunicationChannel.objects.all(), required=True)
    type_of_notification = forms.ModelChoiceField(TypeOfNotification.objects.all(), required=True)
    content = forms.CharField(widget=forms.Textarea(), required=True)