from django.urls import path, re_path
from django.shortcuts import HttpResponsePermanentRedirect, reverse

from . import views

urlpatterns = [
    path('post/<str:slug>', views.Post.as_view(), name='show-post'),
    path('news/', views.News.as_view(), name='main-page'),
    path('news/<str:category_slug>', views.Category.as_view(), name='category'),
    path('add-post/', views.AddNew.as_view(), name='add-new'),
    path('registration/', views.registration, name='registration'),
    path('authorization/', views.authorization, name='authorization'),
    re_path(r'.*', lambda request: HttpResponsePermanentRedirect(reverse('main-page'))),
]
