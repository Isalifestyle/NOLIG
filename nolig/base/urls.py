from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('discussion/<str:pk>', views.discussion, name='discussion'),
    path('flashcards/', views.flashcard_sets, name='flashcard_sets'),
    path('flashcards/<int:set_id>/', views.flashcard_detail, name='flashcard_detail'),
]