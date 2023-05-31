from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

from core import models


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(min_length=3, max_length=50)
    last_name = forms.CharField(min_length=3, max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['username'].label = 'Логин'

        self.fields['first_name'].widget.attrs.update({'placeholder': 'Имя пользователя', 'autofocus': 'autofocus'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Фамилия пользователя'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Логин', 'autofocus': False})
        self.fields['email'].widget.attrs.update({'placeholder': 'Почта'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Повторите пароль'})
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_username(self):
        login = self.cleaned_data.get('username')
        if len(login) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return login


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'

        self.fields['username'].widget.attrs.update({'class': 'form-control',
                                                    'placeholder': 'Логин'})
        self.fields['password'].widget.attrs.update({'class': 'form-control',
                                                     'placeholder': 'Пароль'})


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(min_length=3, max_length=50)
    last_name = forms.CharField(min_length=3, max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')


class UpdateProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].label = "Аватар"
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = models.Profile
        fields = ('slug', 'bio', 'date_birthday', 'avatar')

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if len(bio) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return bio


#class SearchProfileForm(Form):
    #profile_name = CharField(label="Поиск по ")