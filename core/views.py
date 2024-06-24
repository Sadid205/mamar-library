from django.shortcuts import render
from django.views.generic import TemplateView
from books.models import Books
from category.models import CategoryModel
# Create your views here.

class HomeView(TemplateView):
    template_name = 'core/index.html'

    def get(self,request,category_slug=None):
        books = Books.objects.all()
        if category_slug is not None:
            category = CategoryModel.objects.get(slug=category_slug)
            books = Books.objects.filter(category=category)
        categories = CategoryModel.objects.all()
        return render(request,self.template_name,{"books":books,"categories":categories})