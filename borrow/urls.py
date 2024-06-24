from django.urls import path
from .views import BorrowView,BorrowedBookList,ReturnBookView
urlpatterns = [
    path('books/<int:id>/',BorrowView,name='borrow'),
    path('books/borrowed_list/',BorrowedBookList.as_view(),name='borrowed_book_list'),
    path('books/return/<int:id>/',ReturnBookView,name='return_book'),
]
