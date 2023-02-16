from django.urls import path
from apps.api.blog.views import ArticleListView, ArticleCreateView, ArticleDeleteView, ArticleDetailView,\
    ArticleUpdateView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('article/', ArticleListView.as_view()),
    path('article/<int:pk>/', ArticleDetailView.as_view()),
    path('article/create/', ArticleCreateView.as_view()),
    path('article/update/<int:pk>/', ArticleUpdateView.as_view()),
    path('article/delete/<int:pk>/', ArticleDeleteView.as_view()),
]