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