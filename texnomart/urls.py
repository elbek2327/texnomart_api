from django.urls import path
from texnomart import views
from .views import (RegisterApiView,
                    LoginApiView,
                    LogoutView,
                    ProductListView,
                    CategoryProductListView,
                    ProductByCategoryListView,
                    CategoryListCreateView,
                    CategoryRetrieveUpdateDestroyView,
                    ProductListCreateView,
                    ProductRetriveUpdateDestroyView,
                    KorzinkaListView,
                    KorzinkaListCreateView,
                    KorzinkaRetriveUpdateDestroyView,
                    CommentListView, 
                    CommentCreateView,
                    CommentUpdateDeleteView)
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    #User authentication
    path('register/', views.RegisterApiView.as_view(), name='register'),
    # path('login/', views.LoginApiView.as_view(), name='login'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Products all
    path('all_products/', views.ProductListView.as_view(), name='all_products'),
    
    # Taking all products and category elements
    path('category/<slug:category_slug>/products/', views.CategoryProductListView.as_view(), name='category_product_list'),
    
    # Productni Category orqali chiqarish
    path('products/by_category/', views.ProductByCategoryListView.as_view(), name='product_by_category'),
    
    #Category CRUD
    path('category_add/', views.CategoryListCreateView.as_view(), name='category_add'),
    path('category/<slug:slug>/', views.CategoryRetrieveUpdateDestroyView.as_view(), name='category_update_delete_by_id'),
    
    # Product CRUD
    path('product_add/', views.ProductListCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/', views.ProductRetriveUpdateDestroyView.as_view(), name='product_update_delete_by_id'),
    
    #Korzinka
    path('all_korzinka/', views.KorzinkaListView.as_view(), name='all_things_in_korzinka'),
    path('korzinka_add/', views.KorzinkaListCreateView.as_view(), name='add_item_to_korzinka'),
    path('korzinka/edit/<int:pk>/', views.KorzinkaRetriveUpdateDestroyView.as_view(), name='change_korzinka_by_id'),
    
    #Comments
    path('all_comments/', views.CommentListView.as_view(), name='all_comments'),
    path('comment_add/', views.CommentCreateView.as_view(), name='add comment'),
    path('comment/edit/<int:pk>/', views.CommentUpdateDeleteView.as_view(), name='change_comment_by_id'),
    
]
