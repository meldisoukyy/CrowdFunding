from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from taggit.models import Tag

from .models import Project, Image
from .forms import ProjectForm, ImageForm, ReviewRating, ReviewForm

from categories.models import Category

class ProjectHome(ListView):
    model = Project
    template_name: str = 'project/home.html'
    context_object_name = 'all_projects'

    def post(self, request, *args, **kwargs):
        searched = request.POST['searched']
        try:
            tag = Tag.objects.get(slug=searched)
            projects = Project.objects.filter(project_tags=tag)
        except:
            projects = Project.objects.filter(project_title__contains=searched)
        return render(request, 'project/search.html', context={"searched": searched, "projects": projects})

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

# def projects_index(request, tag_slug=None):
#     projects = Project.get_all_projects()
#     categories = Category.get_all_categories()
#     tag = None
#     if tag_slug:
#         tag = get_object_or_404(Tag, slug=tag_slug)
#         projects = Project.objects.filter(tags__in=[tag])
#     return render(request, 'project/index.html', context={"projects": projects, "categories": categories, "tag": tag})

def submit_review(request, project_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(project__id=project_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.rating = form.cleaned_data['rating']
                data.project_id = project_id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)  
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'project/show.html', {"project":project})

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)

    projects = Project.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'projects': projects,
    }
    return render(request, 'project/search.html', context)