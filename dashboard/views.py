from asgiref.sync import async_to_sync
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.views.generic import *
from INT.models import *
from .forms import NewsForms, LectureForm, SpeakerForm, CompanyForm, NotifyForm
from restapi.serializers import *
from channels.layers import get_channel_layer
import json
from rest_framework.renderers import JSONRenderer

LOGIN_URL = '/dashboard/login'


class DashboardLoginView(LoginView):
    template_name = 'dashboard/login.html'
    
    def get_redirect_url(self):
        redirect_url = super(DashboardLoginView, self).get_redirect_url()
        if redirect_url == '':
            return '/dashboard/'
        return redirect_url


class DashboardLogoutView(LogoutView):
    template_name = 'dashboard/logout.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    login_url = LOGIN_URL


class SpeakersView(LoginRequiredMixin, ListView):
    model = Speaker
    template_name = 'dashboard/speakers/list.html'
    context_object_name = 'speakers'
    login_url = LOGIN_URL


class SpeakerDetailView(LoginRequiredMixin, DetailView):
    model = Speaker
    template_name = 'dashboard/speakers/detail.html'
    context_object_name = 'speaker'
    login_url = LOGIN_URL


class SpeakerCreateView(LoginRequiredMixin, CreateView):
    model = Speaker
    template_name = 'dashboard/speakers/create.html'
    form_class = SpeakerForm
    success_url = '/dashboard/speakers'
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(SpeakerCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context

    def form_valid(self, form):
        self.object = form.save()
        serializer = SpeakerSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Speaker", type_of_change="create", content=json)
        return HttpResponseRedirect(self.get_success_url())


class SpeakerDeleteView(LoginRequiredMixin, DeleteView):
    model = Speaker
    template_name = 'dashboard/speakers/delete.html'
    success_url = '/dashboard/speakers'
    context_object_name = 'speaker'
    login_url = LOGIN_URL

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        serializer = SpeakerSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Speaker", type_of_change="delete", content=json)
        self.object.delete()
        return HttpResponseRedirect(success_url)


class SpeakerUpdateView(LoginRequiredMixin, UpdateView):
    model = Speaker
    # fields = ['name', 'surname', 'company_id', 'picture_id', 'description']
    template_name = 'dashboard/speakers/create.html'
    success_url = '/dashboard/speakers'
    form_class = SpeakerForm
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(SpeakerUpdateView, self).get_context_data(**kwargs)
        context['isEdited'] = True
        return context

    def form_valid(self, form):
        self.object = form.save()
        serializer = SpeakerSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Speaker", type_of_change="update", content=json)
        return HttpResponseRedirect(self.get_success_url())


class LecturesView(LoginRequiredMixin, ListView):
    model = Lecture
    template_name = 'dashboard/lectures/list.html'
    context_object_name = 'lectures'
    login_url = LOGIN_URL


class LectureDetailView(LoginRequiredMixin, DetailView):
    model = Lecture
    template_name = 'dashboard/lectures/detail.html'
    context_object_name = 'lecture'
    login_url = LOGIN_URL


class LectureCreateView(LoginRequiredMixin, CreateView):
    model = Lecture
    template_name = 'dashboard/lectures/create.html'
    form_class = LectureForm
    success_url = '/dashboard/lectures'
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(LectureCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        serializer = LectureSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Lecture", type_of_change="create", content=json)
        return HttpResponseRedirect(self.get_success_url())

"""    def form_valid(self, form):
        self.object = form.save()
        for speaker in form.cleaned_data["speakers"]:
            s = SpeakerLecture.objects.get_or_create(lecture_id=self.object, speaker_id=speaker)

        return HttpResponseRedirect(self.get_success_url())"""


class LectureDeleteView(LoginRequiredMixin, DeleteView):
    model = Lecture
    template_name = 'dashboard/lectures/delete.html'
    success_url = '/dashboard/lecture'
    context_object_name = 'lecture'
    login_url = LOGIN_URL
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        serializer = LectureSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Lecture", type_of_change="delete", content=json)
        self.object.delete()
        return HttpResponseRedirect(success_url)


class LectureUpdateView(LoginRequiredMixin, UpdateView):
    model = Lecture
    template_name = 'dashboard/lectures/create.html'
    form_class = LectureForm
    success_url = '/dashboard/lectures'
    context_object_name = 'lecture'
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(LectureUpdateView, self).get_context_data(**kwargs)
        context['isEdited'] = True
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        serializer = LectureSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Lecture", type_of_change="update", content=json)
        return HttpResponseRedirect(self.get_success_url())
    
"""    def form_valid(self, form):
        self.object = form.save()
        q = SpeakerLecture.objects.filter(lecture_id=self.object)
        for attribution in q:
            if attribution.speaker_id not in form.cleaned_data["speakers"]:
                attribution.delete()
        for speaker in form.cleaned_data["speakers"]:
            s = SpeakerLecture.objects.get_or_create(lecture_id=self.object, speaker_id=speaker)

        return HttpResponseRedirect(self.get_success_url())
"""

class CompanyView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'dashboard/companies/list.html'
    context_object_name = 'companies'
    login_url = LOGIN_URL


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'dashboard/companies/detail.html'
    context_object_name = 'company'
    login_url = LOGIN_URL


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    template_name = "dashboard/companies/create.html"
    form_class = CompanyForm
    success_url = '/dashboard/companies'
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(CompanyCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context

    def form_valid(self, form):
        self.object = form.save()
        serializer = CompanySerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Company", type_of_change="create", content=json)
        return HttpResponseRedirect(self.get_success_url())


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'dashboard/companies/delete.html'
    success_url = '/dashboard/companies'
    context_object_name = 'company'
    login_url = LOGIN_URL
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        serializer = CompanySerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Company", type_of_change="delete", content=json)
        self.object.delete()
        return HttpResponseRedirect(success_url)


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = 'dashboard/companies/create.html'
    form_class = CompanyForm
    success_url = '/dashboard/companies'
    context_object_name = 'company'
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        context['isEdited'] = True
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        serializer = CompanySerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Company", type_of_change="update", content=json)
        return HttpResponseRedirect(self.get_success_url())


class PlacesView(LoginRequiredMixin, ListView):
    model = Place
    template_name = 'dashboard/places/list.html'
    context_object_name = 'places'
    login_url = LOGIN_URL


class PlaceCreateView(LoginRequiredMixin, CreateView):
    model = Place
    template_name = 'dashboard/places/create.html'
    fields = ['building_name', 'room_name']
    success_url = '/dashboard/places'
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(PlaceCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        serializer = PlaceSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Place", type_of_change="create", content=json)
        return HttpResponseRedirect(self.get_success_url())


class PlaceDeleteView(LoginRequiredMixin, DeleteView):
    model = Place
    template_name = 'dashboard/places/delete.html'
    success_url = '/dashboard/places'
    context_object_name = 'place'
    login_url = LOGIN_URL
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        serializer = PlaceSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Place", type_of_change="delete", content=json)
        self.object.delete()
        return HttpResponseRedirect(success_url)


class PlaceUpdateView(LoginRequiredMixin, UpdateView):
    model = Place
    template_name = 'dashboard/places/create.html'
    fields = ['building_name', 'room_name']
    success_url = '/dashboard/places'
    context_object_name = 'place'
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(PlaceUpdateView, self).get_context_data(**kwargs)
        context['isEdited'] = True
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        serializer = PlaceSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Place", type_of_change="update", content=json)
        return HttpResponseRedirect(self.get_success_url())


class PartnerStatusesView(LoginRequiredMixin, ListView):
    model = PartnerStatus
    template_name = 'dashboard/partner_statuses/list.html'
    context_object_name = 'statuses'
    login_url = LOGIN_URL


class PartnerStatusCreateView(LoginRequiredMixin, CreateView):
    model = PartnerStatus
    template_name = 'dashboard/partner_statuses/create.html'
    fields = ['name', 'priority']
    success_url = '/dashboard/partner_statuses'
    login_url = LOGIN_URL
    
    def form_valid(self, form):
        self.object = form.save()
        serializer = PartnerStatusSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="PartnerStatus", type_of_change="create", content=json)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(PartnerStatusCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context


class PartnerStatusDeleteView(LoginRequiredMixin, DeleteView):
    model = PartnerStatus
    template_name = 'dashboard/partner_statuses/delete.html'
    success_url = '/dashboard/partner_statuses'
    context_object_name = 'status'
    login_url = LOGIN_URL
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        serializer = PartnerStatusSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="PartnerStatus", type_of_change="delete", content=json)
        self.object.delete()
        return HttpResponseRedirect(success_url)


class PartnerStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = PartnerStatus
    template_name = 'dashboard/partner_statuses/create.html'
    fields = ['name', 'priority']
    success_url = '/dashboard/partner_statuses'
    context_object_name = 'status'
    login_url = LOGIN_URL
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        serializer = PartnerStatusSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="PartnerStatus", type_of_change="delete", content=json)
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super(PartnerStatusUpdateView, self).get_context_data(**kwargs)
        context['isEdited'] = True
        return context


class NewsesView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'dashboard/news/list.html'
    context_object_name = 'newses'
    login_url = LOGIN_URL


class NewsDetailView(LoginRequiredMixin, DetailView):
    model = News
    template_name = 'dashboard/news/detail.html'
    context_object_name = 'news'
    login_url = LOGIN_URL


class NewsCreateView(LoginRequiredMixin, CreateView):
    form_class = NewsForms
    template_name = 'dashboard/news/create.html'
    success_url = '/dashboard/news'
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(NewsCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        serializer = NewsSerializer(self.object, allow_null=True)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="News", type_of_change="create", content=json)
        return HttpResponseRedirect(self.get_success_url())
    
    """def form_valid(self, form):
        return super(NewsCreateView, self).form_valid(form)"""


class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'dashboard/news/delete.html'
    success_url = '/dashboard/news'
    login_url = LOGIN_URL
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        serializer = NewsSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="News", type_of_change="delete", content=json)
        self.object.delete()
        return HttpResponseRedirect(success_url)


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    form_class = NewsForms
    template_name = 'dashboard/news/create.html'
    success_url = '/dashboard/news'
    context_object_name = 'news'
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(NewsUpdateView, self).get_context_data(**kwargs)
        context['isEdited'] = True
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        serializer = NewsSerializer(self.object, allow_null=True)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="News", type_of_change="update", content=json)
        return HttpResponseRedirect(self.get_success_url())
    
    """def form_valid(self, form):
        return super(NewsUpdateView, self).form_valid(form)"""


class PicturesView(LoginRequiredMixin, ListView):
    model = Picture
    template_name = 'dashboard/pictures/list.html'
    context_object_name = 'pictures'
    queryset = Picture.objects.all().reverse()
    login_url = LOGIN_URL


class PictureCreateView(LoginRequiredMixin, CreateView):
    model = Picture
    template_name = 'dashboard/pictures/create.html'
    fields = ['source']
    success_url = '/dashboard/pictures'
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(PictureCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        serializer = PictureSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Picture", type_of_change="create", content=json)
        return HttpResponseRedirect(self.get_success_url())


class PictureDeleteView(LoginRequiredMixin, DeleteView):
    model = Picture
    template_name = 'dashboard/pictures/delete.html'
    success_url = '/dashboard/pictures'
    login_url = LOGIN_URL
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        serializer = PictureSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Picture", type_of_change="delete", content=json)
        self.object.delete()
        return HttpResponseRedirect(success_url)


class NotifyView(LoginRequiredMixin, FormView):
    success_url = '/dashboard'
    template_name = 'dashboard/notify.html'
    login_url = LOGIN_URL
    form_class = NotifyForm

    def form_valid(self, form):
        message = {
            'id': timezone.now().strftime("%Y%m%d%H%M%S"),
            'content': form.cleaned_data['content'],
            'type_of_message': form.cleaned_data['type_of_notification'].name
        }
        group = "chat_%s" % form.cleaned_data['channel'].name
        layer = get_channel_layer()
        async_to_sync(layer.group_send)(group, {
            'type': 'chat_message',
            'message': json.dumps(message)
        })
        return super(NotifyView, self).form_valid(form)


class PhotoView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'dashboard/pictures/list.html'
    context_object_name = 'pictures'
    queryset = Photo.objects.all().reverse()
    login_url = LOGIN_URL


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    template_name = 'dashboard/pictures/create.html'
    fields = ['source']
    success_url = '/dashboard/pictures'
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(PhotoCreateView, self).get_context_data(**kwargs)
        context['isEdited'] = False
        return context

    def form_valid(self, form):
        self.object = form.save()
        serializer = PictureSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Photo",
                                              type_of_change="create",
                                              content=json)
        return HttpResponseRedirect(self.get_success_url())


class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = 'dashboard/pictures/delete.html'
    success_url = '/dashboard/pictures'
    login_url = LOGIN_URL

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        serializer = PictureSerializer(self.object)
        renderer = JSONRenderer()
        renderer.charset = "utf-8"
        json = renderer.render(serializer.data).decode("utf-8")
        change_object = Change.objects.create(model="Photo",
                                              type_of_change="delete",
                                              content=json)
        self.object.delete()
        return HttpResponseRedirect(success_url)