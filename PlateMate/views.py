from django.shortcuts import render

from django.http import HttpResponse

# Stuff
def home(request):
    return HttpResponse('<h1>Plate Mate!</h1>')
