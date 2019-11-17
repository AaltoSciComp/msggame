from django.urls import path

from . import views

urlpatterns = [
    path(r'status/', views.status, name='status'),
    path(r'network/', views.view_network, name='network'),
    path(r'', views.index, name='index'),
]
