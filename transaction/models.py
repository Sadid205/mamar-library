from django.db import models
from accounts.models import UserLibraryAccountModel
from .constants import TRANSACTION_TYPE
# Create your models here.

class Transaction(models.Model):
    account = models.ForeignKey(UserLibraryAccountModel,related_name='transactions',on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=3,max_digits=8)
    balance_after_transaction = models.DecimalField(decimal_places=3,max_digits=8)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.account.account_number)

