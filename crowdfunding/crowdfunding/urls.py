from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from project.views import LandingPage


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", LandingPage.as_view(), name="landing_page"),
    path('project/', include('project.urls')),
    path('account/', include('account.urls')),
    path('password/', include('password.urls')),
    path('donation/', include('donation.urls')),
    # path('category/', include('categories.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
