from django.urls import path
from PlateMate import views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("Customer_Home/", views.Customer_Home, name = "Customer_Home"),
    path("Customer_About_Us/", views.Customer_About_Us, name = "About_Us"),
    path("Customer_Menu_Ordering/", views.Customer_Menu_Ordering, name = "Menu_Ordering"),
    path("Customer_Receipt_Check/", views.Customer_Receipt_Check, name = "Pay_Screen"),
    path("App_Menu/", views.App_Menu, name = "App_Menu"),
    path("Entree_Menu/", views.Entree_Menu, name = "Entree_Menu"),
    path("Kids_Sides_Menu/", views.Kids_Sides_Menu, name = "Kids_Sides_Menu"),
    path("Dessert_Menu/", views.Dessert_Menu, name = "Dessert_Menu"),
    path("Drink_Menu/", views.Drink_Menu, name = "Drink_Menu"),
    path("Server_Order_Screen/", views.Server_Order_Screen, name = "Server_Ordering"),
    path('server_delete_order_item/', views.server_delete_order_item, name='server_delete_order_item'),
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
    path('update-table/<int:table_number>/', views.update_table, name='update_table'),
    path('get-staff-subpositions/<int:staff_number>/', views.get_staff_subpositions, name='get_staff_subpositions'),
    path('get-staff-name/<int:staff_number>/', views.get_staff_name, name='get_staff_name'),
    path("Server_Table_View/", views.Server_Table_View, name = "Test Page"),
    path('create_order/', views.create_order, name='create_order'),
    path('delete_order_item/', views.delete_order_item, name='delete_order_item'),
    path('chat/', views.chat_view, name='chat')
]