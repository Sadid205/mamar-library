from django.urls import path
from .views import BookDetailsView
urlpatterns = [
    path('details/<int:id>/',BookDetailsView.as_view(),name='book_details')
]
