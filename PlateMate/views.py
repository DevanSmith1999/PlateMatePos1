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
    context = {}
    table_id = 1 #Set table id here (1 for testing will need to be retrived from table user eventually)
    active_orders = []
    
    #handle the order button (Pushes order to Kitchen)
    if request.method == 'POST' and 'mark_ordered' in request.POST:
        ActiveOrder.objects.filter(TableID=table_id).update(Ordered=True)
        return render(request, 'PlateMate/Customer_Menu_Ordering.html', context)
    
    elif request.method == 'POST' and 'Add': #handle the add button
        try:
            menu_item_id = int(request.POST.get('MenuItemID'))
            table_id = int(request.POST.get('TableID'))

            # Retrieve Table object *may be source of error later - Remeber dealing with table object not table id value
            table = Table.objects.get(pk=table_id)
        
            # Check for existing order with same menu_item_id and TableID
            existing_order = ActiveOrder.objects.filter(MenuItemID=menu_item_id, TableID=table, Ordered = 0).first()  # Get the first matching order

            if existing_order:
                # Increment quantity of existing order
                existing_order.Quantity += 1
                existing_order.save()
            else:
                # Create new order if none exists
                new_order = ActiveOrder(MenuItemID=menu_item_id, TableID=table, Quantity=1)
                new_order.save()

            # After processing the form, retrieve active orders with data integrity check
            active_orders = []
            
            # Retrive all the data for displaying 
            total_price = 0
            for order in ActiveOrder.objects.filter(TableID=table_id, Ordered = 0):
                order.menu_item = MenuItem.objects.get(pk=order.MenuItemID)
                active_orders.append(order)
                total_price += order.menu_item.Price * order.Quantity #calc sum of all currently ordered items
            
            context['active_orders'] = active_orders
            context['total_price'] = total_price #sum of all ordered items
            

            return render(request, 'PlateMate/Customer_Menu_Ordering.html', context)
        except (ValueError, Exception) as e:
            print("ERRORRRRRRRRRR")
            # Handle various exceptions
            context['active_orders'] = []  # Set empty list for active orders
            return render(request, 'PlateMate/Customer_Menu_Ordering.html', context)
    else:  # GET request (initial page load)
        table_id = 1
        active_orders = []
        for order in ActiveOrder.objects.filter(TableID=table_id):
            order.menu_item = MenuItem.objects.get(pk=order.MenuItemID)
            active_orders.append(order)
        context['active_orders'] = active_orders

    
    
    return render(request, 'PlateMate/Customer_Menu_Ordering.html', context)



