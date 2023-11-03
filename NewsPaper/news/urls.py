from django.urls import path

from .views import (NewsList, News, Search, NewsCreate, NewsEdit, NewsDelete, ArticlesCreate,
                    ArticlesEdit, ArticlesDelete, subscriptions)

urlpatterns = [
   path('news/', NewsList.as_view(), name='news_list'),
   path('news/<int:pk>', News.as_view(), name='news_detail'),
   path('news/search', Search.as_view()),
   path('news/create', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create', ArticlesCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', ArticlesEdit.as_view(), name='articles_update'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]