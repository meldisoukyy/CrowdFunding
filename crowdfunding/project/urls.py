from django.urls import path
from . import views as vi

urlpatterns = [
    path('', vi.ProjectHome.as_view(), name='project_home'),
    path('create/', vi.CreateProject.as_view(), name='create_project'),
    path('update/<int:pk>', vi.UpdateProject.as_view(), name='update_project'),
    path('delete/<int:pk>', vi.DeleteProject.as_view(), name='delete_project'),
    path('view/<int:pk>', vi.ViewProject.as_view(), name='view_project'),
    # path('tag/<slug:tag_slug>', vi.projects_index, name="project_by_tag"),
    path('tag/<slug:slug>/', vi.tagged, name="tagged"),
    path('submit_review/<int:project_id>/', vi.submit_review, name='submit_review')
]