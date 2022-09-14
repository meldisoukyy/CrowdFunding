from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from django.views.generic.edit import CreateView

from .models import Project

from .forms import ProjectForm


def project(request):
    all_projects = str(Project.objects.all())
    return HttpResponse(all_projects)

# def create_project(request):
#     if request.POST:
#         form = ProjectForm(request.POST, request.FILES)
#         print(form)
#         print(form.is_valid())
#         if form.is_valid():
#             form.save()
#             return HttpResponse('Success')
#     context = {
#         'form' : ProjectForm(),
#         }
#     return render(request, 'project/create.html', context = context)

class CreateProject(CreateView):
    form_class = ProjectForm
    # fields = '__all__'
    template_name = 'project/create.html'

    def get_success_url(self):
        return reverse('create_project')

def update_project(request):
    pass

def view_project(request, project_id):
    pass

def delete_project(request, project_id):
    pass