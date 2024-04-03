# urls.py

from django.urls import path
from Staff import views
urlpatterns = [
    path('create_staff/', views.create_staff, name='create_staff'),
    path('create_position/', views.create_position, name='create_position'),
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/<int:pk>/delete/', views.staff_delete, name='staff_delete'),
    path('positions/', views.position_list, name='position_list'),
    path('positions/<int:pk>/delete/', views.position_delete, name='position_delete'),
]
