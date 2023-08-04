from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
# from django.contrib.auth.models import User
from .models import CustomUser, Book

class RegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 
            'last_name', 
            'username', 
            'email', 
            'password1', 
            'password2', 
            'birth_year', 
            'address',
            'public_visibility',
        ]

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'First Name'
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Last Name'
            }
        )
    )

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Username'
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'abc@example.com',
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Password'
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Confirm Password'
            }
        )
    )

    birth_year = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control lg',
                'placeholder': 'Birth Year'
            }
        )
    )

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Address'
            }
        )
    )

class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Password'
            }
        )
    )


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = [
            'title', 
            'description', 
            'cost', 
            'published_date', 
            'visibility', 
            'file'
        ]

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control form-control-lg',
            }
        )
    )

    cost = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
            }
        )
    )

    published_date = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
            }
        )
    )

    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file form-control height-auto',
                'accept': '.pdf, .jpeg, .jpg'
            }
        )
    )