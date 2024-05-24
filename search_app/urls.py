from django.urls import path
from . import views

urlpatterns = [
    path('alllogsets/', views.list_all_logsets, name='list_all_logsets'),
    path('', views.search_app, name='search_app'),
    # Other URL patterns...
]
