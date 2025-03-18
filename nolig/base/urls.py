from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import FlashcardSetViewSet, FlashCardViewSet
from . import views

router = DefaultRouter()
router.register(r'flashcardsets', FlashcardSetViewSet)
router.register(r'flashcards', FlashCardViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('discussion/<str:pk>', views.discussion, name='discussion'),
    path('flashcards/', views.flashcard_sets, name='flashcard_sets'),
    path('flashcards/<int:set_id>/', views.flashcard_detail, name='flashcard_detail'),
    path('api/', include(router.urls)),

]