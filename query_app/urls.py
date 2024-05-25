from django.urls import path
from . import views

app_name = 'query_app'

urlpatterns = [
    path('alllogsets/', views.list_all_logsets, name='list_all_logsets'),
    path('', views.query_app, name='query_app'),
    path('simple_log_query/', views.simple_log_query, name='simple_log_query'),
]

