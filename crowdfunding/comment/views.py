from .models import Comment
from project.models import Project
from django.shortcuts import get_object_or_404 , redirect
from django.http import HttpResponse 
# Create your views here.


def create(request,projectid):
    if request.POST:
        project = get_object_or_404(Project,pk = projectid)
        Ancomment = Comment()
        Ancomment.project = project
        Ancomment.user = request.user
        Ancomment.comment = request.POST['content']
        Ancomment.save()
        return redirect('/project')