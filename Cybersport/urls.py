from django.urls import path, re_path
from django.shortcuts import HttpResponsePermanentRedirect, reverse

from . import views

urlpatterns = [
    path('post/<str:slug>', views.show_post, name='show-post'),
    path('news/', views.show_all_news, name='main-page'),
    path('news/<str:category_slug>/', views.show_category_news, name='category'),
    path('user/<str:username>/', views.show_user, name='user'),
    path('user/<str:username>/posts/', views.show_user_posts, name='user-posts'),
    path('add-new/', views.add_new, name='add-new'),
    path('registration/', views.registration, name='registration'),
    path('authorization/', views.authorization, name='authorization'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.search, name='search'),
    re_path(r'.*', lambda request: HttpResponsePermanentRedirect(reverse('main-page'))),
]
