from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from servico.views import home
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home_principal'),
    path('servico/', include('servico.urls')),
    path('vendas/', include('vendas.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)