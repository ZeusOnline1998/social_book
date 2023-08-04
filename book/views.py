from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from book.models import Book, CustomUser
from .forms import BookForm, RegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, FormView, CreateView, DetailView

# Create your views here.
def index(request):
    authors = CustomUser.objects.filter(public_visibility=True)
    book_count = Book.objects.select_related().count()
    context = {
        'authors': authors
    }
    return render(request, 'index.html', context=context)

# class IndexView(ListView):
#     model = CustomUser
#     template_name = 'index.html'
#     context_object_name = 'authors'
#     def get_queryset(self):
#         return CustomUser.objects.filter(public_visibility=True)


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

class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('books-list')
    template_name = 'book_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

# def upload_book(request):
#     if request.method == 'POST':
#         form = BookForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.instance.author = request.user
#             form.save()
#             return redirect('home')
#     form = BookForm()
#     return render(request, 'upload_book.html', {"form": form})

class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.filter(visibility=True)

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

def author_detail(request, slug):
    author = CustomUser.objects.get(slug=slug)
    books = Book.objects.filter(author=author, visibility=True)
    context = {
        'author': author,
        'books': books
    }
    print(request.user)
    return render(request, 'author_detail.html', context)
