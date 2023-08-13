# urls.py

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('obras/', include('obras.urls')),
    path('', include('dashboard.urls')),
    path('associacoes/', include('associacoes.urls')),
    path('chaining/', include('smart_selects.urls')),
    path('select2/', include('django_select2.urls')),
]

# Adicione isso no final do arquivo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
