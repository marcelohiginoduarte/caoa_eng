from django.shortcuts import render, redirect
from django.db.models import Sum
from .forms import CriarVendedorForms
from .models import ListaVendedores, VendaMensal
from datetime import datetime
from vendas.models import Venda
from django.contrib.auth.decorators import login_required, user_passes_test



def is_direcao(user):
    return user.groups.filter(name='direcao').exists()


@login_required
def ver_todos_vendedores(request):
    if not request.user.groups.filter(name='direcao').exists():
        return render(request, 'sem_acesso.html')

    MESES = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro',
    }

    ver_vendedores = ListaVendedores.objects.all()
    hoje = datetime.now()
    ano_atual = str(hoje.year)

    vendas_por_vendedor = {vendedor.nome: {} for vendedor in ver_vendedores}
    total_vendas_por_vendedor = {vendedor.nome: 0 for vendedor in ver_vendedores}
    total_comissao = {vendedor.nome: 0 for vendedor in ver_vendedores}

    total_geral_vendas = 0
    total_geral_comissao = 0

    for num_mes, nome_mes in MESES.items():
        for vendedor in ver_vendedores:
            total_vendas = Venda.objects.filter(
                vendedor=vendedor.id,
                status_venda='aprov_banc',
                mes=nome_mes,
                ano=ano_atual
            ).aggregate(total=Sum('valor'))['total'] or 0

            total_comissao_vendedor = Venda.objects.filter(
                vendedor=vendedor.id,
                status_pg_vendedor='real',
                mes=nome_mes,
                ano=ano_atual
            ).aggregate(total=Sum('comissao'))['total'] or 0

            vendas_por_vendedor[vendedor.nome][nome_mes] = {
                'total_vendas': total_vendas,
                'total_comissao': total_comissao_vendedor
            }

            total_vendas_por_vendedor[vendedor.nome] += total_vendas
            total_comissao[vendedor.nome] += total_comissao_vendedor

            total_geral_vendas += total_vendas
            total_geral_comissao += total_comissao_vendedor

    return render(request, 'vendas_mensais_vendedor.html', {
        'ver_vendedores': ver_vendedores,
        'meses': MESES.values(),
        'vendas_por_vendedor': vendas_por_vendedor,
        'total_vendas_por_vendedor': total_vendas_por_vendedor,
        'total_comissao': total_comissao,
        'total_geral_vendas': total_geral_vendas,
        'total_geral_comissao': total_geral_comissao,
    })



@login_required
def criar_vendedor(request):
    if not request.user.groups.filter(name='direcao').exists():
            return render(request, 'sem_acesso.html')
    if request.method == 'POST':
        form = CriarVendedorForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vertodosvendedores')
        
    else:
        form = CriarVendedorForms()
    
    return render(request, 'vendedores_cadastrar.html', {'form': form})

@login_required
def relatorio_vendas_mensais(request):
    vendas_mensais = VendaMensal.objects.order_by('-ano', '-mes')
    return render(request, 'relatorio_vendas_mensais.html', {'vendas_mensais': vendas_mensais})