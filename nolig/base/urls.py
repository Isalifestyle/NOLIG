from django.urls import path, include 
from django.shortcuts import redirect
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlashcardSetViewSet, FlashCardViewSet, flashcard_sets, flashcard_detail
from rest_framework.routers import DefaultRouter
from .views import FlashcardSetViewSet, FlashCardViewSet
from . import views
from .views import serve_react


router = DefaultRouter()
router.register(r'flashcard-sets', FlashcardSetViewSet)
router.register(r'flashcards', FlashCardViewSet)

urlpatterns = [

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
     path('register/', views.registerPage, name="register"),

    path('', views.home, name='home'),
    path('discussion/<str:pk>', views.discussion, name='discussion'),
    path('api/', include(router.urls)),  # API endpoints for flashcards
    path('api/flashcard-sets/', flashcard_sets, name='flashcard-sets'),
    path('api/flashcard-sets/<int:set_id>/', flashcard_detail, name='flashcard-detail'),
    path('flashcards/', serve_react, name='react_frontend'),

    path('create-discussion/', views.createDiscussion, name="create-discussion"),
    path('update-discussion/<str:pk>', views.updateDiscussion, name="update-discussion"),
    path('delete-discussion/<str:pk>', views.deleteDiscussion, name="delete-discussion"),
]