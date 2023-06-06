import datetime

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
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)

    def clean_username(self):
        login = self.cleaned_data.get('username')
        if len(login) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return login

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return last_name


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
        fields = ('first_name', 'last_name', 'email',)


class UpdateProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].label = 'Аватар'
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = models.Profile
        fields = ('slug', 'bio', 'date_birthday', 'avatar')

    def clean_date_birthday(self):
        date_birthday = self.cleaned_data.get('date_birthday')
        end_date = datetime.date(1923, 12, 31)
        if date_birthday:
            if date_birthday > datetime.datetime.now().date():
                raise ValidationError('Дата не должна превышать текущую')
            elif date_birthday < end_date:
                raise ValidationError(f'Дата не должна быть меньше {end_date}')
        return date_birthday

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if len(bio) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return bio

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return last_name


class SearchUserForm(forms.Form):
    user_name = forms.CharField(label='Поиск по имени', required=False)
    user_name.widget.attrs.update({'class': 'form-control me-2', 'placeholder': 'Поиск',
                                      'type': 'search', 'aria-label': 'Search'})
