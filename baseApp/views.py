from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm

def loginPage(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        #check if user exists
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        #authenticate user
        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page':page}
    return render(request, 'baseApp/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # commit = False freezes data so we can clean up below
            user.username = user.username.lower() #make all username letters lowercase
            user.save
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    return render(request, 'baseApp/login_register.html', {'form':form})

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
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) #filter activity feed based on search function on topics

    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_messages':room_messages} # key is variable used in for loop, pair is list
    return render(request, 'baseApp/home.html', context) # passing context in makes it available in home.html

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created') #message_set.all grabs the set of messages related to this specific room
    participants = room.participants.all() #for many to many
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body') #value passed in from room input
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'baseApp/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'room_messages': room_messages, 'topics':topics}
    return render(request, 'baseApp/profile.html', context)

@login_required(login_url='login') #prohibits access to createroom if not a user, redirects to login page if not user
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST) #passes all values into the form
        if form.is_valid(): #checks that everything is valid (types)
            form.save() #saves to model
            return redirect('home')
    context = {'form':form}
    return render(request, 'baseApp/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save
            return redirect('home')

    context = {'form':form}
    return render(request, 'baseApp/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'baseApp/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'baseApp/delete.html', {'obj':message})
