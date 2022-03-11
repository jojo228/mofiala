from django import forms
from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm, widgets
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



IDENTITE = [

        ('Particulier', 'Particulier'),
        ('Professionel', 'Professionel')
    ]

CHOIX = [
        ('Oui', 'Oui'),
        ('Non', 'Non')
    ]



class FormeUser(forms.ModelForm):

    password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    passwordCheck=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    class Meta:
        model=User
        fields=('first_name','last_name','password')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }  

    def clean(self):
        cleaned_data = super(FormeUser, self).clean()
        password = cleaned_data.get("password")
        passwordCheck = cleaned_data.get("passwordCheck")

        if password != passwordCheck:
            raise forms.ValidationError(
                "password and passwordCheck does not match"
            )


class AgenceForm(ModelForm):
    class Meta:
        model = Agence
        exclude = ('user',)
        

        widgets = {
            'nom_agence': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }



class ContribuableForm(ModelForm):

    
    class Meta:
        model = Contribuable
        fields = '__all__'


       

class AuthenticationFormWithContact(forms.Form):
    contact = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)


    def clean(self):
        contact = self.cleaned_data.get('contact')
        password = self.cleaned_data.get('password')
        
        if contact and password:
            self.user_cache = authenticate(self.request, contact=contact, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Contact ou mot de passe invalide")
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError("inactive user")

    def get_user(self):
        return self.user_cache