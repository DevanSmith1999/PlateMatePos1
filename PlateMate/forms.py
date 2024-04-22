from django import forms
from .models import Table

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['floor_plan', 'shape', 'x_position', 'y_position', 'width', 'height', 'table_number']

    def clean_table_number(self):
        table_number = self.cleaned_data['table_number']
        
        # Check if table_number is unique
        if Table.objects.filter(table_number=table_number).exists():#pylint:disable=no-member
            raise forms.ValidationError("Table number already exists.")
        
        return table_number
