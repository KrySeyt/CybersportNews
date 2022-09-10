from django.shortcuts import redirect
from django.urls import path, include, reverse

from . import views


urlpatterns = [
    path('', views.show_all_news),
    path('news/', views.show_all_news, name='main-page'),
    path('news/<slug:category_slug>/', views.show_category_news, name='category'),
    path('post/<slug:post_slug>', views.show_post, name='show-post'),
    path('like/<str:object_type>/<int:pk>', views.like, name='like'),
    path('unlike/<str:object_type>/<int:pk>', views.unlike, name='unlike'),
    path('dislike/<str:object_type>/<int:pk>', views.dislike, name='dislike'),
    path('undislike/<str:object_type>/<int:pk>', views.undislike, name='undislike'),
    path('add-comment/<str:object_type>/<int:pk>', views.add_comment, name='add-comment'),
    path('delete-comment/<int:comment_pk>', views.delete_comment, name='delete-comment'),
    path('user/<str:username>/', views.show_user, name='user'),
    path('user/<str:username>/posts/', views.show_user_posts, name='user-posts'),
    path('user/<str:username>/comments/', views.show_user_comments, name='user-comments'),
    path('user/<str:username>/edit/', views.edit_user, name='edit-user'),
    path('add-new/', views.add_new, name='add-new'),
    path('delete-new/<slug:post_slug>', views.delete_new, name='delete-new'),
    path('registration/', views.registration, name='registration'),
    path('authorization/', views.authorization, name='authorization'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.search, name='search'),
    path('email-confirmation/sended/', views.email_confirmation_sended, name='email-confirmation-sended'),
    path('email-confirmation/', views.email_confirmation, name='email-confirmation'),
    path('test', views.test),
]
