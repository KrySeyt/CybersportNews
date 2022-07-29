from typing import Tuple

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import QuerySet
from django.core.paginator import Paginator

from .forms import NewForm

from . import models


FIELDS_FOR_SEARCH: Tuple[str, ...] = ('title', 'text', 'date')

NEWS_PER_PAGE: int = 5


def _show_news(request: HttpRequest, news: QuerySet, context: dict = None):
    paginator = Paginator(news, NEWS_PER_PAGE)
    page_number = request.GET.get('page', 1)
    print(page_number)
    page_obj = paginator.get_page(page_number)

    if not context:
        context = dict()

    context['page_obj'] = page_obj

    return render(request, 'Cybersport/main.html', context)


def show_category_news(request: HttpRequest, category_slug: str):
    news = models.New.objects.filter(category__slug=category_slug, is_published=True).order_by('-date')
    context: dict = {
        'title': models.Category.objects.get(slug=category_slug).name
    }
    return _show_news(request, news, context)


def show_user_posts(request: HttpRequest, username: str):
    news = models.New.objects.filter(author__username=username, is_published=True).order_by('-date')
    context: dict = {
        'title': f'Новости {username}'
    }
    return _show_news(request, news, context)


def show_all_news(request: HttpRequest):
    news = models.New.objects.filter(is_published=True).order_by('-date')
    context: dict = {
        'title': 'Все новости'
    }
    return _show_news(request, news, context)


class News(ListView):
    paginate_by = 5
    model = models.New
    template_name = 'Cybersport/main.html'
    context_object_name = 'news'

    def get_context_data(self, *args, **kwargs):
        context: dict = super(News, self).get_context_data(*args, **kwargs)
        context['title'] = 'Все новости'
        return context

    def get_queryset(self):
        return models.New.objects.filter(is_published=True)


class Category(News):
    def get_context_data(self, *args, **kwargs) -> dict:
        context: dict = super(Category, self).get_context_data(*args, **kwargs)
        context['title'] = self.kwargs['category'].name
        return context

    def get_queryset(self):
        self.kwargs['category'] = models.Category.objects.get(slug=self.kwargs['category_slug'])
        return models.New.objects.filter(category_id=self.kwargs['category'].pk, is_published=True)


def add_new(request: HttpRequest):
    if request.method == 'POST':
        form = NewForm(request.POST)
        if form.is_valid():
            new = form.save()
            new.slug = slugify(new.title, allow_unicode=True)

            if request.user.is_authenticated:
                new.author = request.user

            new.save()
            return HttpResponseRedirect('main-page')

    else:
        form = NewForm()

    return render(request, 'Cybersport/add-post.html', context={'form': form})


class AddNew(CreateView):

    form_class = NewForm
    template_name = 'Cybersport/add-post.html'
    context_object_name = 'form'
    success_url = reverse_lazy('main-page')


def show_post(request: HttpRequest, slug: str):
    post = models.New.objects.get(slug=slug)
    return render(request, 'Cybersport/post.html', {'new': post})


class Post(DetailView):
    context_object_name = 'new'
    model = models.New
    template_name = 'Cybersport/post.html'


def registration(request: HttpRequest):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('main-page')
    else:
        form = UserCreationForm()

    context: dict = {
        'form': form,
    }

    return render(request, 'Cybersport/registration.html', context)


def authorization(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            login(request, user)
            return HttpResponseRedirect('main-page')
    else:
        form = AuthenticationForm()
    context: dict = {
        'form': form
    }
    return render(request, 'Cybersport/authorization.html', context)


def logout_user(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect('main-page')


def search(request: HttpRequest):
    search_param: str = request.GET.get('search-param')

    if search_param:
        args: list = []
        for field in FIELDS_FOR_SEARCH:
            args.append(f'Q({field}__icontains=search_param)')
        queryset: QuerySet = models.New.objects.filter(eval(' | '.join(args)))[:5]
    else:
        queryset: QuerySet = models.New.objects.all()[:5]

    context: dict = {
        'news': queryset
    }

    return render(request, 'Cybersport/main.html', context=context)


def show_user(request: HttpRequest, username: str):
    pass
