from django.urls import path
from . import views

urlpatterns = [
    path('alllogsets/', views.list_all_logsets, name='list_all_logsets'),
    path('', views.query_app, name='query_app'),
    path('search_logs', views.search_logs, name='search_logs'),
    # Other URL patterns...
]
