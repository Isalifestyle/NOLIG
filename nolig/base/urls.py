from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlashcardSetViewSet, FlashCardViewSet, flashcard_sets, flashcard_detail, flashcard_feed, serve_react
from . import views
from django.urls import re_path

router = DefaultRouter()
router.register(r'flashcard-sets', FlashcardSetViewSet)
router.register(r'flashcards', FlashCardViewSet)

urlpatterns = [

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('user/<int:user_id>/', views.user_profile, name='user-profile'),
    path('settings/', views.user_settings, name='user-settings'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('flashcard-set/<int:set_id>/', views.flashcard_set_detail, name='flashcard-set-detail'),
    

    path('', views.home, name='home'),
    path('discussion/<str:pk>', views.discussion, name='discussion'),
    
    # API endpoints
    # path('api/', include(router.urls)),
    # path('api/flashcard-sets/', flashcard_sets, name='flashcard-sets'),
    # path('api/flashcard-sets/<int:set_id>/', flashcard_detail, name='flashcard-detail'),
    # path('api/flashcards/', flashcard_feed, name='flashcard-feed'),
    # Routes related to discussions
    path('create-discussion/', views.createDiscussion, name="create-discussion"),
    path('update-discussion/<str:pk>', views.updateDiscussion, name="update-discussion"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),

    # Flashcard feed route
    # path('flashfeed/', flashcard_feed, name='flashcard-feed'),
    path('create-flashcard/', views.createFlashcard, name="create-flashcard"),
    # React route for all unmatched paths
    # re_path(r'^(?!create-discussion|update-discussion|delete-message|discussion).*$', serve_react),
    # path('flashcards/<int:set_id>/', views.serve_react),
]