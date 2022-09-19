from django.urls import path
from . import views as vi

urlpatterns = [
    path('', vi.ProjectHome.as_view(), name='project_home'),
    path('create/', vi.create_project, name='create_project'),
    path('update/<int:pk>', vi.UpdateProject.as_view(), name='update_project'),
    path('delete/<int:pk>', vi.DeleteProject.as_view(), name='delete_project'),
    path('view/<int:pk>', vi.ViewProject.as_view(), name='view_project'),
]