import json
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from PlateMate import models #Use this to access Menuitem data# Stuff
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from Staff import models as sm

from django.shortcuts import render, redirect
# from django.http import HttpResponse 
from .models import ActiveOrder, MenuItem, Table  #Use this to access Menuitem data

from django.http import JsonResponse
from .PlateMate_AI_1 import chat

 # Import all relevant models
# Stuff


def chat_view(request):
    user_query = request.GET.get('query', 'Default Query')  # Get the query parameter from URL
    response = chat(user_query)  # Call function
    return JsonResponse({'response': response})  # Return the response as JSON

def home(request):
    '''This is Plate Mate's home landing page'''
    return render(
        request,
        'PlateMate/Manager_home.html'
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

def App_Menu(request):
    '''Access appetizer menu items'''
    return render(
        request,
        'PlateMate/App_Menu.html'
    )

def Entree_Menu(request):
    '''Access entree menu items'''
    return render(
        request,
        'PlateMate/Entree_Menu.html'
    )
def Kids_Sides_Menu(request):
    '''Access kids and side menu items'''
    return render(
        request,
        'PlateMate/Kids_Sides_Menu.html'
    )

def Drink_Menu(request):
    '''Access drink menu items'''
    return render(
        request,
        'PlateMate/Drink_Menu.html'
    )

def Dessert_Menu(request):
    '''Access dessert menu items '''
    return render(
        request,
        'PlateMate/Dessert_Menu.html'
    )

def Customer_Receipt_Check(request):
    '''See all items ordered; Price and order total'''
    return render(
        request,
        'PlateMate/Customer_Receipt_Check.html'
    )

def Server_Order_Screen(request):
    context = {}
    table_id = 1 #Set table id here (1 for testing will need to be retrived from table user eventually)
    active_orders = []
    
    #handle the order button (Pushes order to Kitchen)
    if request.method == 'POST' and 'mark_ordered' in request.POST:
        print("order button pressed")
        ActiveOrder.objects.filter(TableID=table_id).update(Ordered=True)#pylint:disable=no-member
        return render(request, 'PlateMate/Server_Order_Screen.html', context)
        
    
    elif request.method == 'POST' and 'Add': #handle the add button
        try:
            menu_item_id = int(request.POST.get('MenuItemID'))
            table_id = int(request.POST.get('TableID'))                             #*****Currenrly getting table id from form to be updated with table user id!
            
            # Retrieve Table object *may be source of error later - Remeber dealing with table object not table id value
            table = Table.objects.get(pk=table_id)#pylint:disable=no-member
            
            # Check for existing order with same menu_item_id and TableID
            existing_order = ActiveOrder.objects.filter(MenuItemID=menu_item_id, TableID=table, Ordered = 0).first()#pylint:disable=no-member  # Get the first matching order
            
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
            for order in ActiveOrder.objects.filter(TableID=table_id):#pylint:disable=no-member
                order.menu_item = MenuItem.objects.get(pk=order.MenuItemID)#pylint:disable=no-member
                active_orders.append(order)
                total_price += order.menu_item.Price * order.Quantity #calc sum of all currently ordered items
            
            context['active_orders'] = active_orders
            context['total_price'] = total_price #sum of all ordered items
            

            return render(request, 'PlateMate/Server_Order_Screen.html', context)
        except (ValueError, Exception) as e:
            print(e)
            # Handle various exceptions
            context['active_orders'] = []  # Set empty list for active orders
            return render(request, 'PlateMate/Server_Order_Screen.html', context)
    else:  # GET request (initial page load)
        table_id = 1
        active_orders = []
        for order in ActiveOrder.objects.filter(TableID=table_id):#pylint:disable=no-member
            order.menu_item = MenuItem.objects.get(pk=order.MenuItemID)#pylint:disable=no-member
            active_orders.append(order)
        context['active_orders'] = active_orders
    return render(request, 'PlateMate/Server_Order_Screen.html', context)

def server_delete_order_item(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = ActiveOrder.objects.get(pk=order_id)#pylint:disable=no-member
            if order.Quantity > 1:
                order.Quantity -= 1
                order.save()
            else:
                order.delete()

            # Recalculate total price for all active orders after deletion/modification
            active_orders = ActiveOrder.objects.filter(TableID=1)#pylint:disable=no-member  # Assuming table_id
            total_price = 0
            for order in active_orders:
                order.menu_item = MenuItem.objects.get(pk=order.MenuItemID)#pylint:disable=no-member
                total_price += order.menu_item.Price * order.Quantity
            tax = float(total_price) * 0.0445
            totalandtax = f"{float(total_price) + tax:.2f}"
            tax = f"{tax:.2f}"
            
            # Update context with the new total price
            context = {'active_orders': active_orders, 'total_price': total_price,'tax': tax, 'totalandtax': totalandtax}
            return render(request, 'PlateMate/Server_Order_Screen.html', context)

        except (ActiveOrder.DoesNotExist, ValueError):#pylint:disable=no-member
            # Handle errors
            pass
    return redirect('create_order')  # Redirect back even on GET requests (optional)

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

def floorplan_view(request):
    return render(request, 'PlateMate/floor_plan.html')


def save_floor_plan(request, floor_plan_name):
    if request.method == 'POST':
        # Get the tables and textboxes from the POST request
        tables_json = request.POST.get('table', '')
        textboxes_json = request.POST.get('textbox', '')

        try:
            # Get existing floor plan by name
            floor_plan = models.FloorPlan.objects.get(name=floor_plan_name)#pylint:disable=no-member
            
            print(f"Received floor plan name: {floor_plan_name}")
            print(f"Received tables data: {tables_json}")
            print(f"Received text boxes data: {textboxes_json}")

            # Delete existing tables and text boxes associated with the floor plan
            deleted_tables = models.Table.objects.filter(floor_plan=floor_plan).delete()[0]#pylint:disable=no-member
            deleted_textboxes = models.TextBox.objects.filter(floor_plan=floor_plan).delete()[0]#pylint:disable=no-member

            print(f"Deleted {deleted_tables} tables and {deleted_textboxes} text boxes")

            # Convert JSON string to Python list
            tables_data = json.loads(tables_json)
            textboxes_data = json.loads(textboxes_json)

            # Create tables for the floor plan
            for table_data in tables_data:
                table = models.Table(
                    floor_plan=floor_plan,
                    shape=table_data['shape'],
                    x_position=table_data['x_position'],
                    y_position=table_data['y_position'],
                    width=table_data['width'],
                    height=table_data['height'],
                    table_number=table_data.get('table_number', 1)

                )
                table.save()

            # Create text boxes for the floor plan
            for text_data in textboxes_data:
                textbox = models.TextBox(
                    floor_plan=floor_plan,
                    x_position=text_data['x_position'],
                    y_position=text_data['y_position'],
                    width=text_data['width'],
                    height=text_data['height'],
                    content=text_data.get('content', ''),
                    id=text_data.get('id')
                )
                textbox.save()

            return JsonResponse({'status': 'success', 'message': 'Floor plan updated successfully!'})

        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Floor plan does not exist.'})

        except Exception as e:
            # Handle any exceptions that occur during saving
            return JsonResponse({'status': 'error', 'message': f'Error updating floor plan: {e}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
def get_floor_plan(request, floor_plan_name):
    try:
        floor_plan = get_object_or_404(models.FloorPlan, name=floor_plan_name)
        
        tables = models.Table.objects.filter(floor_plan=floor_plan)#pylint:disable=no-member
        text_boxes = models.TextBox.objects.filter(floor_plan=floor_plan)#pylint:disable=no-member

        tables_data = [
            {
                'table_number': table.table_number,
                'shape': table.shape,
                'x_position': table.x_position,
                'y_position': table.y_position,
                'width': table.width,
                'height': table.height,
                'isOccupiedBy': table.isOccupiedBy
            }
            for table in tables
        ]

        textboxes_data = [
            {
                'x_position': textbox.x_position,
                'y_position': textbox.y_position,
                'width': textbox.width,
                'height': textbox.height,
                'content': textbox.content,
                'id':textbox.id
            }
            for textbox in text_boxes
        ]

        return JsonResponse({
            'tables': tables_data,
            'textboxes': textboxes_data
        })
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Floor plan not found'}, status=404)

def floor_plan_view(request, floor_plan_name):
    try:
        floor_plan = get_object_or_404(models.FloorPlan, name=floor_plan_name)
        
        tables = models.Table.objects.filter(floor_plan=floor_plan)#pylint:disable=no-member
        textboxes = models.TextBox.objects.filter(floor_plan=floor_plan)#pylint:disable=no-member

        tables_data = [
            {
                'table_number': table.table_number,
                'shape': table.shape,
                'x_position': table.x_position,
                'y_position': table.y_position,
                'width': table.width,
                'height': table.height,
                'isOccupiedBy': table.isOccupiedBy
            }
            for table in tables
        ]

        textboxes_data = [
            {
                'x_position': textbox.x_position,
                'y_position': textbox.y_position,
                'width': textbox.width,
                'height': textbox.height,
                'content': textbox.content,
                'id':textbox.id
                
            }
            for textbox in textboxes
        ]

        context = {
            'floor_plan_name': floor_plan_name,
            'tables': tables_data,
            'textboxes': textboxes_data
        }
        
        return render(request, 'PlateMate/MainDining.html', context)
    
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Floor plan not found'}, status=404)
def edit_floor_plan(request, floor_plan_name):
    try:
        floorplan = models.FloorPlan.objects.get(name=floor_plan_name)#pylint:disable=no-member
        
        if request.method == 'POST':
            # Handle form submission to save changes to the floor plan
            # ...

           
            return redirect('list_floor_plans')

        tables = models.Table.objects.filter(floor_plan=floorplan)#pylint:disable=no-member
        textboxes = models.TextBox.objects.filter(floor_plan=floorplan)#pylint:disable=no-member

        tables_data = [
            {
                'table_number': table.table_number,
                'shape': table.shape,
                'x_position': table.x_position,
                'y_position': table.y_position,
                'width': table.width,
                'height': table.height,
            }
            for table in tables
        ]

        textboxes_data = [
            {
                'x_position': textbox.x_position,
                'y_position': textbox.y_position,
                'width': textbox.width,
                'height': textbox.height,
                'content': textbox.content,
                'id': textbox.id,
            }
            for textbox in textboxes
        ]

        context = {
            'floorplan': floorplan,
            'tables': tables_data,
            'textboxes': textboxes_data,
        }
        
        return render(request, 'PlateMate/Edit_Floor_Plan.html', context)
    
    except ObjectDoesNotExist:
        
        return redirect('list_floor_plans')

def remove_shape(request, shape_id):
    try:
        # Extract the integer ID from the shape_id
        try:
            shape_id_int = int(shape_id.split('-')[1])
        except ValueError:
            return JsonResponse({'error': 'Invalid shape ID format'}, status=400)

        # Try to delete a Table with the given table_number
        print(f"Here is the shapeID{shape_id}")
        if shape_id.startswith('table'):
            deleted_count, _ = models.Table.objects.filter(table_number=shape_id_int).delete()#pylint:disable=no-member
            print(f"Delete query for Table with table_number {shape_id_int}: {models.Table.objects.filter(table_number=shape_id_int).query}")#pylint:disable=no-member
            if deleted_count != 0:
                print(f"Deleted {deleted_count} table(s) with table_number: {shape_id_int}")
                return JsonResponse({'message': 'Table removed successfully'}, status=200)
            else:
                print(f"Table with table_number: {shape_id_int} not found")
                return JsonResponse({'error': 'Table not found'}, status=404)
        
        # Try to delete a TextBox with the given id
        elif not shape_id.startswith('table'):
            deleted_count, _ = models.TextBox.objects.filter(id=shape_id_int).delete()#pylint:disable=no-member
            print(f"Delete query for TextBox with id {shape_id_int}: {models.TextBox.objects.filter(id=shape_id_int).query}") #pylint:disable=no-member
            if deleted_count != 0:
                print(f"Deleted {deleted_count} textbox with id: {shape_id_int}")
                return JsonResponse({'message': 'TextBox removed successfully'}, status=200)
            else:
                print(f"TextBox with id: {shape_id_int} not found")
                return JsonResponse({'error': 'TextBox not found'}, status=404)

        # If neither Table nor TextBox is found
        else:
            return JsonResponse({'error': 'Shape not found'}, status=404)

    except Exception as e:
        print(f"Error in remove_shape view: {e}")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
def list_floorplans(request):
    # Fetch all floor plans from the database
    floorplan = models.FloorPlan.objects.all()#pylint:disable=no-member
    print("Rendering the list of floor plans.")

    context = {
        'floorplan': floorplan
    }

    return render(request, 'PlateMate/floorplan_list.html', context)
@require_http_methods(["PUT"])
def update_table(request, table_number):
    print("Received table ID:", table_number)
    data = request.body.decode('utf-8')
    print("Received data:", data)
    table_data = json.loads(data)
    
    table = get_object_or_404(models.Table, table_number=table_number)
    
    # Update the table's isOccupiedBy field
    table.isOccupiedBy = table_data.get('isOccupiedBy', None)
    table.save()
    
    return JsonResponse({'status': 'success', 'message': 'Table updated successfully'}, status=200)
def get_staff_subpositions(request, staff_number):
    try:
        print(staff_number)
        staff = sm.Staff.objects.get(id_number=staff_number)#pylint:disable=no-member
        subposition_ids = [subposition.id for subposition in staff.subposition.all()]
        print(subposition_ids)
        return JsonResponse(subposition_ids, safe=False)

    except sm.Staff.DoesNotExist:#pylint:disable=no-member
        return JsonResponse({"error": "Staff not found"}, status=404)
def get_staff_name(request, staff_number):
    try:
        staff = sm.Staff.objects.get(id_number=staff_number)#pylint:disable=no-member
        first_name = staff.first_name
        print(first_name)
        return JsonResponse({'first_name': first_name})
    except sm.Staff.DoesNotExist:#pylint:disable=no-member
        return JsonResponse({'error': 'Staff member not found'}, status=404)

        
def create_order(request):
    print("hellow there")
    context = {}
    table_id = 1 #Set table id here (1 for testing will need to be retrived from table user eventually)
    active_orders = []
    
    #handle the order button (Pushes order to Kitchen)
    if request.method == 'POST' and 'mark_ordered' in request.POST:
        print("order button pressed")
        ActiveOrder.objects.filter(TableID=table_id).update(Ordered=True)#pylint:disable=no-member
        return render(request, 'PlateMate/Customer_Menu_Ordering.html', context)
        
    
    elif request.method == 'POST' and 'Add': #handle the add button
        try:
            menu_item_id = int(request.POST.get('MenuItemID'))
            table_id = int(request.POST.get('TableID'))                             #*****Currenrly getting table id from form to be updated with table user id!
            
            # Retrieve Table object *may be source of error later - Remeber dealing with table object not table id value
            table = Table.objects.get(pk=table_id)#pylint:disable=no-member
            
            # Check for existing order with same menu_item_id and TableID
            existing_order = ActiveOrder.objects.filter(MenuItemID=menu_item_id, TableID=table, Ordered = 0).first()#pylint:disable=no-member  # Get the first matching order
            
            if existing_order:
                # Increment quantity of existing order
                existing_order.Quantity += 1
                existing_order.save()
            else:
                # Create new order if none exists
                new_order = ActiveOrder(MenuItemID=menu_item_id, TableID=table, Quantity=1)
                print("did we get here3")
                new_order.save()  
                print("did we get here4")  

            # After processing the form, retrieve active orders with data integrity check
            active_orders = []
            
            # Retrive all the data for displaying 
            total_price = 0
            for order in ActiveOrder.objects.filter(TableID=table_id, Ordered = 0):#pylint:disable=no-member
                order.menu_item = MenuItem.objects.get(pk=order.MenuItemID)#pylint:disable=no-member
                active_orders.append(order)
                total_price += order.menu_item.Price * order.Quantity #calc sum of all currently ordered items
            
            context['active_orders'] = active_orders
            context['total_price'] = total_price #sum of all ordered items
            

            return render(request, 'PlateMate/Customer_Menu_Ordering.html', context)
        except (ValueError, Exception) as e:
            print(e)
            # Handle various exceptions
            context['active_orders'] = []  # Set empty list for active orders
            return render(request, 'PlateMate/Customer_Menu_Ordering.html', context)
    else:  # GET request (initial page load)
        table_id = 1
        active_orders = []
        for order in ActiveOrder.objects.filter(TableID=table_id):#pylint:disable=no-member
            order.menu_item = MenuItem.objects.get(pk=order.MenuItemID)#pylint:disable=no-member
            active_orders.append(order)
        context['active_orders'] = active_orders

    return render(request, 'PlateMate/Customer_Menu_Ordering.html', context)

def delete_order_item(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = ActiveOrder.objects.get(pk=order_id)#pylint:disable=no-member
            if order.Quantity > 1:
                order.Quantity -= 1
                order.save()
            else:
                order.delete()

            # Recalculate total price for all active orders after deletion/modification
            active_orders = ActiveOrder.objects.filter(TableID=1, Ordered = 0)#pylint:disable=no-member  # Assuming table_id
            total_price = 0
            for order in active_orders:
                order.menu_item = MenuItem.objects.get(pk=order.MenuItemID)#pylint:disable=no-member
                total_price += order.menu_item.Price * order.Quantity

            # Update context with the new total price
            context = {'active_orders': active_orders, 'total_price': total_price}
            return render(request, 'PlateMate/Customer_Menu_Ordering.html', context)

        except (ActiveOrder.DoesNotExist, ValueError):#pylint:disable=no-member
            # Handle errors
            pass
    return redirect('create_order')  # Redirect back even on GET requests (optional)

