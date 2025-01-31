from django.urls import path
from . import views


urlpatterns = [
    path('gerar/relatorio/servico', views.gerar_relatorio, name='gerar_relatorio'),
]