from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def index(request):
    return render(request, 'index.html')


def register_user(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {"form": form})


def login_user(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                pass
    form = UserLoginForm()
    return render(request, 'login.html', {"form": form})

def logout_user(request):
    logout(request)
    return redirect('home')
