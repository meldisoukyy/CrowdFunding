from django.urls import path
from . import views as vi

urlpatterns = [
    path('create/', vi.create_project, name='create_project'),
]