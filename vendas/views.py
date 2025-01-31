from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Venda
from .forms import VendasExternasForms, Alterar_status_vendas
from django.views.generic import DeleteView, UpdateView
from django.core.paginator import Paginator
from lista_vendedores.models import ListaVendedores
from django.db.models import Q

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
    query = request.GET.get('q', '')  
    if request.user.is_superuser:
        vendas = Venda.objects.all()  
    else:
        vendedor = get_object_or_404(ListaVendedores, nome=request.user.username)
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
        "cidade": venda_detalhe.cidade,
        "consumo": venda_detalhe.consumo,
        "email": venda_detalhe.email,
        "vendedor": venda_detalhe.vendedor.id if venda_detalhe.vendedor else None, 
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