from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('project/', include('project.urls')),
    path('account/', include('account.urls')),
    path('password/', include('password.urls')),
    path('comment/', include('comment.urls')),
    path('donation/', include('donation.urls')),
    # path('category/', include('categories.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
