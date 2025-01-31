from django.shortcuts import render
from django.db.models import Sum, Count
from datetime import datetime
from servico.models import Servico
from vendas.models import Venda
from lista_vendedores.models import ListaVendedores


def gerar_relatorio(request):
    relatorio = (Servico.objects
                 .values('mes', 'tipo_serviço', 'vendedor__nome')
                 .annotate(
                     total_valor_empreendimento=Sum('valor_empreendimento'),
                     total_valor_custos=Sum('valor_custos'),
                     total_valor_lucro=Sum('valor_lucro')
                 )
                 .order_by('vendedor__nome', 'mes'))

    vendedores = {}
    for item in relatorio:
        vendedor_nome = item['vendedor__nome']
        mes = item['mes']
        if vendedor_nome not in vendedores:
            vendedores[vendedor_nome] = {
                'Janeiro': 0, 'Fevereiro': 0, 'Março': 0, 'Abril': 0, 'Maio': 0,
                'Junho': 0, 'Julho': 0, 'Agosto': 0, 'Setembro': 0, 'Outubro': 0,
                'Novembro': 0, 'Dezembro': 0
            }
        vendedores[vendedor_nome][mes] = item['total_valor_empreendimento']

    return render(request, 'relatorios_servicos.html', {'vendedores': vendedores})


def gerar_relatorio_tipo_servico(request):
    relatorio = (Servico.objects
                 .values('mes', 'tipo_serviço')
                 .annotate(
                     total_valor_empreendimento=Sum('valor_empreendimento'),
                     total_valor_custos=Sum('valor_custos'),
                     total_valor_lucro=Sum('valor_lucro')
                 )
                 .order_by('tipo_serviço', 'mes'))

    tipo_servico = {}
    for item in relatorio:
        tipo_nome = item['tipo_serviço']
        mes = item['mes']
        
        if tipo_nome not in tipo_servico:
            tipo_servico[tipo_nome] = {
                'Janeiro': 0, 'Fevereiro': 0, 'Março': 0, 'Abril': 0, 'Maio': 0,
                'Junho': 0, 'Julho': 0, 'Agosto': 0, 'Setembro': 0, 'Outubro': 0,
                'Novembro': 0, 'Dezembro': 0
            }
        
        tipo_servico[tipo_nome][mes] = item['total_valor_empreendimento']

    return render(request, 'relatorios_tipo_servico.html', {'tipo_servico': tipo_servico})

