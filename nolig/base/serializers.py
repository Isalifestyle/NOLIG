from rest_framework import serializers
from .models import FlashCard, FlashcardSet

class FlashcardSetSerializer(serializers.ModelSerializer):
    flashcards = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = FlashcardSet
        fields = ['id', 'user', 'title', 'description', 'created', 'flashcards']

class FlashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashCard
        fields = ['id', 'user', 'flashcard_set', 'question', 'answer', 'updated', 'created']
