# models.py

from django.db import models

class Position(models.Model):
    name = models.CharField(max_length=100)
    parent_position = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subpositions')

    def __str__(self):
        return f"{self.name}"
    
class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=4, unique=True)  # Assuming last four digits of SSN
    positions = models.ManyToManyField('Position', related_name='staff')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

