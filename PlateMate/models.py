from django.db import models

# Create your models here.

class MenuItem(models.Model):
  Name = models.CharField( ("Name"), max_length=100)
  Type = models.CharField( ("type"), max_length=50)
  Description = models.TextField()
  Price = models.DecimalField(max_digits=5, decimal_places=2)

  
