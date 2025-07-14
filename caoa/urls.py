from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', include('servico.urls')),
    path('vendas/', include('vendas.urls')),
    path('vendedor', include('lista_vendedores.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('despesas/', include('acompanhamentosfinanceiroprojeto.urls')),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)