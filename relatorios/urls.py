from django.urls import path
from . import views


urlpatterns = [
    path('gerar/relatorio/servico', views.gerar_relatorio_vendas_por_mes, name='gerar_relatorio'),
]