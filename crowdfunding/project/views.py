from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.messages.views import SuccessMessageMixin

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
    # success_message: str = 'Object Updated Successfully!'
    def get_success_url(self) -> str:
        return reverse('project_home')

# View
class ViewProject(DetailView):
    model = Project
    template_name: str = 'project/view.html'

# Delete
class DeleteProject(DeleteView):
    model = Project
    template_name: str = 'project/view.html'
    success_url = reverse_lazy('project_home')