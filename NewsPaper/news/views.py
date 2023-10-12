from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'newslist.html'
    context_object_name = 'newslist'


class News(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
