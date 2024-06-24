from django.shortcuts import render,redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class UserRegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        return super().form_valid(form)

class UserLibraryAccountUpdateView(LoginRequiredMixin,View):
    template_name = 'accounts/profile.html'

    def get(self,request):
        form = UserUpdateForm(instance=request.user)
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form = UserUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('login')
    
class UserPasswordChangeView(LoginRequiredMixin,PasswordChangeView):
    template_name = 'accounts/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')

    def form_valid(self,form):
        messages.success(self.request,"You have successfully changed your account password")
        message  = render_to_string('accounts/pass_change_email.html',{'user':self.request.user})
        send_email = EmailMultiAlternatives("Password Change Successful","",to=[self.request.user.email])
        send_email.attach_alternative(message,'text/html')
        send_email.send()
        return super().form_valid(form)