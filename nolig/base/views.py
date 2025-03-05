from django.shortcuts import render
from .models import Discussion
# Create your views here.




def home(request):
    discussions = Discussion.objects.all()
    context ={'discussions':discussions}
    return render(request, 'base/home.html',context)

def discussion(request,pk):
    discussion= Discussion.objects.get(id=pk)   
    context = {'discussion':discussion}

    return render(request, 'base/discussion.html',context)

