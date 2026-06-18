from django.urls import path,include
from unicodedata import category, name

from products.views import (
    ProductListView,ProductDetailView,CategoryListView,CategoryDetailView,
    FileListView,FileDetailView,
)
urlpatterns = [
    path('categories/' , CategoryListView.as_view(),name='categories-list'),
    path('categories/<int:pk>/' , CategoryDetailView.as_view(),name='categories-detail'),


    path('products/',ProductListView.as_view(),name='product-List'),
    path('products/<int:pk>',ProductDetailView.as_view(),name='product-detail'),

    path('products/<int:product_pk>/files/',FileListView.as_view(),name='file_list'),
    path('products/<int:product_pk>/files/<int:pk>/',FileDetailView.as_view(),name='file_detail'),
]