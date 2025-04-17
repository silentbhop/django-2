from .models import Book, CustomUser
from django.forms import ModelForm, TextInput, NumberInput, PasswordInput, EmailInput, CharField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-container',
                'placeholder': 'Название книги'
                }),
            'author': TextInput(attrs={
                'class': 'form-container',
                'placeholder': 'Автор'
                }),
            'price': NumberInput(attrs={
                'class': 'form-container',
                'placeholder': 'Цена',
                'step': '0.01'
                }),
        }

class CustomUserCreationForm(UserCreationForm):
    password1 = CharField(
        widget= PasswordInput(attrs={'class': 'form-container', 'placeholder': 'Пароль'})
    )
    password2 =  CharField(
        widget= PasswordInput(attrs={'class': 'form-container', 'placeholder': 'Повторите пароль'})
    )  
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-container',
                'placeholder': 'Имя пользователя'
                }),
            'email': EmailInput(attrs={
                'class': 'form-container',
                'placeholder': 'Почта'
                }),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = CharField(
        widget=TextInput(attrs={'class': 'form-container', 'placeholder': 'Имя пользователя'})
    )
    password = CharField(
        widget=PasswordInput(attrs={'class': 'form-container', 'placeholder': 'Пароль'})
    )

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        }