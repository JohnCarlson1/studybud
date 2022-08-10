from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

def home(request):
    rooms = Room.objects.all() #objects is used to query database table
    context = {'rooms': rooms} # key is variable used in for loop, pair is list
    return render(request, 'baseApp/home.html', context) # passing context in makes it available in home.html

def room(request, pk):

    room = Room.objects.get(id=pk)
    context = {'room':room}

    return render(request, 'baseApp/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST) #passes all values into the form
        if form.is_valid(): #checks that everything is valid (types)
            form.save() #saves to model
            return redirect('home')
    context = {'form':form}
    return render(request, 'baseApp/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save
            return redirect('home')

    context = {'form':form}
    return render(request, 'baseApp/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'baseApp/delete.html', {'obj':room})
