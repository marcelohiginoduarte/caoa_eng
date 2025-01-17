from django.contrib import admin
from servico.views import home
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home_principal'),
    path('servico/', include('servico.urls')),
    path('vendas/', include('vendas.urls')),
]
