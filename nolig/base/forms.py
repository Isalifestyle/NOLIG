from django.forms import ModelForm
from .models import Discussion, FlashCard, FlashcardSet
from django import forms

class DiscussionForm(forms.ModelForm):
    topic = forms.CharField()  # override default ForeignKey behavior
    class Meta:
        model = Discussion
        fields = ['name', 'description']  # 🛑 DO NOT include 'topic' here
class FlashcardForm(ModelForm):
    class Meta:
        model = FlashCard
        fields = '__all__'

class FlashcardSetForm(ModelForm):
    class Meta:
        model = FlashcardSet
        fields = '__all__'
