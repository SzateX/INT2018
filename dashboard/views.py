from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from INT.models import *


class DashboardView(TemplateView):
    template_name = 'dashboard.html'


class SpeakersView(ListView):
    model = Speaker
    template_name = 'speakers/list.html'
    context_object_name = 'speakers'


class SpeakerDetailView(DetailView):
    model = Speaker
    template_name = 'speakers/detail.html'
    context_object_name = 'speaker'


class SpeakerCreateView(CreateView):
    model = Speaker
    template_name = 'speakers/create.html'
    fields = ['name', 'surname', 'company_id', 'picture_id', 'description']
    success_url = '/dashboard/speakers'

    def get_context_data(self, **kwargs):
        context = super(SpeakerCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context


class SpeakerDeleteView(DeleteView):
    model = Speaker
    template_name = 'speakers/delete.html'
    success_url = '/dashboard/speakers'
    context_object_name = 'speaker'


class SpeakerUpdateView(UpdateView):
    model = Speaker
    fields = ['name', 'surname', 'company_id', 'picture_id', 'description']
    template_name = 'speakers/create.html'
    success_url = '/dashboard/speakers'

    def get_context_data(self, **kwargs):
        context = super(SpeakerUpdateView, self).get_context_data(**kwargs)
        context['isEdited'] = True
        return context


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
    template_name = 'lectures/list.html'
    context_object_name = 'lectures'


class LectureDetailView(DetailView):
    model = Lecture
    template_name = 'lectures/detail.html'
    context_object_name = 'lecture'


class LectureCreateView(CreateView):
    model = Lecture
    template_name = 'lectures/create.html'
    fields = ['title', 'begin_time', 'end_time', 'place_id',
              'description']
    success_url = '/dashboard/lecture'

    def get_context_data(self, **kwargs):
        context = super(LectureCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context


class LectureDeleteView(DeleteView):
    model = Lecture
    template_name = 'lectures/delete.html'
    success_url = '/dashboard/lecture'


class LectureUpdateView(UpdateView):
    model = Lecture
    template_name = 'lectures/create.html'
    fields = ['title', 'begin_time', 'end_time', 'place_id',
              'description']
    success_url = '/dashboard/lecture'

    def get_context_data(self, **kwargs):
        context = super(LectureUpdateView, self).get_context_data(**kwargs)
        context['isEdited'] = True
        return context


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
