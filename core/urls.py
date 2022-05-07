from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include("homepage.urls")),
    path('api/v1/', include("api_backend.urls")),
    path('database-projects', include('database_projects.urls')),
    path('website-projects/', include('website_projects.urls'))
]

urlpatterns += static(settings.IMAGES_URL, document_root=settings.IMAGES_ROOT)
