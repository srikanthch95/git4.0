from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login



from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated

from .models import Books,BorrowedBooks
from .serializers import BooksSerializer

from datetime import datetime



class Add_Books_To_Library(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        if request.user.is_authenticated:
            user = request.user
            if user.is_superuser:
                bookData = request.data
                bookserilalize = BooksSerializer(data=bookData)
                if bookserilalize.is_valid():
                    bookserilalize.save()
                    return Response('Book is Added to the library')
                else:
                    return Response('please give valid book details')
            else:
                return Response('Only Access for Admin')


class GetAllBooks(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self,request):
        content = Books.objects.all()
        content1 = BooksSerializer(content, many=True)
        return Response(content1.data)



class UserRegistration(APIView):
    def post(self,request):
        userData = request.data
        try:
            user = User.objects.create_user(userData['username'], userData['email'], userData['password'])
        except:
            return Response('pls enter valid data')
        else:
            user.save()
            return  Response('registered successfully')


class UserLogin(APIView):
    def post(self,request):
        userData = request.data
        user_name = userData['username']
        user_password = userData['password']
        user = authenticate(request, username = user_name, password = user_password)

        if user is not None:
            login(request, user)
            username = request.user
            print(username)
            return Response(f'login success {username}')
        else:
            return Response('pls verify credentials')



class BorrowedBook(APIView):
    permission_classes = (IsAuthenticated,)
    print(permission_classes)
    def put(self, request):
        if request.user.is_authenticated:
            user = request.user.id
            book_Data = request.data
            try:
                borrow_book = Books.objects.get(id=book_Data['book_id'])
                bookid = book_Data['book_id']
                date = datetime.now()
                try:
                    existing_user = BorrowedBooks.objects.get(borrowed_user_id=user)
                    BorrowedBooks.objects.filter(borrowed_user_id=user).update(total_borrowed_books = existing_user.total_borrowed_books+1)
                    total_books = borrow_book.book_count
                    Books.objects.filter(id=book_Data['book_id']).update(book_count=total_books - 1)
                    message = {"message": f"Hi,  Book  { borrow_book.book_name } Is Borrowed"}
                    return Response(message)

                except BorrowedBooks.DoesNotExist:
                    user_borrowed_books = BorrowedBooks(book_id=bookid, borrow_date=date, borrowed_book_id=bookid,
                                                 borrowed_user_id=user)
                    user_borrowed_books.save()
                    total_books = borrow_book.book_count
                    Books.objects.filter(id=book_Data['book_id']).update(book_count=total_books - 1)
                    message = {"message": f"Hi,  Book  { borrow_book.book_name } Is Borrowed"}
                    return Response(message)



            except Books.DoesNotExist:
                message = {"message": 'Please Once Check Book ID Number'}
                return Response(message)
        else:
            print(request.user)
            return Response('User is not logged in')



def home(requset):
    return render(requset,'home.html')