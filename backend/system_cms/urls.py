from django.urls import path
from . import views
from .auth_views import CustomObtainAuthToken

urlpatterns = [
    path('api/token/', CustomObtainAuthToken.as_view(), name='obtain-token'),
    path('api/customers/', views.CustomerListCreateView.as_view()),
    path('api/customers/<int:pk>/', views.CustomerRetrieveUpdateDestroyView.as_view()),
    path('api/products/', views.ProductListView.as_view()),
    path('api/products/<int:pk>', views.ProductRetrieveUpdateDestroyView.as_view()),
    path('api/orders/', views.OrderListView.as_view()),
    path('api/orders/<int:pk>/', views.OrderRetrieveUpdateDestroyView.as_view()),
]