from django.shortcuts import redirect
from django.urls import path

from . import views


urlpatterns = [
    path('post/<str:slug>', views.show_post, name='show-post'),
    path('news/', views.show_all_news, name='main-page'),
    path('news/<str:category_slug>/', views.show_category_news, name='category'),
    path('user/<str:username>/', views.show_user, name='user'),
    path('user/<str:username>/posts/', views.show_user_posts, name='user-posts'),
    path('user/<str:username>/edit/', views.edit_user, name='edit-user'),
    path('add-new/', views.add_new, name='add-new'),
    path('registration/', views.registration, name='registration'),
    path('authorization/', views.authorization, name='authorization'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.search, name='search'),
    path('email-confirmation/sended/', views.email_confirmation_sended, name='email-confirmation-sended'),
    path('email-confirmation/', views.email_confirmation, name='email-confirmation'),
    path('test', views.test),
    path('', lambda request: redirect('main-page')),
]
