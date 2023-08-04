from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('upload-book/', views.UploadBookView.as_view(), name='upload-book'),
    # path('upload-book/', views.upload_book, name='upload-book'),
    path('books-list/', views.BookListView.as_view(), name='books-list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('author/<str:username>/', views.author_detail, name='author-detail'),
]
