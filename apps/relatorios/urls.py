from django.urls import path
from . import views


urlpatterns = [
    path('gerar/relatorio/vendas', views.gerar_relatorio_vendas_por_mes, name='gerar_relatorio_vendedor'),
    path('relatorios/gerar/relatorio/servico/', views.gerar_relatorio, name='gerar_relatorio'),
    path('gerar/relatorio/tipo_servico', views.gerar_relatorio_tipo_servico, name='gerar_relatorio_tipo_servico'),
]