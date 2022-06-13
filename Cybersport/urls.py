from django.urls import path
from django.shortcuts import HttpResponsePermanentRedirect, reverse

from . import views

urlpatterns = [
    path('post/<str:slug>', views.Post.as_view(), name='show-post'),
    path('news/<str:category_slug>', views.Category.as_view(), name='main-page'),
    # path('<int:category_id>', lambda request, category_id: HttpResponsePermanentRedirect(reverse('main-page',
    #                                                                                              category_id))),
    path('', lambda request: HttpResponsePermanentRedirect(reverse('main-page', 'all'))),
]
