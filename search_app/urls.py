from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_app, name='search_app'),
    # Other URL patterns...
]
