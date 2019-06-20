from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, Schedule, Visitor
from django.core.exceptions import ValidationError


def file_size(value):  # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2'
                  ]


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class UpdateProfileFormNotVerified(forms.ModelForm):
    photo = forms.FileField(required=False, validators=[file_size])

    class Meta:
        model = Profile
        exclude = ['user', 'verified']


class UpdateProfileFormVerified(forms.ModelForm):
    photo = forms.FileField(required=False, validators=[file_size])

    class Meta:
        model = Profile
        exclude = ['user', 'verified', 'category', 'designation', 'date_of_birth', 'gender']


class UpdateScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        exclude = ['approve']


class UpdateVisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        exclude = ['photo']