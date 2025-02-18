from django.urls import path
from . import views

urlpatterns = [
    path('servico/dash', views.dash_servico, name='dash_servico'),
    path('servico/entrada', views.entrada_principal, name='entrada_do_sistema'),
    path('servicocadastrar/', views.cadastrar_servico, name='cadastrar_servicos'),
    path('servicovertodos/', views.todos_servicos, name='todos_servicos'),
    path('servicoeditar/<int:servico_id>', views.editar_servico, name='editar_servico'),
    path('servico/<int:id>/detalhes', views.detalhes_servico_json, name='detalhe_servico'),
    path('servico/delete/<int:pk>', views.DeletarServico.as_view(), name='deletarservico'),
    path('servico/logouut', views.logout, name='logout'),
]