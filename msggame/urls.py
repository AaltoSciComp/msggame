from django.urls import path

from . import views

urlpatterns = [
    path(r'status/', views.status, name='status'),
    path(r'', views.index, name='index'),
]
