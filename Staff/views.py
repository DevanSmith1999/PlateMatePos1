# views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import PositionForm, SubPositionForm, StaffForm
from .models import Position, SubPosition, Staff
from django.contrib.auth import logout
from django.urls import reverse

def create_position(request):
    if request.method == 'POST':
        form = SubPositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('position_list')
    else:
        form = SubPositionForm()

    parent_positions = Position.objects.all()#pylint: disable=no-member
    context = {
        'form': form,
        'parent_positions': parent_positions
    }
    return render(request, 'Positions/create_positions.html', context)

def position_list(request):
    positions = Position.objects.all() # pylint: disable=no-member
    return render(request, 'Positions/position_list.html', {'positions': positions})

def edit_position(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            return redirect('position_list')
    else:
        form = PositionForm(instance=position)
    return render(request, 'Positions/edit_position.html', {'form': form})

def confirm_delete_subposition(request, pk):
    subposition = get_object_or_404(SubPosition, pk=pk)
    if request.method == 'POST':
        # If the form is submitted via POST, delete the subposition
        subposition.delete()
        # Redirect the user to a success page or another appropriate page
        return redirect('subposition_list')  # Redirect to the positions list page
    return render(request, 'Positions/confirm_delete_subposition.html', {'subposition': subposition})

def delete_subposition(request, pk):
    subposition = get_object_or_404(SubPosition, pk=pk)
    if request.method == 'POST':
        subposition.delete()
        return redirect('subposition_list')  # Redirect to the subpositions list page
    return redirect('Positions/confirm_delete_subposition', pk=pk)  # Redirect to the confirmation page if GET request

# Views for Staff
def staff_list(request):
    subposition = SubPosition.objects.all()#pylint:disable=no-member
    return render(request, 'Staff/staff_list.html', {'subposition': subposition})

def get_staff(request):
    subposition_id = request.GET.get('subposition_id')
    staff = Staff.objects.filter(subposition__id=subposition_id)#pylint:disable=no-member
    staff_data = [{'id': staff.id, 'first_name': staff.first_name, 'last_name': staff.last_name} for staff in staff]
    return JsonResponse(staff_data, safe=False)

def staff_detail(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    return render(request, 'Staff/staff_detail.html', {'staff': staff})

def subpositions_list(request):
    subpositions=SubPosition.objects.all()# pylint: disable=no-member
    return render(request, 'Staff/subposition_list.html',{'subpositions': subpositions})

def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect(reverse('staff_detail', kwargs={'staff_id': staff.id})) 
    else:
        form = StaffForm(instance=staff)
    
    # Pre-fill the Date_of_birth field with the existing value
    form.fields['Date_of_birth'].initial = staff.Date_of_birth
    
    subposition = SubPosition.objects.all()  #pylint:disable=no-member
    context = {
        'form': form,
        'staff': staff,
        'subposition': subposition,
    }
    return render(request, 'Staff/staff_edit.html', context)

def check_id_number(request):
    if request.method == 'POST':
        id_number = request.POST.get('id_number')
        if Staff.objects.filter(id_number=id_number).exists():#pylint:disable=no-member
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def confirm_delete_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        # If the form is submitted via POST, delete the staff member
        staff.delete()
        # Redirect the user to a success page or another appropriate page
        return redirect('staff_list')  # Redirect to the staff list page
    return render(request, 'Staff/staff_delete_confirm.html', {'staff': staff})


def create_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data['id_number']
            if Staff.objects.filter(id_number=id_number).exists():#pylint:disable=no-member
                form.add_error('id_number', 'ID number already exists.')
            else:
                form.save()
                return redirect('staff_list')
            
    else:
        form = StaffForm()
    
    positions = Position.objects.all()#pylint: disable=no-member
    context = {
        'form': form,
        'positions': positions
    }
    return render(request, 'Staff/create_staff.html', context)


def get_subpositions(request):
    parent_position_id = request.GET.get('parent_position')
    if parent_position_id:
        subpositions = SubPosition.objects.filter(parent_position_id=parent_position_id).values('id', 'name')#pylint: disable=no-member
        return JsonResponse(list(subpositions), safe=False)
    else:
        return JsonResponse({'error': 'No parent position provided'}, status=400)

def logout_confirmation(request):
    return render(request, 'logout_confirmation.html')

def logout_user(request):
    logout(request)
    return redirect('login') 