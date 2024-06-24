from django.shortcuts import render
from django.views.generic import DetailView
from .models import Books
from .forms import CommentForm
from borrow.models import Borrow
# Create your views here.

class BookDetailsView(DetailView):
    model = Books
    pk_url_kwarg = 'id'
    template_name = 'books/book_details.html'
    
    def post(self,request,*args,**kwargs):
        comment_form = CommentForm(data=self.request.POST)
        book = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.save()
        return  self.get(self,request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        comments = book.comments.all()
        try:
            borrow_book = Borrow.objects.get(user=self.request.user,book=book)
        except:
            borrow_book = None
        comment_form = CommentForm()
        context['comments'] = comments
        if borrow_book is not None:
            context['comment_form'] = comment_form
        else:
            context['comment_form'] = None

        return context

