from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_user, name='login'),
    # path('api/login/', views.LoginAPI.as_view(), name='login-api'),
    # path('login/', views.LoginUserAPI.as_view(), name='login'),
    # path('login/', views.TokenCreateView.as_view(), name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='my_logout'),
    path('upload-book/', views.UploadBookView.as_view(), name='upload-book'),
    # path('upload-book/', views.upload_book, name='upload-book'),
    path('books-list/', views.BookListView.as_view(), name='books-list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('api/book/<int:pk>/', views.BookDetailAPI.as_view(), name='book-detail-api'),
    path('author/<str:username>/', views.author_detail, name='author-detail'),
    path('send-details', views.send_details, name='send-details'),
    path('api/book/<int:pk>/change-book-visibility/', views.change_book_visibility, name='change-book-visibility'),
    path('author/<int:pk>/change-author-visibility/', views.change_author_visibililty, name='change-author-visibility'),
    # path('generate/', views.generate, name='generate'),
]
