from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from .models import Project

from .forms import ProjectForm

class ProjectHome(ListView):
    model = Project
    template_name: str = 'project/home.html'
    context_object_name = 'all_projects'

class CreateProject(CreateView):
    form_class = ProjectForm
    template_name = 'project/create.html'

    def get_success_url(self):
        return reverse('create_project')

def update_project(request):
    pass

class ViewProject(DetailView):
    model = Project
    template_name: str = 'project/view.html'

def delete_project(request, project_id):
    pass