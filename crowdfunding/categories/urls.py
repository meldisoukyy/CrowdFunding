from django.urls import path, include
from .views import CreateCategory, UpdateCategory

urlpatterns = [
    path('create/', CreateCategory.as_view(), name='create_category'),
    path('update/<int:pk>', UpdateCategory.as_view(), name='update_category'),
]
