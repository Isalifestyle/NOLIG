from django.forms import ModelForm
from .models import Discussion, FlashCard, FlashcardSet
from django import forms

class DiscussionForm(forms.ModelForm):
    topic = forms.CharField(
        max_length=200,
        help_text="Enter a topic (e.g., Math, History...)"
    )

    class Meta:
        model = Discussion
        fields = ['name', 'topic', 'description']

class FlashcardForm(ModelForm):
    class Meta:
        model = FlashCard
        fields = '__all__'

class FlashcardSetForm(ModelForm):
    class Meta:
        model = FlashcardSet
        fields = '__all__'
