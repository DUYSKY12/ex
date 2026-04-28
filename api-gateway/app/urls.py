from django.urls import path
from . import views

urlpatterns = [
    # Page Renders
    path('', views.homepage, name='homepage'),
    path('login/<str:role>/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    
    path('customer/', views.customer_home, name='customer_home'),
    path('customer/profile/', views.customer_profile, name='customer_profile'),
    path('customer/checkout/', views.customer_checkout, name='customer_checkout'),
    
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),

    # API / Proxy Endpoints
    path('api/products/', views.api_products, name='api_products'),
    path('api/search/', views.api_search, name='api_search'),
    
    # Generic proxy for other microservices
    path('api/proxy/<str:service>/<path:endpoint>', views.proxy_view, name='proxy_view'),
]
