from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Discussion, Topic, FlashcardSet, Message, FlashCard
from .forms import DiscussionForm, FlashcardForm, FlashcardSetForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from .models import Profile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FlashcardSetSerializer, FlashCardSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    # Filter the flashcard sets based on whether the user is logged in or not
    if request.user.is_authenticated:
        flashcard_sets = FlashcardSet.objects.filter(user=request.user).order_by('-created')  # Logged-in user sees their sets
        discussions = Discussion.objects.filter(host=request.user).order_by('-created')
    else:
        flashcard_sets = FlashcardSet.objects.all().order_by('-created')  # Non-logged-in user sees all sets
        discussions = Discussion.objects.all().order_by('-created')
    if q:
        discussions = discussions.filter(
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
            topic_name = form.cleaned_data['topic']
            topic, created = Topic.objects.get_or_create(name=topic_name)

            # ✅ Now we can safely create the discussion instance
            discussion = form.save(commit=False)
            discussion.host = request.user
            discussion.topic = topic  # this is a Topic instance now
            discussion.save()

            return redirect('home')

    return render(request, 'base/discussion_form.html', {'form': form})


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
def createFlashcardSet(request):
    form = FlashcardSetForm()

    if request.method == 'POST':
        form = FlashcardSetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/flashcard_set_form.html', context)

@login_required(login_url='login')
def updateDiscussion(request, pk):
    discussion = Discussion.objects.get(id=pk)

    if request.user != discussion.host:
        return HttpResponse('You are not allowed here!')

    form = DiscussionForm(instance=discussion)

    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            topic_name = form.cleaned_data['topic']
            topic, created = Topic.objects.get_or_create(name=topic_name)
            
            discussion = form.save(commit=False)
            discussion.topic = topic  # manually assign topic instance
            discussion.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/discussion_form.html', context)

@login_required(login_url='login')
def updateFlashcard(request, pk):
    flashcard = FlashCard.objects.get(id=pk)
    form = FlashcardForm(instance=flashcard)

    if request.user != flashcard.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/flashcard_form.html', context)

@login_required(login_url='login')
def updateFlashcardSet(request, pk):
    flashcard_set = FlashcardSet.objects.get(id=pk)
    form = FlashcardSetForm(instance=flashcard_set)

    if request.user != flashcard_set.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        form = FlashcardSetForm(request.POST, instance=flashcard_set)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/flashcard_set_form.html', context)

@login_required(login_url='login')
def deleteFlashcardSet(request, pk):
    flashcard_set = FlashcardSet.objects.get(id=pk)

    if request.user != flashcard_set.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        flashcard_set.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':flashcard_set})

@login_required(login_url='login')
def deleteFlashcard(request, pk):
    flashcard = FlashCard.objects.get(id=pk)

    if request.user != flashcard.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        flashcard.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':flashcard})

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


def flashcardFeed(request):
    flashcard_sets = FlashcardSet.objects.all().order_by('-created')
    
    return render(request, 'base/flashcard_page.html', {'flashcard_sets': flashcard_sets})

def discussionPage(request):
    discussions = Discussion.objects.all().order_by('-created')
    
    return render(request, 'base/discussion_page.html', {'discussions': discussions})

def userProfile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # If user is looking at their own profile, redirect to the editable settings page
    if request.user.is_authenticated and request.user.id == user.id:
        return redirect('user-settings')

    return render(request, 'base/public_profile.html', {'user': user})
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
    return redirect('landing')


@login_required(login_url='login')
def user_settings(request):
    # Get or create the user's profile
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'update_avatar' in request.POST:
            avatar = request.FILES.get('avatar')
            if avatar:
                profile.avatar = avatar
                profile.save()

        elif 'update_password' in request.POST:
            new_password = request.POST.get('password')
            if new_password:
                request.user.set_password(new_password)
                request.user.save()
                login(request, request.user)  # Optional: re-login
                messages.success(request, "Password updated successfully.")

        elif 'update_bio' in request.POST:
            new_bio = request.POST.get('bio', '')
            profile.bio = new_bio
            profile.save()
            messages.success(request, "Bio updated successfully.")

    return render(request, 'base/user_settings.html', {
        'user': request.user,
        'profile': profile  # ✅ Pass profile to access bio and avatar
    })


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


def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'base/landing_page.html')

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'base/landing_page.html')