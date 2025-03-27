from django.urls import path, include 
from django.shortcuts import redirect
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlashcardSetViewSet, FlashCardViewSet, flashcard_sets, flashcard_detail
from rest_framework.routers import DefaultRouter
from .views import FlashcardSetViewSet, FlashCardViewSet, flashcard_feed
from . import views
from .views import serve_react
from django.urls import re_path

router = DefaultRouter()
router.register(r'flashcard-sets', FlashcardSetViewSet)
router.register(r'flashcards', FlashCardViewSet)

urlpatterns = [

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name='home'),
    path('discussion/<str:pk>', views.discussion, name='discussion'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/flashcard-sets/', flashcard_sets, name='flashcard-sets'),
    path('api/flashcard-sets/<int:set_id>/', flashcard_detail, name='flashcard-detail'),

    # Routes related to discussions
    path('create-discussion/', views.createDiscussion, name="create-discussion"),
    path('update-discussion/<str:pk>', views.updateDiscussion, name="update-discussion"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),

    # Flashcard feed route
    path('flashfeed/', flashcard_feed, name='flashcard-feed'),

    # React route for all unmatched paths
    # re_path(r'^(?!create-discussion|update-discussion|delete-message|discussion).*$', serve_react),
]