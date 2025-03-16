from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('discussion/<str:pk>', views.discussion, name='discussion'),
    path('flashcards/', views.flashcards, name='flashcards'),
]