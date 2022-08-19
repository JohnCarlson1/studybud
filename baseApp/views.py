from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

def home(request):

    #for search functionality on home page
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    #objects is used to query Room model, filter filters to rooms where topic name contains (i requires
    #allows lowercase) q which is the get request
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__contains=q)
        ) #objects is used to query database table, Q is imported from db.models, allows searching by multiple parameters

    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count} # key is variable used in for loop, pair is list
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
