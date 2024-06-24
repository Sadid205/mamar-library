from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserLogoutView,UserLibraryAccountUpdateView,UserPasswordChangeView
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('password_change/',UserPasswordChangeView.as_view(),name='change_password'),
    path('profile/',UserLibraryAccountUpdateView.as_view(),name='profile'),
]
