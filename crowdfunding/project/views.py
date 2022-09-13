from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Project

from .forms import ProjectForm

# Create your views here.
def create_project(request):
    context = {
        'form' : ProjectForm,
        }
    if request == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/project/create')
    return render(request, 'project/create.html', context = context)
