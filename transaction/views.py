from django.shortcuts import render
from .models import Transaction
from .forms import DepositForm
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .constants import DEPOSIT
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
# Create your views here.

def send_transaction_email(user,amount,subject,template,book=None,quantity=None):
    message = render_to_string(template,{
        'user':user,
        'amount':amount,
        'book':book,
        'quantity':quantity
    })
    send_email = EmailMultiAlternatives(subject,'',to=[user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()

class DepositMoneyView(LoginRequiredMixin,CreateView):
    template_name = 'transaction/deposit.html'
    model = Transaction
    form_class = DepositForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account':self.request.user.account
        })
        return kwargs
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title':"Deposit Form"
        })
        return context
    
    def get_initial(self):
        initial = {'transaction_type':DEPOSIT}
        return initial

    def form_valid(self,form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields =[
                'balance'
            ]
        )
        messages.success(
            self.request,
            f'{amount} taka was successfully deposited to your account'
        )
        send_transaction_email(self.request.user,amount,"Deposit Balance","transaction/deposit_email.html")

        return super().form_valid(form)
    
