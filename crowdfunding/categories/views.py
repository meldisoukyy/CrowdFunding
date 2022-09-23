from urllib import request
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from .models import Category

# Create your views here.
class CreateCategory(CreateView):
    model = Category
    fields = '__all__'
    template_name: str = 'category/create.html'

    def get_success_url(self) :
        return reverse('project_home')

class UpdateCategory(UpdateView):
    model = Category
    fields = '__all__'
    template_name: str = 'category/update.html'

    def get_success_url(self) :
        return reverse('project_home')