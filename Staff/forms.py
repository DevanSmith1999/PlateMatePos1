# forms.py

from django import forms
from .models import Staff, Position,SubPosition

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']

class SubPositionForm(forms.ModelForm):
    parent_position = forms.ModelChoiceField(queryset=None, empty_label="-- Select Parent Position --")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent_position'].queryset = Position.objects.all()#pylint:disable=no-member

    class Meta:
        model = SubPosition
        fields = ['name', 'parent_position']


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'Date_of_birth', 'id_number', 'subposition']
        widgets = {
            'Date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subposition'].queryset = SubPosition.objects.all()#pylint:disable=no-member
