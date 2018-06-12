from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from INT.models import *
from .forms import NewsForms


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


class LecturesView(ListView):
    model = Lecture
    template_name = 'lectures/list.html'
    context_object_name = 'lectures'


class LectureDetailView(DetailView):
    model = Lecture
    template_name = 'lectures/detail.html'
    context_object_name = 'lecture'
    # TODO: Create template for lecture details


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
    context_object_name = 'lecture'


class LectureUpdateView(UpdateView):
    model = Lecture
    template_name = 'lectures/create.html'
    fields = ['title', 'begin_time', 'end_time', 'place_id',
              'description']
    success_url = '/dashboard/lecture'
    context_object_name = 'lecture'

    def get_context_data(self, **kwargs):
        context = super(LectureUpdateView, self).get_context_data(**kwargs)
        context['isEdited'] = True
        return context


class CompanyView(ListView):
    model = Company
    template_name = 'companies/list.html'
    context_object_name = 'companies'


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/detail.html'
    context_object_name = 'company'
    # TODO: Create template for company details


class CompanyCreateView(CreateView):
    model = Company
    template_name = "companies/create.html"
    fields = ['name', 'description', 'status_id', 'picture_id']
    success_url = '/dashboard/companies'

    def get_context_data(self, **kwargs):
        context = super(CompanyCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context


class CompanyDeleteView(DeleteView):
    model = Company
    template_name = 'companies/delete.html'
    success_url = '/dashboard/companies'
    context_object_name = 'company'


class CompanyUpdateView(UpdateView):
    model = Company
    template_name = 'companies/create.html'
    fields = ['name', 'description', 'status_id', 'picture_id']
    success_url = '/dashboard/companies'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        context['isEdited'] = True
        return context


class PlacesView(ListView):
    model = Place
    template_name = 'places/list.html'
    context_object_name = 'places'


class PlaceDetailView(DetailView):
    model = Place
    template_name = 'places/detail.html'
    context_object_name = 'place'


class PlaceCreateView(CreateView):
    model = Place
    template_name = 'places/create.html'
    fields = ['building_name', 'room_name']
    success_url = '/places'

    def get_context_data(self, **kwargs):
        context = super(PlaceCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context


class PlaceDeleteView(DeleteView):
    model = Place
    template_name = 'places/delete.html'
    success_url = '/places'
    context_object_name = 'place'


class PlaceUpdateView(UpdateView):
    model = Place
    template_name = 'places/create.html'
    fields = ['building_name', 'room_name']
    success_url = '/places'
    context_object_name = 'place'

    def get_context_data(self, **kwargs):
        context = super(PlaceUpdateView, self).get_context_data(**kwargs)
        context['isEdited'] = True
        return context


class PartnerStatusesView(ListView):
    model = PartnerStatus
    template_name = 'partner_statuses/list.html'
    context_object_name = 'statuses'


class PartnerStatusDetailView(DetailView):
    model = PartnerStatus
    template_name = 'partner_statuses/detail.html'
    context_object_name = 'status'


class PartnerStatusCreateView(CreateView):
    model = PartnerStatus
    template_name = 'partner_statuses/create.html'
    fields = ['name']
    success_url = '/partner_statuses'

    def get_context_data(self, **kwargs):
        context = super(PartnerStatusCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context


class PartnerStatusDeleteView(DeleteView):
    model = PartnerStatus
    template_name = 'partner_statuses/delete.html'
    success_url = '/partner_statuses'
    context_object_name = 'status'


class PartnerStatusUpdateView(UpdateView):
    model = PartnerStatus
    template_name = 'partner_statuses/create.html'
    fields = ['name']
    success_url = '/partner_statuses'
    context_object_name = 'status'

    def get_context_data(self, **kwargs):
        context = super(PartnerStatusUpdateView, self).get_context_data(**kwargs)
        context['isEdited'] = True
        return context


class NewsesView(ListView):
    model = News
    template_name = 'news/list.html'
    context_object_name = 'newses'


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'


class NewsCreateView(CreateView):
    form_class = NewsForms
    template_name = 'news/create.html'
    success_url = '/news'

    def get_context_data(self, **kwargs):
        context = super(NewsCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'news/delete.html'
    success_url = '/news'


class NewsUpdateView(UpdateView):
    form_class = NewsForms
    template_name = 'news/create.html'
    success_url = '/news'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super(NewsUpdateView, self).get_context_data(**kwargs)
        context['isEdited'] = True
        return context


class PicturesView(ListView):
    model = Picture
    template_name = 'pictures/list.html'
    context_object_name = 'pictures'
    queryset = Picture.objects.all().reverse()


class PictureCreateView(CreateView):
    model = Picture
    template_name = 'pictures/create.html'
    fields = ['source']
    success_url = '/pictures'

    def get_context_data(self, **kwargs):
        context = super(PictureCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context


class PictureDeleteView(DeleteView):
    model = Picture
    template_name = 'pictures/delete.html'
    success_url = '/pictures'