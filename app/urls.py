from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('variables/', views.variables_view, name='variables'),
    path('new_variable/', views.new_variable, name='new_variable'),
    path('delete_variable/', views.delete_variable, name='delete_variable'),
    path('find_variable', views.find_variable, name='find_variable'),
    path('update_variable', views.update_variable, name='update_variable'),
    path('upload-variables/', views.upload_variables, name='upload_variables'),
    path('delete_variable_direct/<int:variable_id>/', views.delete_variable_direct, name='delete_variable_direct'),
]

