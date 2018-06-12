from INT.models import News
from django import forms
from martor.fields import MartorFormField


class NewsForms(forms.ModelForm):
    content = MartorFormField()

    class Meta:
        model = News
        fields = ('title', 'publish_date', 'picture_id')


