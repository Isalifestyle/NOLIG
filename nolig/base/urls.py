from django.urls import path
from . import views

from .views import flashcard_feed, createFlashcardSet, updateFlashcardSet, deleteFlashcardSet, updateFlashcard, deleteFlashcard
from .views import flashcard_feed,flashcard_sets,flashcard_detail 

from .views import flashcard_feed,flashcard_sets,flashcard_detail, user_profile



urlpatterns = [

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('user/<int:user_id>/', views.user_profile, name='user-profile'),
    path('settings/', views.user_settings, name='user-settings'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('flashcards/<int:set_id>/', views.flashcard_set_detail, name='flashcard-set-detail'),


    path('', views.home, name='home'),
    path('discussion/<str:pk>', views.discussion, name='discussion'),
    path('delete-discussion/<int:pk>/', views.deleteDiscussion, name='delete-discussion'),
    path('load_more_replies/', views.load_more_replies, name='load-more-replies'),

  
    # Routes related to discussions
    path('create-discussion/', views.createDiscussion, name="create-discussion"),
    path('update-discussion/<str:pk>', views.updateDiscussion, name="update-discussion"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),

    # Flashcard feed route
    path('flashfeed/', flashcard_feed, name='flashcard-feed'),
    path('create-flashcard/', views.createFlashcard, name="create-flashcard"),
    path('delete-flashcard/<str:pk>', views.deleteFlashcard, name="delete-flashcard"),
    path('update-flashcard/<str:pk>', views.updateFlashcard, name="update-flashcard"),

    path('create-flashcard-set/', views.createFlashcardSet, name="create-flashcard-set"),
    path('update-flashcard-set/<str:pk>', views.updateFlashcardSet, name="update-flashcard-set"),
    path('delete-flashcard-set/<str:pk>', views.deleteFlashcardSet, name="delete-flashcard-set"),
    # React route for all unmatched paths
    # re_path(r'^(?!create-discussion|update-discussion|delete-message|discussion).*$', serve_react),
    # path('api/', include(router.urls)),
    path('api/flashcard-sets/', flashcard_sets, name='flashcard-sets'),
    path('api/flashcard-sets/<int:set_id>/', flashcard_detail, name='flashcard-detail'),
    path('api/flashcards/', flashcard_feed, name='flashcard-feed'),
]