from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Venda
from .forms import VendasExternasForms, Alterar_status_vendas


def CadastrarVenda(request):
    if request.method == 'POST':
        form = VendasExternasForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vendasporvendedor')
    else:
        form = VendasExternasForms()
    
    return render(request, 'vendascadastrar.html', {'form': form})


def vendas_vendedor_logado(request):
    vendas = Venda.objects.filter(vendendor=request.user.username)
    return render(request, 'vendas_todas_vendedor.html', {'vendas': vendas, 'user_name': request.user.get_full_name() or request.user.username})



def status_vendas(request, venda_id):
    venda = Venda.objects.get(id=venda_id)
    cliente = venda.cliente
    servico = venda.servico
    consumo = venda.consumo
    valor = venda.valor


    status_venda = get_object_or_404(Venda, id=venda_id)
    if request.method == 'POST':
        form = Alterar_status_vendas(request.POST, instance=status_venda)
        if form.is_valid():
            form.save()
            return redirect ('vendasporvendedor')
    else:
        form = Alterar_status_vendas(instance=status_venda)
    return render(request, 'status_vendas.html', {'form': form,
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
        "consumo": venda_detalhe.consumo,
        "valor_empreendimento": venda_detalhe.formatar_valor,
        "comissao": venda_detalhe.formatar_comissao,
        "status_venda": venda_detalhe.status_venda,
        "status_pagamento": venda_detalhe.status_pg_vendedor,
    }
    return JsonResponse(data)