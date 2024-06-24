from django.db import models
from .constants import REVIEWS
from category.models import CategoryModel
# Create your models here.

class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.ManyToManyField(CategoryModel)
    image = models.ImageField(upload_to='uploads/',blank=True,null=True)
    borrowing_price = models.DecimalField(default=0,max_digits=7,decimal_places=2)
    user_reviews = models.CharField(max_length=50,choices=REVIEWS)
    description = models.TextField()
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    book =  models.ForeignKey(Books,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=30)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comments by {self.name}"