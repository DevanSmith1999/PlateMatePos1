# models.py

from django.db import models

class Position(models.Model):
    POSITION_CHOICES = (
        ('FOH', 'FOH'),
        ('BOH', 'BOH'),
    )
    name = models.CharField(max_length=100, choices=POSITION_CHOICES)

    def __str__(self):
        return f"{self.name}"

class SubPosition(models.Model):
    name = models.CharField(max_length=100)
    parent_position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='subpositions')

    def __str__(self):
        return f"{self.name}"
    

class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Date_of_birth = models.DateField(null=True)
    id_number = models.CharField(max_length=20)
    subposition = models.ManyToManyField(SubPosition,null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"