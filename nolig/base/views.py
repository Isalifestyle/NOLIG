from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Discussion, Topic, FlashcardSet
from .models import FlashcardSet
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import FlashcardSet, Message
from django.shortcuts import render
from django.http import HttpResponse
from .forms import DiscussionForm, FlashcardForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import FlashcardSet, FlashCard
from .serializers import FlashcardSetSerializer, FlashCardSerializer
from django.http import HttpResponseBadRequest



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    # Filter the flashcard sets based on whether the user is logged in or not
    if request.user.is_authenticated:
        flashcard_sets = FlashcardSet.objects.filter(user=request.user).order_by('-created')  # Logged-in user sees their sets
    else:
        flashcard_sets = FlashcardSet.objects.all().order_by('-created')  # Non-logged-in user sees all sets

    discussions = Discussion.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    discussion_count = discussions.count()
    room_messages = Message.objects.filter(Q(discussion__topic__name__icontains=q))

    context = {
        'discussions': discussions, 
        'topics': topics, 
        'discussion_count': discussion_count, 
        'room_messages': room_messages,
        'flashcard_sets': flashcard_sets  # Passing filtered flashcards to the template
    }
    return render(request, 'base/home.html', context)

def discussion(request, pk):
    discussion = Discussion.objects.get(id=pk)
    # Filter top-level messages
    discussion_messages = Message.objects.filter(discussion=discussion, parent__isnull=True)
    participants = discussion.participants.all()

    if request.method == 'POST':
        body_text = request.POST.get('body')
        parent_id = request.POST.get('parent_id')  # If replying to a comment
        message = Message(
            discussion=discussion,
            user=request.user,
            body=body_text
        )
        if parent_id:
            try:
                parent_message = Message.objects.get(id=parent_id, discussion=discussion)
                message.parent = parent_message
            except Message.DoesNotExist:
                pass
        message.save()
        discussion.participants.add(request.user)
        return redirect('discussion', pk=discussion.id)

    context = {
        'discussion': discussion,
        'discussion_messages': discussion_messages,
        'participants': participants
    }
    return render(request, 'base/discussion.html', context)


@login_required(login_url='login')
def createDiscussion(request):
    form = DiscussionForm()

    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/discussion_form.html', context)

@login_required(login_url='login')
def createFlashcard(request):
    form = FlashcardForm()

    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/flashcard_form.html', context)

@login_required(login_url='login')
def updateDiscussion(request, pk):
    discussion = Discussion.objects.get(id=pk)
    form = DiscussionForm(instance=discussion)

    if request.user != discussion.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/discussion_form.html', context)

@login_required(login_url='login')
def deleteDiscussion(request, pk):
    discussion = Discussion.objects.get(id=pk)

    if request.user != discussion.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        discussion.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':discussion})

# API view to get all flashcard sets
@api_view(['GET'])
def flashcard_sets(request):
    sets = FlashcardSet.objects.all()
    serializer = FlashcardSetSerializer(sets, many=True)
    return Response(serializer.data)

# API view to get all flashcards in a set
@api_view(['GET'])
def flashcard_detail(request, set_id):
    flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
    flashcards = flashcard_set.flashcards.all()
    serializer = FlashCardSerializer(flashcards, many=True)
    return Response(serializer.data)

# ViewSets for the API (used for Django REST Framework's router)
class FlashcardSetViewSet(viewsets.ModelViewSet):
    queryset = FlashcardSet.objects.all()
    serializer_class = FlashcardSetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class FlashCardViewSet(viewsets.ModelViewSet):
    queryset = FlashCard.objects.all()
    serializer_class = FlashCardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registeration')

    return render(request, 'base/login_register.html', {'form': form})

@login_required(login_url='login')
def deleteMessage(request, pk):
    try:
        # Retrieve the message with the given pk
        message = Message.objects.get(id=pk)
    except Message.DoesNotExist:
        # Handle the case where the message does not exist
        messages.error(request, 'Message not found.')
        return redirect('home')

    # Check if the current user is the author of the message
    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this message.')

    # If the user is the author, delete the message
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})


def flashcard_feed(request):
    if request.user.is_authenticated:
        # Only show flashcard sets created by the logged-in user
        flashcard_sets = FlashcardSet.objects.filter(user=request.user).order_by('-created')
    else:
        # Show all flashcard sets if the user is not logged in
        flashcard_sets = FlashcardSet.objects.all().order_by('-created')
    
    return render(request, 'base/flashcard_feed.html', {'flashcard_sets': flashcard_sets})

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {
        'user': user
    }
    return render(request, 'base/user_settings.html', context)

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)   

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password not exist')
            
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

#Logout
def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def user_settings(request):
    # You can pass the user object to the template to display information
    return render(request, 'base/user_settings.html', {'user': request.user})


@login_required
def delete_account(request):
    if request.method == "POST":
        # The user has confirmed to delete their account, so delete the user
        user = request.user
        user.delete()
        return redirect('home')  # Redirect to home page after deletion

    # If GET request, show the confirmation page
    return render(request, 'base/confirm_delete_account.html')
def flashcard_set_detail(request, set_id):
    flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
    flashcards = flashcard_set.flashcards.all()  # Only flashcards for this set
    
    return render(request, 'base/flashcard_set_detail.html', {
        'flashcard_set': flashcard_set,
        'flashcards': flashcards
    })

def load_more_replies(request):
    parent_id = request.GET.get('parent_id')
    if not parent_id:
        return HttpResponseBadRequest("Missing parent_id")

    try:
        parent_message = Message.objects.get(id=parent_id)
    except Message.DoesNotExist:
        return HttpResponseBadRequest("Parent message not found")

    # For simplicity, load all replies, but you can filter if needed
    replies = parent_message.replies.all()

    # Render a partial HTML template with these replies
    return render(request, 'base/replies_partial.html', {'replies': replies})