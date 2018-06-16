from INT.models import News, Speaker, Lecture, SpeakerLecture
from django import forms
from martor.fields import MartorFormField
from django.contrib.admin.widgets import AdminDateWidget


class NewsForms(forms.ModelForm):
    content = MartorFormField()
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