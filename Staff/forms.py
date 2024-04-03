# forms.py

from django import forms
from .models import Staff, Position

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'id_number', 'positions']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'parent_position']
