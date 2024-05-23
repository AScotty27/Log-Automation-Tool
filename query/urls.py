from django.urls import path
from . import views

urlpatterns = [
    path("", views.query, name="query"),
        path('alllogsets/', views.list_all_logsets, name='alllogsets'),
]

