from INT.models import News, Speaker, Lecture, SpeakerLecture, Picture, Company
from django import forms
from martor.fields import MartorFormField
from django.contrib.admin.widgets import AdminDateWidget


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
    picture_id = forms.ModelChoiceField(Picture.objects.all(), widget=PictureSelect())
    publish_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        model = News
        fields = ('title', 'picture_id', 'content', 'publish_date')


class LectureForm(forms.ModelForm):
    speakers = forms.ModelMultipleChoiceField(queryset=Speaker.objects.all(), required=False)

    class Meta:
        model = Lecture
        fields = ('begin_time', 'end_time', 'description', 'title', 'place_id')

    def __init__(self, *args, **kwargs):
        super(LectureForm, self).__init__(*args, **kwargs)
        if kwargs['instance'] is not None:
            sl = SpeakerLecture.objects.filter(lecture_id = kwargs['instance'])
            self.fields["speakers"].initial = [s.speaker_id.pk for s in sl]
            print(self.fields["speakers"].initial)


class SpeakerForm(forms.ModelForm):
    picture_id = forms.ModelChoiceField(Picture.objects.all(), widget=PictureSelect())

    class Meta:
        model = Speaker
        fields = ('name', 'surname', 'description', 'picture_id', 'company_id')


class CompanyForm(forms.ModelForm):
    picture_id = forms.ModelChoiceField(Picture.objects.all(), widget=PictureSelect())

    class Meta:
        model = Company
        fields = ('name', 'description', 'picture_id', 'status_id')