from django.shortcuts import render, redirect
# from django.http import HttpResponse 
from .models import ActiveOrder, MenuItem, Table  #Use this to access Menuitem data

 # Import all relevant models
# Stuff


def home(request):
    '''This is Plate Mate's home landing page'''
    return render(
        request,
        'PlateMate/home.html'
    )

def Customer_Home(request):
    '''Landing Page for Table To reset after server closes table.'''
    return render(
        request,
        'PlateMate/Customer_Home.html'
    )

def Customer_About_Us(request):
    '''Access to information about the resturant'''
    return render(
        request,
        'PlateMate/Customer_About_Us.html'
    )

def Customer_Menu_Ordering(request):
    '''Access menu with all restaurant orders and be able to add items to a check/order'''
    return render(
        request,
        'PlateMate/Customer_Menu_Ordering.html'
    )

def Customer_App_Ordering(request):
    '''Access appetizer menu items and be able to add items to a check/order'''
    return render(
        request,
        'PlateMate/Customer_App_Ordering.html'
    )

def Customer_Entree_Ordering(request):
    '''Access entree menu items and be able to add items to a check/order'''
    return render(
        request,
        'PlateMate/Customer_Entree_Ordering.html'
    )
def Customer_Kids_Sides_Ordering(request):
    '''Access kids and side menu items and be able to add items to a check/order'''
    return render(
        request,
        'PlateMate/Customer_Kids_Sides_Ordering.html'
    )

def Customer_Drinks_Ordering(request):
    '''Access drink menu items and be able to add items to a check/order'''
    return render(
        request,
        'PlateMate/Customer_Drinks_Ordering.html'
    )

def Customer_Dessert_Ordering(request):
    '''Access dessert menu items and be able to add items to a check/order'''
    return render(
        request,
        'PlateMate/Customer_Dessert_Ordering.html'
    )

def Customer_Receipt_Check(request):
    '''See all items ordered; Price and order total'''
    return render(
        request,
        'PlateMate/Customer_Receipt_Check.html'
    )

def Kitchen_Current_Orders(request):
    '''View current orders from all tables'''
    return render(
        request,
        'PlateMate/Kitchen_Current_Orders.html'
    )

def Manager_Checks(request):
    '''View all currently open checks'''
    return render(
        request,
        'PlateMate/Manager_Checks.html'
    )

def Manager_Stats(request):
    '''Page of restaurant  stats'''
    return render(
        request,
        'PlateMate/Manager_Stats.html'
    )

def Manager_Table_Assignment(request):
    '''Page to Assign servers to  tables'''
    return render(
        request,
        'PlateMate/Manager_Table_Assignment.html'
    )

def Server_Check_View(request):
    '''Page for servers to see their table's open checks and items ordered'''
    return render(
        request,
        'PlateMate/Server_Check_View.html'
    )

def Server_Pin_Log_in(request):
    '''a log in page for servers to use a pin to access other server pages'''
    return render(
        request,
        'PlateMate/Server_Pin_Log_in.html'
    )

def Server_Table_View(request):
    '''A map of tables for servers to be able to select a table a view their ticket'''
    return render(
        request,
        'PlateMate/Server_Table_View.html'
    )


def create_order(request):
  print("Testing print")
  if request.method == 'POST':
    try:
      menu_item_id = int(request.POST.get('MenuItemID'))
      table_id = int(request.POST.get('TableID'))

      # Retrieve MenuItem object and Table object
      menu_item = MenuItem.objects.get(pk=menu_item_id)
      table = Table.objects.get(pk=table_id)

      # Check for existing order with same MenuItemID and TableID
      existing_order = ActiveOrder.objects.filter(MenuItemID=menu_item, TableID=table).first()  # Get the first matching order
      if existing_order:
        # Increment quantity of existing order
        existing_order.Quantity += 1
        existing_order.save()
        return render(request, 'PlateMate/Customer_Menu_Ordering.html') 
      else:
        # Create new order if none exists
        new_order = ActiveOrder(MenuItemID=menu_item, TableID=table, Quantity=1)
        new_order.save()
        return render(request, 'PlateMate/Customer_Menu_Ordering.html')  
    except (ValueError, Exception) as e:
      # Handle various exceptions
      return render(request, 'PlateMate/Customer_Menu_Ordering.html')