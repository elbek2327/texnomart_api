from django.urls import path
from texnomart import views
from .views import ProductListView, CategoryProductListView, ProductByCategoryListView

urlpatterns = [
    # showing all products 1 st task
    path('products_all/', views.ProductListView.as_view(), name='products_all'),
    # Showing all category and products 2nd task
    path('categories/<slug:category_slug>/products/', views.CategoryProductListView.as_view(), name='category_product_list'),
    
    path('products/by_category/', views.ProductByCategoryListView.as_view(), name='product_by_category'),
    
    
    
]
