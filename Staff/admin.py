from django.contrib import admin
from .models import Position, Staff,SubPosition

# Register your models here.
admin.site.register(Position)
admin.site.register(Staff)
admin.site.register(SubPosition)