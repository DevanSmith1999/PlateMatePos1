from django.shortcuts import render

from django.http import HttpResponse
from PlateMate.models import MenuItem #Use this to access Menuitem data
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

def Customer_Menu_Ordering(request):
    '''Access menu with all restaurant orders and be able to add items to a check/order'''
    return render(
        request,
        'PlateMate/Customer_Menu_Ordering.html'
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