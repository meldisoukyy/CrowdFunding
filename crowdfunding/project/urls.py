from django.urls import path
from . import views as vi

urlpatterns = [
    path('', vi.project, name='project'),
    path('create/', vi.CreateProject.as_view(), name='create_project'),
    path('update/', vi.update_project, name='update_project'),
    path('delete/<int:pk>', vi.delete_project, name='delete_project'),
    path('view/<int:pk>', vi.view_project, name='view_project'),
]