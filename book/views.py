from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from book.models import Book, CustomUser
from .forms import BookForm, RegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView, CreateView, DetailView
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from .wrappers import file_upload_check
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import permission_classes, authentication_classes, renderer_classes, api_view
from djoser.views import TokenCreateView, TokenDestroyView
# from django.views.generic import TemplateView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import string
import random
# Create SQLAchemmy Engine
def get_connection():

    url = "postgresql://postgres:pass@localhost:5432/social_book"
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    return Session()

# stmt = select(book_custom)

# Create your views here.
@login_required
def index(request):
    authors = CustomUser.objects.filter(public_visibility=True).order_by('id')
    # book_count = Book.objects.select_related().count()
    context = {
        'authors': authors,
        # 'book_count': book_count
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
            user = authenticate(username=username, password=password)
            # token = Token.objects.get_or_create(user=user)
            create_token = TokenCreateView.as_view()
            token = create_token(request)
            print(token)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {request.user.get_fullname}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid Credentials, Please try again")
    form = UserLoginForm()
    return render(request, 'login.html', {"form": form})



# class LoginAPI(CreateAPIView):
#     template_name = 'api_login.html'
#     renderer_classes = [TemplateHTMLRenderer]

#     # def get(self, request):
#     #     return Response({"data": "hello world"})
#     #     print("Here")

#     def post(self, request):
#         print("Here")
#         username = request.POST['id_username']
#         password = request.POST['id_password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             token = Token.objects.get_or_create(user=user)
#             login(request, user)
#             return redirect('home')

@login_required
def logout_user(request):
    token = Token.objects.get(user=request.user)
    # destroy_token = TokenDestroyView.as_view()
    # token = destroy_token(request)
    print(token)
    # print(token)
    logout(request)
    token.delete()
    return redirect('home')

@method_decorator(login_required, name='dispatch')
class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('books-list')
    template_name = 'book_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        messages.success(self.request, "Your book has been uploaded")
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

@method_decorator([login_required(redirect_field_name='books-list'), file_upload_check], name='dispatch')
class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.filter(visibility=True)
@method_decorator(login_required, name='dispatch')
class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'


# class BookDetailAPI(APIView):
#     authentication_classes = [TokenAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#     model = Book
#     serializer_class = BookSerializer
#     template_name = 'api_book_detail.html'
#     renderer_classes = [TemplateHTMLRenderer]

#     def get(self, request, pk):
#         queryset = Book.objects.get(pk=pk)
#         print(queryset)
#         return Response({"book": queryset})

#     def post(self, request, pk):
#         book = Book.objects.get(pk=pk)
#         subject = f"Request for details of {book.title} - Social Book"
#         message = f'Here is your requested information\nBook Name: {book.title}\nDescription: {book.description}\nAuthor: {book.author.get_fullname}\nPublished Date: {book.published_date}\nCost: {book.cost}'
#         from_email = settings.EMAIL_HOST_USER
#         to_email = [request.user.email]
#         try:
#             send_mail(subject, message, from_email, recipient_list=to_email)
#             messages.success(request, "Book details been sent, check your email")
#         except Exception:
#             messages.error(request, "Error sending email try again later")
#         return redirect('book-detail-api', pk=book.pk)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@renderer_classes([TemplateHTMLRenderer])
def book_detail_api(request, pk):

    if request.method == "GET":
        book = Book.objects.get(pk=pk)
        return Response({"book": book}, template_name='api_book_detail.html')
    
    if request.method == "POST":
        book = Book.objects.get(pk=pk)
        subject = f"Request for details of {book.title} - Social Book"
        message = f'Here is your requested information\nBook Name: {book.title}\nDescription: {book.description}\nAuthor: {book.author.get_fullname}\nPublished Date: {book.published_date}\nCost: {book.cost}'
        from_email = settings.EMAIL_HOST_USER
        to_email = [request.user.email]
        try:
            send_mail(subject, message, from_email, recipient_list=to_email)
            messages.success(request, "Book details been sent, check your email")
        except Exception:
            messages.error(request, "Error sending email try again later")
        return redirect('book-detail-api', pk=book.pk)

@csrf_exempt
def change_book_visibility(request, pk):
    book = Book.objects.get(pk=pk)
    if book.visibility:
        book.visibility = False
    else:
        book.visibility = True
    book.save()
    return redirect('book-detail-api', pk=book.pk)


def author_detail(request, username):
    author = CustomUser.objects.get(username=username)
    if request.user == author:
        books = Book.objects.filter(author=author)
    else:
        books = Book.objects.filter(author=author, visibility=True)
    context = {
        'author': author,
        'books': books
    }
    # print(request.user)
    return render(request, 'author_detail.html', context)

@csrf_exempt
def change_author_visibililty(request, pk):
    author = CustomUser.objects.get(pk=pk)
    if author.public_visibility:
        author.public_visibility = False
    else:
        author.public_visibility = True
    author.save()
    return redirect('author-detail', username=author.username)

def send_details(request):
    user = CustomUser.objects.get(username=request.user.username)

    subject = "Request for details - Social Book"
    message = f'Here is your information you requested from our website\nName: {user.get_fullname} \nUsername: {user.username} \nEmail: {user.email} \nAddress: {user.address} \n'
    from_email = settings.EMAIL_HOST_USER
    to_email = user.email
    try:
        send_mail(subject, message, from_email, recipient_list=[to_email])
        messages.success(request, "Your details have been sent, check your email")
    except Exception:
        messages.error(request, "Error sending email try again later")
    return redirect('home')

def generate_2fa():
    digits = string.digits
    two_fa = ''
    for _ in range(6):
        two_fa += random.choice(digits)
    return two_fa
