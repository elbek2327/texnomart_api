from django.urls import path
from texnomart import views
from .views import ProductListView

urlpatterns = [
    path('nothing/', views.some, name='nothing'),
    # showing all products
    path('products_all/', views.ProductListView.as_view(), name='products_all')
    
]
