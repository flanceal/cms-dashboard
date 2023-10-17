from django.urls import path
from . import views

urlpatterns = [
    path('customers/', views.CustomerListCreateView.as_view()),
    path('customers/<int:pk>/', views.CustomerRetrieveUpdateDestroyView.as_view()),
    path('products/', views.ProductListView.as_view()),
    path('products/<int:pk>', views.ProductRetrieveUpdateDestroyView.as_view()),
]