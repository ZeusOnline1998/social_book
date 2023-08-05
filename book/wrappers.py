from .models import Book
from django.shortcuts import redirect

def file_upload_check(func):

    def user_file_exists(request, *args, **kwargs):
        if Book.objects.filter(author=request.user).exists():
            return func(request, *args, **kwargs)
        else:
            return redirect('upload-book')

    return user_file_exists
