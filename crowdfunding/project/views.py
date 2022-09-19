from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.messages.views import SuccessMessageMixin

import project

from .models import Project, Image
from .forms import ProjectForm, ImageForm

class ProjectHome(ListView):
    model = Project
    template_name: str = 'project/home.html'
    context_object_name = 'all_projects'

# Create
class CreateProject(SuccessMessageMixin, CreateView):
    form_class = ProjectForm
    template_name = 'project/create.html'
    extra_context = {"imageform": ImageForm()}
    # success_message: str = 'Object Created Successfully!'
    def get_success_url(self):
        return reverse('project_home')
    
    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST)
        files = request.FILES.getlist("image")
        if form.is_valid():
            f = form.save(commit=False)
            f.created_by = request.user
            f.save()
            form.save_m2m()
            for i in files:
                Image.objects.create(project=f, image=i)
            # messages.success(request, "New Project Added")
            return HttpResponseRedirect("/project")

# Update
class UpdateProject(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/update.html'
    # extra_context = {"imageform": ImageForm()}
    # success_message: str = 'Object Updated Successfully!'
    def get_success_url(self) -> str:
        return reverse('project_home')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imageform'] = ImageForm()
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        context['images'] = Image.objects.filter(project=project)
        return context

    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST)
        files = request.FILES.getlist("image")
        if form.is_valid():
            f = form.save(commit=False)
            f.created_by = request.user
            f.save()
            form.save_m2m()
            for i in files:
                Image.objects.create(project=f, image=i)
            # messages.success(request, "New Project Added")
            return HttpResponseRedirect("/project")

# View
class ViewProject(DetailView):
    model = Project
    template_name: str = 'project/view.html'

# Delete
class DeleteProject(DeleteView):
    model = Project
    template_name: str = 'project/view.html'
    success_url = reverse_lazy('project_home')