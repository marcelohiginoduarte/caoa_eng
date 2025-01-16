from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('servico/dash', views.dash_servico, name='dash_servico'),
    path('servicocadastrar/', views.cadastrar_servico, name='cadastrar_servicos'),
    path('servicovertodos/', views.todos_servicos, name='todos_servicos'),
    path('servicoeditar/<int:servico_id>', views.editar_servico, name='editar_servico'),
    
]