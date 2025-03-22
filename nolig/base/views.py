from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
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

# Create your views here.

# ok


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

def createDiscussion(request):
    form = DiscussionForm()

    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/discussion_form.html', context)

def updateDiscussion(request, pk):
    discussion = Discussion.objects.get(id=pk)
    form = DiscussionForm(instance=discussion)

    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/discussion_form.html', context)

def deleteDiscussion(request, pk):
    discussion = Discussion.objects.get(id=pk)
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
