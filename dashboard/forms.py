from INT.models import News
from django import forms
from martor.fields import MartorFormField
from django.contrib.admin.widgets import AdminDateWidget


class NewsForms(forms.ModelForm):
    content = MartorFormField()
    publish_date = forms.DateField(widget=AdminDateWidget())

    class Meta:
        model = News
        fields = ('title', 'picture_id')


