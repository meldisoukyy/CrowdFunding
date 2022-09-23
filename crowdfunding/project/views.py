from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from multiprocessing import context
from unicodedata import category
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
from comment.models import Comment
from donation.models import Donation

from django.db.models import Sum, Count

from django.contrib.auth.mixins import (
LoginRequiredMixin,
UserPassesTestMixin # new
)


class LandingPage(ListView):
    model = Project
    template_name: str = 'project/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'top_projects': Project.objects.all().order_by('-project_review_ratio')[:6],
            'featured_projects': Project.objects.filter(is_featured = True).order_by('-project_created_date')[:5],
            'categories': Category.objects.all(),
            'donations_total': Donation.objects.count(),
            'projects_total': Project.objects.count(),
            'ratings_total': ReviewRating.objects.count(),
        })
        return context


class ProjectHome(LoginRequiredMixin,ListView):
    model = Project
    template_name: str = 'project/home.html'
    context_object_name = 'all_projects'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'latest_projects': Project.objects.order_by('-project_created_date')[:10],
            'featured_projects': Project.objects.filter(is_featured = True),
            'categories': Category.objects.order_by('name'),
            'tags': Tag.objects.all(),
        })
        return context

    def post(self, request, *args, **kwargs):
        searched = request.POST['searched']
        try:
            tag = Tag.objects.get(slug=searched)
            projects = Project.objects.filter(project_tags=tag)
        except:
            projects = Project.objects.filter(project_title__contains=searched)
        return render(request, 'project/search.html', context={"searched": searched, "projects": projects})

class ProjectHomeCategory(LoginRequiredMixin,ListView):
    model = Project
    template_name: str = 'project/home-category.html'
    context_object_name = 'all_projects'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'latest_projects': Project.objects.filter(project_category = self.kwargs['pk']).order_by('-project_created_date')[:10],
            'categories': Category.objects.order_by('name'),
        })
        return context
# Create


class CreateProject(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    form_class = ProjectForm
    template_name = 'project/create.html'
    extra_context = {"imageform": ImageForm()}
    # success_message: str = 'Object Created Successfully!'

    def get_success_url(self):
        return reverse('project_home')

    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST, request.FILES)
        files = request.FILES.getlist("image")
        if form.is_valid():
            f = form.save(commit=False)
            f.created_by = request.user
            f.save()
            form.save_m2m()
            for i in files:
                Image.objects.create(project=f, image=i)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Update


class UpdateProject(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/update.html'
    # extra_context = {"imageform": ImageForm()}
    # success_message: str = 'Object Updated Successfully!'

    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST, request.FILES)
        files = request.FILES.getlist("image")
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        if form.is_valid():
            if request.FILES['image']:
                images = Image.objects.filter(project=self.kwargs['pk'])
                images.delete()
            for i in files:
                Image.objects.create(project=project, image=i)
            return super().post(self, request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse('project_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imageform'] = ImageForm()
        return context

    def test_func(self): # new
        obj = self.get_object()
        return obj.created_by == self.request.user


# View
class ViewProject(DetailView):
    model = Project
    template_name: str = 'project/view.html'

    def get_context_data(self, **kwargs):
        category = Project.objects.filter(pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context.update({
            'images': Image.objects.filter(project=self.kwargs['pk']),
            'projects': Project.objects.all(),
        })
        return context

    def post(self, request, *args, **kwargs):
        handler = getattr(
            self,
            "post_{0}".format(self.request.POST.get(
                'type', '')), 
            self.post_operation_not_supported
        )
        return handler(request, args, **kwargs)

    def post_comment(self,request,*args, **kwargs):
        content = request.POST['content']
        Acomment = Comment()
        project = get_object_or_404(Project,pk = self.kwargs['pk'])
        Acomment.project = project
        Acomment.user = request.user
        Acomment.comment = content
        Acomment.save()
        return HttpResponseRedirect("/project/view/"+str(self.kwargs['pk']))

    def post_donate(self,request,*args, **kwargs):
        project = get_object_or_404(Project,pk = self.kwargs['pk'])
        if int(request.POST['amount']) == 0:
            messages.add_message(self.request, messages.INFO, 'You can not donate with zero')
            return HttpResponseRedirect("/project/view/"+str(self.kwargs['pk']))
        if int(request.POST['amount']) > int(project.project_total_target):
            messages.add_message(self.request, messages.INFO, 'You can not donate more than total target')
            return HttpResponseRedirect("/project/view/"+str(self.kwargs['pk']))
        if int(request.POST['amount']) + int(Donation.totalDonation(project)) > int(project.project_total_target):
            messages.add_message(self.request, messages.INFO, 'total donation will be higher than total target')
            return HttpResponseRedirect("/project/view/"+str(self.kwargs['pk']))

        amount = request.POST['amount']
        donate = Donation()
        project = get_object_or_404(Project,pk = self.kwargs['pk'])
        donate.project = project
        donate.user = request.user
        donate.amount = amount
        donate.save()

        return HttpResponseRedirect("/project/view/"+str(self.kwargs['pk']))
    
    def post_rate(self,request,*args, **kwargs):
        project = get_object_or_404(Project,pk = self.kwargs['pk'])
        data = ReviewRating()
        data.project = project
        data.rating = request.POST['rating']
        data.user = request.user
        data.save()
        project.project_review_ratio = project.averageReview()
        project.save()
        return HttpResponseRedirect("/project/view/"+str(self.kwargs['pk']))
    
    def post_operation_not_supported(self,request,*args, **kwargs):
        return render(request, "errors/403.html", {})

# Delete
class DeleteProject(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Project
    template_name: str = 'project/view.html'
    success_url = reverse_lazy('project_home')
    
    def test_func(self): # new
        obj = self.get_object()
        return obj.created_by == self.request.user



def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)

    projects = Project.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'projects': projects,
    }
    return render(request, 'project/search.html', context)
