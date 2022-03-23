"""BarSender URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as auth_token_views
from django.urls import path, include
from Bar_Sender_api import views

router = DefaultRouter(trailing_slash=False)
router.register(r'categories', views.CategoryView, 'category')
router.register(r'orders', views.OrderView, 'order')
router.register(r'payment-types', views.PaymentTypeView, 'payment_type')
router.register(r'products', views.ProductView, 'product')
router.register(r'stores', views.StoreView, 'store')
router.register(r'profile', views.ProfileView, 'profile')
router.register(r'users', views.MyUserView, 'users')

urlpatterns = [
    path('', include(router.urls)),
    path('login', views.login_user),
    path('register', views.register_user)
]
