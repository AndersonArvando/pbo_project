"""coding URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.loginT, name='login'),
    path('logout', views.logout, name='logout'),
    path('product', views.product, name='product'),
    path('product/add', views.productAdd, name='product/add'),
    path('product/edit/<int:id>', views.productEdit, name='product/edit'),
    path('product/update/<int:id>', views.productUpdate, name='product/update'),
    path('product/delete/<int:id>', views.productDelete, name='product/delete'),
    path('vendor', views.vendor, name='vendor'),
    path('vendor/add', views.vendorAdd, name='vendor/add'),
    path('vendor/edit/<int:id>', views.vendorEdit, name='vendor/edit'),
    path('vendor/delete/<int:id>', views.vendorDelete, name='vendor/delete'),
    path('transaction', views.transaction, name='transaction'),
    path('transaction/add', views.transactionAdd, name='transaction/add'),
    path('transaction/edit/<int:id>', views.transactionEdit, name='transaction/edit'),
    path('transaction/delete/<int:id>', views.transactionDelete, name='transaction/delete')
]
