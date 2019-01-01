from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import *


class NewsListView(ListView):
    model = News
    template_name = 'INT/news/list.html'
    context_object_name = 'news_list'
    queryset = model.objects.all().order_by('-publish_date')


class NewsDetailView(DetailView):
    model = News
    template_name = 'INT/news/detail.html'
    context_object_name = 'news'


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'INT/company/detail.html'
    context_object_name = 'company'


class SpeakerDetailView(DetailView):
    model = Speaker
    template_name = 'INT/speakers/detail.html'
    context_object_name = 'speaker'


class HomepageView(TemplateView):
    template_name = 'INT/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['lectures'] = Lecture.objects.all().order_by('begin_time')
        context['partners'] = Company.objects.all()
        context['partner_statuses'] = PartnerStatus.objects\
            .filter(priority__isnull=False)\
            .order_by('priority').prefetch_related('companies')
        return context


class KodziarzeView(TemplateView):
    template_name = 'INT/kodziarze_detail.html'