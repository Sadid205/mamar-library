from django.shortcuts import render,redirect
from .models import Borrow
from books.models import Books,Comment
from django.contrib import messages
from django.views.generic import ListView
from transaction.views import send_transaction_email
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def BorrowView(request,id):
    user = request.user
    book = Books.objects.get(id=id)
    comments = Comment.objects.filter(book=book)

    try:
        ExistingBorrow = Borrow.objects.get(user=user,book=book)
    except:
        ExistingBorrow = None
    if book.quantity > 0:
        if user.account.balance>=book.borrowing_price:
            book.quantity -=1
            book.save()
            user.account.balance-=book.borrowing_price
            user.account.save()
            if ExistingBorrow:
                ExistingBorrow.quantity+=1
                ExistingBorrow.save()
                messages.success(request,f"You have successfully borrowed a book.")
                send_transaction_email(user,book.borrowing_price,"Successfully Borrowed Books","borrow/borrowed_success_email.html",book)
                return render(request,'books/book_details.html',{'books':book,'comments':comments})
            else:
                newBorrow = Borrow()
                newBorrow.user = user
                newBorrow.book = book
                newBorrow.quantity = 1
                newBorrow.save()
                messages.success(request,"You have successfully borrowed a book.")
                send_transaction_email(user,book.borrowing_price,"Successfully Borrowed Books","borrow/borrowed_success_email.html",book)
                return render(request,'books/book_details.html',{'books':book,'comments':comments})
        else:
            messages.warning(request,"Your account does not have enough balance")
            return redirect('home')
            
    else:
        messages.warning(request,"This book is not available at this moment")
        return redirect('home')


class BorrowedBookList(LoginRequiredMixin,ListView):
    model = Borrow
    template_name = 'borrow/borrow_list.html'
    context_object_name = 'borrowed_books'

    def get_queryset(self):
        user = self.request.user
        queryset = Borrow.objects.filter(user=user)
        return queryset

def ReturnBookView(request,id):
    book = Books.objects.get(id=id)
    borrow_book = Borrow.objects.get(user=request.user,book=book)
    book.quantity += borrow_book.quantity
    total_amount = book.borrowing_price * borrow_book.quantity
    request.user.account.balance +=total_amount
    request.user.account.save()
    borrow_book.delete()
    book.save()
    messages.success(request,"You have successfully return book.")
    send_transaction_email(request.user,total_amount,"Successfully Returned Books","borrow/return_success_email.html",book,borrow_book.quantity)
    return redirect('borrowed_book_list')