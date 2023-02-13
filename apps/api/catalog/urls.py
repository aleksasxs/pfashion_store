from django.urls import path
from apps.api.catalog.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView,\
    ProductDeleteView, CategoryListView, CategoryDetailView, CategoryDeleteView, CategoryCreateView, CategoryUpdateView


urlpatterns = [
    path('product/', ProductListView.as_view()),
    path('product/<int:pk>/', ProductDetailView.as_view()),
    path('product/create/', ProductCreateView.as_view()),
    path('product/update/<int:pk>/', ProductUpdateView.as_view()),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view()),

    path('category/', CategoryListView.as_view()),
    path('category/<int:pk>/', CategoryDetailView.as_view()),
    path('category/create/', CategoryCreateView.as_view()),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view()),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view()),
]