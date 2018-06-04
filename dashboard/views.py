from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from INT.models import *


class DashboardView(TemplateView):
    template_name = 'dashboard.html'


class SpeakersView(ListView):
    model = Speaker
    template_name = 'speaker/list.html'


class SpeakerDetailView(DetailView):
    model = Speaker
    template_name = 'speaker/detail.html'
    context_object_name = 'speaker'


class SpeakerCreateView(CreateView):
    model = Speaker
    template_name = 'speaker/create.html'
    fields = ['name', 'surname', 'company', 'description']
    success_url = '/speakers'


class SpeakerDeleteView(DeleteView):
    model = Speaker
    template_name = 'speaker/delete.html'
    success_url = '/speakers'


class SpeakerUpdateView(UpdateView):
    model = Speaker
    fields = ['name', 'surname', 'company', 'description']
    template_name = 'speaker/create.html'
    success_url = '/speakers'


class PlacesView(ListView):
    model = Place
    template_name = 'place/list.html'


class PlaceDetailView(DetailView):
    model = Place
    template_name = 'place/detail.html'
    context_object_name = 'place'


class PlaceCreateView(CreateView):
    model = Place
    template_name = 'place/create.html'
    fields = ['building_name', 'room_name']
    success_url = '/places'


class PlaceDeleteView(DeleteView):
    model = Place
    template_name = 'place/delete.html'
    success_url = '/places'


class PlaceUpdateView(UpdateView):
    model = Place
    template_name = 'place/create.html'
    fields = ['building_name', 'room_name']
    success_url = '/places'


class LecturesView(ListView):
    model = Lecture
    template_name = 'lecture/list.html'


class LectureDetailView(DetailView):
    model = Lecture
    template_name = 'lecture/detail.html'
    context_object_name = 'lecture'


class LectureCreateView(CreateView):
    model = Lecture
    template_name = 'lecture/create.html'
    fields = ['title', 'speaker', 'begin_time', 'end_time', 'place',
              'description']
    success_url = '/lecture'


class LectureDeleteView(DeleteView):
    model = Lecture
    template_name = 'lecture/delete.html'
    success_url = '/lecture'


class LectureUpdateView(UpdateView):
    model = Lecture
    template_name = 'lecture/create.html'
    fields = ['title', 'speaker', 'begin_time', 'end_time', 'place',
              'description']
    success_url = '/lecture'


class NewsView(ListView):
    model = News
    template_name = 'news/list.html'


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'


class NewsCreateView(CreateView):
    model = News
    template_name = 'news/create.html'
    fields = ['title', 'content', 'creation_date', 'publish_date']
    success_url = '/news'


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'news/delete.html'
    success_url = '/news'


class NewsUpdateView(UpdateView):
    model = News
    template_name = 'news/create.html'
    fields = ['title', 'content', 'creation_date', 'publish_date']
    success_url = '/news'


class CompanyView(ListView):
    model = Company
    template_name = 'company/list.html'


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company/detail.html'
    context_object_name = 'Company'


class CompanyCreateView(CreateView):
    model = Company
    template_name = 'company/create.html'
    fields = ['title', 'content', 'creation_date', 'publish_date']
    success_url = '/company'


class CompanyDeleteView(DeleteView):
    model = Company
    template_name = 'company/delete.html'
    success_url = '/company'


class CompanyUpdateView(UpdateView):
    model = Company
    template_name = 'company/create.html'
    fields = ['title', 'content', 'creation_date', 'publish_date']
    success_url = '/company'
