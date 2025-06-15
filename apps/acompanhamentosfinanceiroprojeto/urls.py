from django.urls import path
from . import views

urlpatterns = [
    path('despesa/projeto', views.criar_despesa_projeto, name='criardespesaprojeto'),
    path('despesa/todas', views.ver_despesas_projeto, name='criardespesaprojetotodas'),
    path('despesa/atualizar/<int:pk>', views.AtualizarCustos.as_view(), name='atualizar_custos'),
    path('despesa/deletar/<int:pk>', views.DeletarCustos.as_view(), name='deletar_custos'),
    path('gerar_relatorio/', views.gerar_relatorio, name='gerar_relatorio'),
    path('despestas/todas', views.gerar_varios_pdfs_zip, name='geratodasasdepesas'),
]