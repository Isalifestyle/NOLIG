from django.forms import ModelForm
from .models import Discussion, FlashCard

class DiscussionForm(ModelForm):
    class Meta:
        model = Discussion
        fields = '__all__'


class FlashcardForm(ModelForm):
    class Meta:
        model = FlashCard
        fields = '__all__'
    