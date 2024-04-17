from django.urls import path
from PlateMate import views
from users import views as userviews 

urlpatterns = [
    path("", userviews.home, name="home"),
    path("Customer_Home/", views.Customer_Home, name = "Test Page"),
    path("Customer_Menu_Ordering/", views.Customer_Menu_Ordering, name = "Test Page"),
    path("Customer_Receipt_Check/", views.Customer_Receipt_Check, name = "Test Page"),
    path("Kitchen_Current_Orders/", views.Kitchen_Current_Orders, name = "Test Page"),
    path("Manager_Checks/", views.Manager_Checks, name = "Test Page"),
    path("Manager_Stats/", views.Manager_Stats, name = "Test Page"),
    path("Manager_Table_Assignment/", views.Manager_Table_Assignment, name = "Test Page"),
    path("Server_Check_View/", views.Server_Check_View, name = "Test Page"),
    path("Server_Pin_Log_in/", views.Server_Pin_Log_in, name = "Test Page"),
    path("Server_Table_View/", views.Server_Table_View, name = "Test Page"),
    path('floorplans/', views.list_floorplans, name='list_floorplans'),
    path('edit_floor_plan/<str:floor_plan_name>/', views.edit_floor_plan, name='edit_floor_plan'),
    path('save_floor_plan/<str:floor_plan_name>/', views.save_floor_plan, name='save_floor_plan'),
    path('get-floor-plan/<str:floor_plan_name>/', views.get_floor_plan, name='get_floor_plan_by_name'),
    path('floor-plan/<str:floor_plan_name>/', views.floor_plan_view, name='floor_plan_view'),
    path('remove-shape/<str:shape_id>/', views.remove_shape, name='remove_shape'),
    path('update-table/<int:table_id>/', views.update_table, name='update_table'),
]