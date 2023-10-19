from django.urls import path

from .views import NewsList, News, Search

urlpatterns = [
   path('', NewsList.as_view()),
   path('<int:pk>', News.as_view()),
   path('search', Search.as_view()),
]