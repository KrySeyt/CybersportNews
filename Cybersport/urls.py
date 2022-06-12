from django.urls import path

from . import views

urlpatterns = [
    path('post/<int:pk>', views.Post.as_view(), name='show-post'),
    path('', views.MainPage.as_view(), name='main-page'),
]
