from django.views.generic import *
from INT.models import *
from django.contrib.auth.mixins import LoginRequiredMixin


class View(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


class SpeakersView(LoginRequiredMixin, ListView):
    model = Speaker
    template_name = 'speaker/list.html'


class SpeakerDetailView(LoginRequiredMixin, DetailView):
    model = Speaker
    template_name = 'speaker/detail.html'
    context_object_name = 'speaker'


class SpeakerCreateView(LoginRequiredMixin, CreateView):
    model = Speaker
    template_name = 'speaker/create.html'
    fields = ['name', 'surname', 'company', 'description']
    success_url = '/speakers'


class SpeakerDeleteView(LoginRequiredMixin, DeleteView):
    model = Speaker
    template_name = 'speaker/delete.html'
    success_url = '/speakers'


class SpeakerUpdateView(LoginRequiredMixin, UpdateView):
    model = Speaker
    fields = ['name', 'surname', 'company', 'description']
    template_name = 'speaker/create.html'
    success_url = '/speakers'


class PlacesView(LoginRequiredMixin, ListView):
    model = Place
    template_name = 'place/list.html'


class PlaceDetailView(LoginRequiredMixin, DetailView):
    model = Place
    template_name = 'place/detail.html'
    context_object_name = 'place'


class PlaceCreateView(LoginRequiredMixin, CreateView):
    model = Place
    template_name = 'place/create.html'
    fields = ['building_name', 'room_name']
    success_url = '/places'


class PlaceDeleteView(LoginRequiredMixin, DeleteView):
    model = Place
    template_name = 'place/delete.html'
    success_url = '/places'


class PlaceUpdateView(LoginRequiredMixin, UpdateView):
    model = Place
    template_name = 'place/create.html'
    fields = ['building_name', 'room_name']
    success_url = '/places'


class LecturesView(LoginRequiredMixin, ListView):
    model = Lecture
    template_name = 'lecture/list.html'


class LectureDetailView(LoginRequiredMixin, DetailView):
    model = Lecture
    template_name = 'lecture/detail.html'
    context_object_name = 'lecture'


class LectureCreateView(LoginRequiredMixin, CreateView):
    model = Lecture
    template_name = 'lecture/create.html'
    fields = ['title', 'speaker', 'begin_time', 'end_time', 'place',
              'description']
    success_url = '/lecture'


class LectureDeleteView(LoginRequiredMixin, DeleteView):
    model = Lecture
    template_name = 'lecture/delete.html'
    success_url = '/lecture'


class LectureUpdateView(LoginRequiredMixin, UpdateView):
    model = Lecture
    template_name = 'lecture/create.html'
    fields = ['title', 'speaker', 'begin_time', 'end_time', 'place',
              'description']
    success_url = '/lecture'


class NewsView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'news/list.html'


class NewsDetailView(LoginRequiredMixin, DetailView):
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'


class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'news/create.html'
    fields = ['title', 'content', 'creation_date', 'publish_date']
    success_url = '/news'


class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'news/delete.html'
    success_url = '/news'


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    template_name = 'news/create.html'
    fields = ['title', 'content', 'creation_date', 'publish_date']
    success_url = '/news'


class CompanyView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'company/list.html'


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'company/detail.html'
    context_object_name = 'Company'


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    template_name = 'company/create.html'
    fields = ['title', 'content', 'creation_date', 'publish_date']
    success_url = '/company'


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'company/delete.html'
    success_url = '/company'


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = 'company/create.html'
    fields = ['title', 'content', 'creation_date', 'publish_date']
    success_url = '/company'
