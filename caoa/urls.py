from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from servico.views import home
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home_principal'),
    path('servico/', include('servico.urls')),
    path('vendas/', include('vendas.urls')),
    path('vendedor', include('lista_vendedores.urls')),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)