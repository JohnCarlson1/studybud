from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' #creates form based on all fields in room model
        exclude = ['host', 'participants']