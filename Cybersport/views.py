from typing import Tuple, Container
from hashlib import sha1

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.template.loader import render_to_string
from django.urls import resolve
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import QuerySet, Q
from django.core.paginator import Paginator
from django.core.mail import send_mail

from .forms import NewForm, ChangeUserDataForm, RegistrationForm

from . import models


FIELDS_FOR_SEARCH: Tuple[str, ...] = ('title', 'text', 'date')

NEWS_PER_PAGE: int = 5


def user_is_page_owner_required(view):
    def wrapper(request, username, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('authorization')
        elif request.user.username != username:
            return redirect('edit-user', username=request.user.get_username())
        return view(request, *args, **kwargs)
    return wrapper


def _show_news(request: HttpRequest, news: QuerySet, context: dict = None):
    paginator = Paginator(news, NEWS_PER_PAGE)
    page_number = request.GET.get('page', 1)
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


def show_post(request: HttpRequest, slug: str):
    post = models.New.objects.get(slug=slug)
    return render(request, 'Cybersport/post.html', {'new': post})


def send_email_confirmation(request: HttpRequest, username: str, emails: Container):
    subject_text: str = "Cybersport.social подтверждение аккаунта"
    confirmation_code = sha1(username.encode()).hexdigest()[:5]

    context: dict = {
        'request': request,
        'username': username,
        'confirmation_code': confirmation_code
    }

    html_message = render_to_string('Cybersport/email-confirmation-mail.html', context=context)
    from_email = None
    send_mail(subject=subject_text, message=None, from_email=from_email, recipient_list=emails,
              html_message=html_message)


def email_confirmation_sended(request: HttpRequest):
    return render(request, 'Cybersport/email-confirmation-sended.html')


def registration(request: HttpRequest):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main-page')
    else:
        form = RegistrationForm()

    context: dict = {
        'form': form,
    }

    return render(request, 'Cybersport/registration.html', context)


def email_confirmation(request: HttpRequest):
    username: str = request.GET.get('username')
    confirmation_code: str = request.GET.get('confirmation-code')
    if sha1(username.encode()).hexdigest()[:5] == confirmation_code:
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
    return redirect('main-page')


def authorization(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('main-page')
    else:
        form = AuthenticationForm()
    context: dict = {
        'form': form
    }
    return render(request, 'Cybersport/authorization.html', context)


def logout_user(request: HttpRequest):
    logout(request)
    return redirect('main-page')


def search(request: HttpRequest):
    search_param: str = request.GET.get('search-param')

    if search_param:
        args: list = []
        for field in FIELDS_FOR_SEARCH:
            args.append(f'Q({field}__icontains=search_param)')
        queryset: QuerySet = models.New.objects.filter(eval(' | '.join(args)))
    else:
        queryset: QuerySet = models.New.objects.all()

    context: dict = {
        'title': f'Результаты по запросу "{search_param}"'
    }

    return _show_news(request=request, news=queryset, context=context)


def show_user(request: HttpRequest, username: str):
    page_owner = User.objects.get(username=username)
    context: dict = {
        'page_owner': page_owner
    }
    return render(request, 'Cybersport/user.html', context)


@user_is_page_owner_required
def edit_user(request: HttpRequest):
    if request.method == 'POST':
        form = ChangeUserDataForm(request=request, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('main-page')

    else:
        form = ChangeUserDataForm(request)
    return render(request, 'Cybersport/edit-user.html', context={'form': form})


def test(request: HttpRequest):
    return render(request, 'Cybersport/test.html')
