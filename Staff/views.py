# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import StaffForm, PositionForm
from .models import Staff, Position


def create_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')  # Redirect to staff list page
    else:
        form = StaffForm()
    return render(request, 'create_staff.html', {'form': form})

def create_position(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('position_list')  # Redirect to position list page
    else:
        form = PositionForm()
    return render(request, 'create_position.html', {'form': form})
def staff_list(request):
    staff = Staff.objects.all()
    return render(request, 'staff_list.html', {'staff': staff})

def staff_delete(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.delete()
        return redirect('staff_list')
    return render(request, 'staff_delete_confirm.html', {'staff': staff})

def position_list(request):
    positions = Position.objects.all()
    return render(request, 'position_list.html', {'positions': positions})

def position_delete(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        position.delete()
        return redirect('position_list')
    return render(request, 'position_delete_confirm.html', {'position': position})
