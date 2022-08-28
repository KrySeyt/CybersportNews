from django.shortcuts import redirect
from django.urls import path

from . import views


urlpatterns = [
    path('news/', views.show_all_news, name='main-page'),
    path('news/<slug:category_slug>/', views.show_category_news, name='category'),
    path('post/<slug:post_slug>', views.show_post, name='show-post'),
    path('post/<slug:post_slug>/like', views.like_post, name='like-post'),
    path('post/<slug:post_slug>/unlike', views.unlike_post, name='unlike-post'),
    path('post/<slug:post_slug>/dislike', views.dislike_post, name='dislike-post'),
    path('post/<slug:post_slug>/undislike', views.undislike_post, name='undislike-post'),
    path('post/<slug:post_slug>/add-comment', views.add_comment, name='add-comment'),
    path('delete-comment/<int:comment_pk>', views.delete_comment, name='delete-comment'),
    path('user/<str:username>/', views.show_user, name='user'),
    path('user/<str:username>/posts/', views.show_user_posts, name='user-posts'),
    path('user/<str:username>/comments/', views.show_user_comments, name='user-comments'),
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
