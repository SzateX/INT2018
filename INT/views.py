from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import *


class NewsListView(ListView):
    model = News
    template_name = 'news/list.html'
    context_object_name = 'news_list'
    queryset = model.objects.all().order_by('-publish_date')


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company/detail.html'
    context_object_name = 'company'


class SpeakerDetailView(DetailView):
    model = Speaker
    template_name = 'speaker/detail.html'
    context_object_name = 'speaker'

    def get_context_data(self, **kwargs):
        context = super(SpeakerDetailView, self).get_context_data(**kwargs)
        context['lectures'] = Lecture.objects.filter(speaker=self.object).order_by('begin_time')
        return context


class KodziarzeView(TemplateView):
    template_name = 'kodziarze_detail.html'