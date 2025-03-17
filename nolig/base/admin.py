from django.contrib import admin

# Register your models here.
from .models import Discussion, Topic, Message, FlashCard, FlashcardSet

admin.site.register(Discussion)
admin.site.register(Topic)
admin.site.register(Message)    
admin.site.register(FlashCard)
admin.site.register(FlashcardSet)
