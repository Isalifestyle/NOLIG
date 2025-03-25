from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Discussion, Topic, FlashcardSet, FlashCard
from rest_framework import viewsets
from .models import FlashCard, FlashcardSet
from .serializers import FlashCardSerializer, FlashcardSetSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import FlashcardSet, FlashCard
from .serializers import FlashcardSetSerializer, FlashCardSerializer
import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from .forms import DiscussionForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

# ok

#Login page

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

#Register
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


#Home page
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    discussions = Discussion.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()
    discussion_count = discussions.count()

    context ={'discussions':discussions, 'topics': topics, 'discussion_count': discussion_count}
    return render(request, 'base/home.html', context)

def discussion(request,pk):
    discussion= Discussion.objects.get(id=pk)   
    context = {'discussion': discussion}

    return render(request, 'base/discussion.html',context)

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

def serve_react(request):
    react_build_path = os.path.join(settings.BASE_DIR, 'frontend/build/index.html')

    if os.path.exists(react_build_path):
        with open(react_build_path, 'r') as file:
            return HttpResponse(file.read(), content_type='text/html')
    else:
        return HttpResponse("React build not found. Run 'npm run build' in the frontend folder.", status=404)
