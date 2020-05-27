from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import (Profile,File_uploaded)
from latinoMusic_app.models import (Subscribers,Song,Genre)


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=100, help_text='First Name')
    # last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

class Profile_InfoForm(ModelForm):
    class Meta:
        model = Profile
        exclude =['user','signup_confirmation']
        
class EmailSubscriptionForm(ModelForm):
    class Meta:
        model = Subscribers
        fields ='__all__'         
        
class File_UploadForm(ModelForm):
    
    class Meta:
        model = File_uploaded
        fields = '__all__'

class UploadSongsForm(ModelForm):
    class Meta:
        model = Song
        fields = '__all__'
class AddGenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'
        
#subscription form

subscription_options =[
    ('free','Free for 1-Month ($0 USD/Mon)'),
    ('standard','Standard at($10 USD/Mon)'),
    ('premium','Premium  at($20 USD/Mon)'),    
] 

class SubscriptionForm(forms.Form):
    plans = forms.ChoiceField(choices=subscription_options)
          