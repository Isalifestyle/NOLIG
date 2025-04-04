from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Discussion(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description= models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    
    
# Add a parent field that references self (so a Message can be the child of another Message). If parent is NULL, it’s a top-level comment; if not, it’s a reply.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    body = models.TextField()
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]

class FlashcardSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The creator of the set
    title = models.CharField(max_length=255)  # Title of the flashcard set
    description = models.TextField(blank=True, null=True)  # Optional description
    created = models.DateTimeField(auto_now_add=True) # Timestamp


    def __str__(self):
        return self.title


class FlashCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Owner of the flashcard
    flashcard_set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE, related_name="flashcards")  # Link to set
    question = models.TextField()
    answer = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.question[:50]
