from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Venda
from .forms import VendasExternasForms, Alterar_status_vendas
from django.views.generic import DeleteView, UpdateView
from django.core.paginator import Paginator
from lista_vendedores.models import ListaVendedores
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import joblib
import os
import pandas as pd
from django.views import View


MODELO_PATH = os.path.join('modelo_lm', 'modelo_previsao_valor.pkl')
ENCODER_PATH = os.path.join('modelo_lm', 'encoder_descricoes.pkl')

@login_required 
def CadastrarVenda(request):
    if request.method == 'POST':
        form = VendasExternasForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vendasporvendedor')
    else:
        form = VendasExternasForms()
    
    return render(request, 'vendascadastrar.html', {'form': form})

@login_required 
def vendas_vendedor_logado(request):
    query = request.GET.get('q', '')  
    if request.user.is_superuser or request.user.groups.filter(name='direcao').exists():
        vendas = Venda.objects.all()  
    else:
        try:
            vendedor = ListaVendedores.objects.get(nome=request.user.username)
        except ListaVendedores.DoesNotExist:
            return render(request, 'erro_vendedor.html', {'message': 'Vendedor não encontrado!'})

        vendas = Venda.objects.filter(vendedor=vendedor)

    if query:
        vendas = vendas.filter(
            Q(cliente__icontains=query) | Q(servico__icontains=query)
        )

    paginator = Paginator(vendas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'vendas_todas_vendedor.html',
        {
            'vendas': page_obj,
            'user_name': request.user.get_full_name() or request.user.username,
            'query': query,
            'is_admin': request.user.is_superuser,
        }
    )

@login_required 
def status_vendas(request, venda_id):
    venda = Venda.objects.get(id=venda_id)
    cliente = venda.cliente
    servico = venda.servico
    consumo = venda.consumo
    valor = venda.valor

    
    if not request.user.groups.filter(name='direcao').exists():
        return HttpResponseForbidden("Você não tem permissão para alterar o status da venda.")

    status_venda = get_object_or_404(Venda, id=venda_id)
    if request.method == 'POST':
        form = Alterar_status_vendas(request.POST, instance=status_venda)
        if form.is_valid():
            form.save()
            return redirect('vendasporvendedor')
    else:
        form = Alterar_status_vendas(instance=status_venda)
    
    return render(request, 'status_vendas.html', {
        'form': form,
        'cliente': cliente,
        'servico': servico,
        'consumo': consumo,
        'valor': valor
    })


def detalhe_vendas(request, id):
    venda_detalhe = get_object_or_404(Venda, id=id)
    
    data = {
        "cliente": venda_detalhe.cliente,
        "servico": venda_detalhe.servico,
        "telefone": venda_detalhe.telefone,
        "cidade": venda_detalhe.cidade,
        "consumo": venda_detalhe.consumo,
        "email": venda_detalhe.email,
        "vendedor": venda_detalhe.vendedor.nome if venda_detalhe.vendedor else None, 
        "mes": venda_detalhe.mes,
        "ano": venda_detalhe.ano,
        "valor": venda_detalhe.formatar_valor() if hasattr(venda_detalhe, 'formatar_valor') else venda_detalhe.valor,
        "comissao": venda_detalhe.formatar_comissao() if hasattr(venda_detalhe, 'formatar_comissao') else venda_detalhe.comissao,
        "status_venda": venda_detalhe.status_venda,
        "status_pagamento": venda_detalhe.status_pg_vendedor,
        "foto_documento": venda_detalhe.foto_documento.url if venda_detalhe.foto_documento else None,
        "foto_endereco": venda_detalhe.foto_endereco.url if venda_detalhe.foto_endereco else None,
        "foto_contracheque": venda_detalhe.foto_contracheque.url if venda_detalhe.foto_contracheque else None,
    }
    
    return JsonResponse(data)


class AtualizarVenda(UpdateView):
    model = Venda
    template_name = 'venda_atualizar.html'
    form_class = VendasExternasForms
    success_url = reverse_lazy('vendasporvendedor')


class DeletarVenda(DeleteView):
    model = Venda
    template_name = 'venda__confirm_delete.html'
    success_url = reverse_lazy('vendasporvendedor')


class PreOrcamentoView(View):
    def get(self, request):
        return render(request, 'pre_orcamento.html')

    def post(self, request):
        descricao = request.POST.get('descricao')
        nome_projeto = request.POST.get('nome_projeto')
        tipo_servico = request.POST.get('tipo_servico')

        modelo = joblib.load(MODELO_PATH)
        encoder = joblib.load(ENCODER_PATH)

        df = pd.DataFrame([{
            'descricao': descricao,
            'nome_projeto': nome_projeto,
            'tipo_servico': tipo_servico
        }])
        x_encoded = encoder.transform(df)

        valor_previsto = modelo.predict(x_encoded)[0]

        return render(request, 'pre_orcamento.html', {
            'valor_previsto': round(valor_previsto, 2),
            'descricao': descricao,
            'nome_projeto': nome_projeto,
            'tipo_servico': tipo_servico
        })