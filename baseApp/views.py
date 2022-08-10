from django.shortcuts import render
from .models import Room

def home(request):
    rooms = Room.objects.all() #objects is used to query database table
    context = {'rooms': rooms} # key is variable used in for loop, pair is list
    return render(request, 'baseApp/home.html', context) # passing context in makes it available in home.html

def room(request, pk):
    
    room = Room.objects.get(id=pk)
    context = {'room':room}

    return render(request, 'baseApp/room.html', context)
