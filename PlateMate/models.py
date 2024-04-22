import json
from django.db import models

# Create your models here.

class MenuItem(models.Model):
  Name = models.CharField( ("Name"), max_length=100)
  Type = models.CharField( ("type"), max_length=50)
  Description = models.TextField()
  Price = models.DecimalField(max_digits=5, decimal_places=2)

  def __str__(self):
    return str(self.pk)

class Table(models.Model):
    SHAPE_CHOICES = [
        ('circle', 'Circle'),
        ('rectangle', 'Rectangle'),
        ('square', 'Square'),
    ]

    floor_plan = models.ForeignKey('FloorPlan', related_name='tables', on_delete=models.CASCADE)
    shape = models.CharField(max_length=10, choices=SHAPE_CHOICES)
    x_position = models.IntegerField()
    y_position = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    table_number = models.IntegerField(primary_key=True,unique=True,default=1)  # Custom primary key
    isOccupiedBy = models.CharField(max_length=50, blank=True, null=True)  # Staff number or None

    def __str__(self):
        return f"{self.table_number} - {self.shape} - {self.floor_plan.name}"

class ActiveOrder(models.Model):
  MenuItemID = models.IntegerField()
  TableID = models.ForeignKey(Table,on_delete= models.CASCADE)
  Quantity = models.IntegerField()
  OrderTime = models.DateTimeField(auto_now_add = True)
  Ordered = models.BooleanField(default = False)
  completed = models.BooleanField(default = False)

  def __str__(self):
    return str(self.pk)

class OrderingHistory(models.Model):
  MenuItemID = models.ForeignKey(MenuItem,on_delete= models.CASCADE)
  OrderTime = models.DateTimeField()

  def __str__(self):
    return str(self.pk)

class FloorPlan(models.Model):
    name = models.CharField(max_length=255, default='')

    def __str__(self):
        return f"{self.name}"
    

    
class TextBox(models.Model):
    floor_plan = models.ForeignKey('FloorPlan', related_name='text_boxes', on_delete=models.CASCADE)
    x_position = models.IntegerField()
    y_position = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    content=models.CharField(max_length=255, default='')
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"TextBox - {self.floor_plan.name}"