# urls.py

from django.urls import path
from Staff import views
urlpatterns = [
    path('create_position/', views.create_position, name='create_position'),
    path('positions/', views.position_list, name='position_list'),
    path('get-subpositions/', views.get_subpositions, name='get_subpositions'),#pylint: disable=no-member
    path('subpositions/', views.subpositions_list, name='subposition_list'),# pylint: disable=no-member
    path('subpositions/<int:pk>/confirm_delete/', views.confirm_delete_subposition, name='confirm_delete_subposition'),
    path('subpositions/<int:pk>/delete/', views.delete_subposition, name='delete_subposition'),

    path('create_staff/', views.create_staff, name='create_staff'),# pylint: disable=no-member
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/<int:staff_id>/', views.staff_detail, name='staff_detail'),
    path('staff/<int:pk>/delete/', views.confirm_delete_staff, name='staff_delete'),
    path('staff/<int:staff_id>/edit/', views.edit_staff, name='staff_edit'),
    path('get-staff/', views.get_staff, name='get_staff'),
    path('check-id-number/', views.check_id_number, name='check_id_number'),#pylint:disable=no-member
]
