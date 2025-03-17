from django.shortcuts import render, get_object_or_404
from .models import Discussion, FlashcardSet, FlashCard
# Create your views here.




def home(request):
    discussions = Discussion.objects.all()
    context ={'discussions':discussions}
    return render(request, 'base/home.html',context)

def discussion(request,pk):
    discussion= Discussion.objects.get(id=pk)   
    context = {'discussion':discussion}

    return render(request, 'base/discussion.html',context)


# Show all flashcard sets
def flashcard_sets(request):
    sets = FlashcardSet.objects.all()
    return render(request, 'base/flashcard_sets.html', {'sets': sets})

# Show flashcards in a set
def flashcard_detail(request, set_id):
    flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
    flashcards = flashcard_set.flashcards.all()  # Thanks to related_name="flashcards"
    return render(request, 'base/flashcard_detail.html', {'set': flashcard_set, 'flashcards': flashcards})

