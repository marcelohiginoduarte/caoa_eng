from django.urls import path
from . import views

urlpatterns = [
    path('despesa/proheto', views.criar_despesa_projeto, name='criardespesaprojeto'),
]