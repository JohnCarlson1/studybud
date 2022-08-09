from django.shortcuts import render

rooms = [
    {'id':1, 'name':'Lets learn python!'},
    {'id':2, 'name':'Design with me!'},
    {'id':3, 'name':'Frontend Developer'},
]

def home(request):
    context = {'rooms': rooms} # key is variable used in for loop, pair is list
    return render(request, 'baseApp/home.html', context) # passing context in makes it available in home.html

def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    
    context = {'room':room}

    return render(request, 'baseApp/room.html', context)
