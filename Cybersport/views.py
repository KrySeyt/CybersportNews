from django.http import HttpRequest
from django.views.generic import ListView, DetailView
from django.utils.timezone import activate

import pytz

from . import models


class MainPage(ListView):
    model = models.New
    template_name = 'Cybersport/main.html'
    context_object_name = 'news'

    # def setup(self, request: HttpRequest, *args, **kwargs):
    #     super(MainPage, self).setup(request, *args, **kwargs)
    #     timezone: pytz.timezone = pytz.timezone('Europe/Moscow')
    #     activate(timezone)

    def get_context_data(self, *args, **kwargs):
        context: dict = super(MainPage, self).get_context_data(*args, **kwargs)
        context['title'] = 'Все новости'
        return context


class Post(DetailView):
    context_object_name = 'new'
    model = models.New
    template_name = 'Cybersport/post.html'

