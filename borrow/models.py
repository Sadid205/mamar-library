from django.db import models
from django.contrib.auth.models import User
from books.models import Books
# Create your models here.

class Borrow(models.Model):
    user = models.ForeignKey(User,related_name='borrow',on_delete=models.CASCADE)
    book = models.ForeignKey(Books,on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True,blank=True)
    quantity = models.IntegerField(default=0,blank=True,null=True)

    def __str__(self):
        return str(self.borrow_date)

