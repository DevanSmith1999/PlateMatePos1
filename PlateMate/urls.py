from django.urls import path
from PlateMate import views

urlpatterns = [
    path("", views.home, name="home"),
    path("Customer_Home/", views.Customer_Home, name = "Test Page"),
    path("Customer_About_Us/", views.Customer_About_Us, name = "Test Page"),
    path("Customer_Menu_Ordering/", views.Customer_Menu_Ordering, name = "ordering"),
    path("Customer_App_Ordering/", views.Customer_App_Ordering, name = "Test Page"),
    path("Customer_Entree_Ordering/", views.Customer_Entree_Ordering, name = "Test Page"),
    path("Customer_Kids_Sides_Ordering/", views.Customer_Kids_Sides_Ordering, name = "Test Page"),
    path("Customer_Drinks_Ordering/", views.Customer_Drinks_Ordering, name = "Test Page"),
    path("Customer_Dessert_Ordering/", views.Customer_Dessert_Ordering, name = "Test Page"),
    path("Customer_Receipt_Check/", views.Customer_Receipt_Check, name = "Test Page"),
    path("Kitchen_Current_Orders/", views.Kitchen_Current_Orders, name = "Test Page"),
    path("Manager_Checks/", views.Manager_Checks, name = "Test Page"),
    path("Manager_Stats/", views.Manager_Stats, name = "Test Page"),
    path("Manager_Table_Assignment/", views.Manager_Table_Assignment, name = "Test Page"),
    path("Server_Check_View/", views.Server_Check_View, name = "Test Page"),
    path("Server_Pin_Log_in/", views.Server_Pin_Log_in, name = "Test Page"),
    path("Server_Table_View/", views.Server_Table_View, name = "Test Page"),
    path('create_order/', views.create_order, name='create_order')
]