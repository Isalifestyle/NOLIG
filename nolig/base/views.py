from django.shortcuts import render, get_object_or_404
from .models import Discussion, FlashcardSet, FlashCard
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

# Create your views here.




def home(request):
    discussions = Discussion.objects.all()
    context ={'discussions':discussions}
    return render(request, 'base/home.html',context)

def discussion(request,pk):
    discussion= Discussion.objects.get(id=pk)   
    context = {'discussion':discussion}

    return render(request, 'base/discussion.html',context)


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
