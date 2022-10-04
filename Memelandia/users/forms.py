from django import forms

from django.contrib.auth.models import User
from .models import Profile


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(required=False,widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    is_private = forms.BooleanField(required=False,widget=forms.RadioSelect(choices=((False, 'False'), (True, 'True'))))

    class Meta:
        model = Profile
        fields = ['avatar', 'is_private', 'bio']
