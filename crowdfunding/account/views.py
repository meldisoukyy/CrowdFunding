from pipes import Template
from unicodedata import category
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import DetailView, TemplateView
from django.contrib.auth import authenticate, login
from .forms import UserForm
from .models import User
from .tokens import account_activation_token
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import RegisterForm, EditProfileForm
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
import django
from project.models import Project
from donation.models import Donation
from categories.models import Category
django.utils.encoding.force_text = force_str


def socialHomeView(request):
    return render(request, 'product/home.html')


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            form.cleaned_data.get('username')
            current_site = get_current_site(request)
            mail_subject = 'Please verify your registration in CrowdFunding'
            message = render_to_string(
                'acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
            )
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'registration/check_mail.html')

        else:
            print('Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {'form': form}
            return render(request, 'registration/register.html', context)

    return render(request, 'registration/register.html', {})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(reverse('login')) 
    else:
        return HttpResponse('Activation link is invalid!')


def signin(request):
    if request.method != "POST":
        form = UserForm()
        return render(request, 'registration/login.html', {'form': form})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is None:
            form = UserForm()
            return render(request, 'registration/login.html', {'form': form, 'error': 'invalid username or password'})
        login(request, user)
        return redirect('project_home')

class ViewProfile(DetailView):
    model = User
    template_name: str = 'account/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'projects': Project.objects.filter(created_by=self.kwargs['pk']),
        })
        return context

class ViewProfileDonations(DetailView):
    model = User
    template_name: str = 'account/view-donations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'donations': Donation.objects.filter(user=self.kwargs['pk'])
        })
        return context

class UpdateAccountView(UpdateView):
    form_class = EditProfileForm
    template_name = 'account/edit.html'
    model = User
    context_object_name = "object"

    def post(self, request, *args, **kwargs):
        if 'delete_account' in request.POST.keys():
            user_id = self.kwargs['pk']
            user = User.objects.filter(pk = user_id)
            user.delete()
            return redirect('/')
        else:
            return super().post(self, request, *args, **kwargs)

class Dashboard(TemplateView):
    model = Category 
    template_name = 'account/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'projects': Project.objects.order_by('id'),
            'categories': Category.objects.order_by('id')
        })
        return context

    def post(self, request, *args, **kwargs):
        if 'delete_project' in request.POST.keys():
            project_id = self.kwargs['pk']
            try:
                project = Project.objects.filter(pk = project_id)
            except: 
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            project.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        elif 'delete_category' in request.POST.keys():
            category_id = self.kwargs['pk']
            try:
                category = Category.objects.filter(pk = category_id)
            except: 
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            category.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return super().post(self, request, *args, **kwargs)


def feature_it(request):
    project = get_object_or_404(Project, pk = request.POST['project'])
    project.is_featured = True
    project.save()
    return redirect(reverse('project_home'))