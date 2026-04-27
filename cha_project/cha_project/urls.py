from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
    path('departments/', include('departments.urls')),
    path('emergency/', include('emergency.urls')),
    path('documents/', include('documents.urls')),
    path('api/v1/', include('cha_project.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
