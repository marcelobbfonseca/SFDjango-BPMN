from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.models import Group

class _GroupForm(ModelForm):

    class Meta:

        model = Group
        fields = ('name', 'permissions')

class _UserCreationForm(UserCreationForm):

    class Meta:
        
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'groups')
       

class _UserChangeForm(ModelForm):

    class Meta:

        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'groups')
