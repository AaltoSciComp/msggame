from django.urls import path

from . import views

urlpatterns = [
    path(r'status/', views.status, name='status'),
    path(r'network/digraph', views.network_digraph, name='network_digraph'),
    path(r'network/stats', views.network_stats, name='network_stats'),
    path(r'', views.index, name='index'),
]
