from django.views.generic import ListView, DetailView

from . import models


class News(ListView):
    model = models.New
    template_name = 'Cybersport/main.html'
    context_object_name = 'news'

    def get_context_data(self, *args, **kwargs):
        context: dict = super(News, self).get_context_data(*args, **kwargs)
        context['title'] = 'Все новости'
        return context

    def get_queryset(self):
        return New.objects.filter(is_published=True)


class Category(ListView):
    model = models.New
    template_name = 'Cybersport/main.html'
    context_object_name = 'news'

    def get_context_data(self, *args, **kwargs) -> dict:
        context: dict = super(Category, self).get_context_data(*args, **kwargs)
        context['title'] = self.kwargs['category'].name
        return context

    def get_queryset(self):
        self.kwargs['category'] = models.Category.objects.get(slug=self.kwargs['category_slug'])
        return models.New.objects.filter(category_id=self.kwargs['category'].pk, is_published=True)


class Post(DetailView):
    context_object_name = 'new'
    model = models.New
    template_name = 'Cybersport/post.html'

