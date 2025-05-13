from django.urls import path
from texnomart import views
from .views import (ProductListView,
                    CategoryProductListView,
                    ProductByCategoryListView,
                    CategoryListCreateView,
                    CategoryRetrieveUpdateDestroyView,
                    ProductListCreateView,
                    ProductRetriveUpdateDestroyView)

urlpatterns = [
    # showing all products 1 st task
    path('products_all/', views.ProductListView.as_view(), name='products_all'),
    
    
    # Showing all category and products 2nd task
    path('category/<slug:category_slug>/products/', views.CategoryProductListView.as_view(), name='category_product_list'),
    # hamma productlarni kategoriyalari bilan chiqarib beradi unsorted
    path('products/by_category/', views.ProductByCategoryListView.as_view(), name='product_by_category'),
    
    #3rd task
    path('category_add/', views.CategoryListCreateView.as_view(), name='category_add'),
    path('category/<slug:slug>/', views.CategoryRetrieveUpdateDestroyView.as_view(), name='category_update_delete'),
    
    path('product_add/', views.ProductListCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/', views.ProductRetriveUpdateDestroyView.as_view(), name='product_update_delete'),
    
    
    
]
