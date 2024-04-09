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
  ServerID = models.IntegerField(default = 1)

  def __str__(self):
    return str(self.pk)

class ActiveOrder(models.Model):
  MenuItemID = models.ForeignKey(MenuItem,on_delete= models.CASCADE)
  TableID = models.ForeignKey(Table,on_delete= models.CASCADE)
  Quantity = models.IntegerField()
  OrderTime = models.DateTimeField(auto_now_add = True)
  completed = models.BooleanField(default = False)

  def __str__(self):
    return str(self.pk)

class OrderingHistory(models.Model):
  MenuItemID = models.ForeignKey(MenuItem,on_delete= models.CASCADE)
  OrderTime = models.DateTimeField()

  def __str__(self):
    return str(self.pk)

