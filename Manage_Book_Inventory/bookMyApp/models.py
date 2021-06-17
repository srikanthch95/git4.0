from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Books(models.Model):
    book_name = models.CharField(max_length=50)
    book_author = models.CharField(max_length=40)
    book_count = models.IntegerField()

    def __str__(self):
        return self.book_name



class BorrowedBooks(models.Model):
    borrowed_user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_book = models.ForeignKey(Books,on_delete=models.CASCADE)
    book_id = models.IntegerField()
    borrow_date = models.DateTimeField()
    total_borrowed_books = models.IntegerField(default=False)