from django.urls import path
from PlateMate import views
from users import views as userviews 

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
    path("Kitchen_Current_Orders/", views.Kitchen_Current_Orders, name = "Test Page"),
    path("Manager_Checks/", views.Manager_Checks, name = "Test Page"),
    path("Manager_Stats/", views.Manager_Stats, name = "Test Page"),
    path("Manager_Table_Assignment/", views.Manager_Table_Assignment, name = "Test Page"),
    path("Server_Check_View/", views.Server_Check_View, name = "Test Page"),
    path("Server_Pin_Log_in/", views.Server_Pin_Log_in, name = "Test Page"),
    path("Server_Table_View/", views.Server_Table_View, name = "Test Page"),
    path('create_order/', views.create_order, name='create_order'),
    path('delete_order_item/', views.delete_order_item, name='delete_order_item')
]