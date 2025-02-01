from django.shortcuts import render
from django.db.models import Sum, Count, Q
from datetime import datetime
from servico.models import Servico
from vendas.models import Venda
from lista_vendedores.models import ListaVendedores
from .utilits import export_to_excel


def gerar_relatorio_vendas_por_mes(request):
    relatorio = (Servico.objects
                 .values('mes', 'tipo_serviço', 'vendedor__nome')
                 .annotate(
                     total_valor_empreendimento=Sum('valor_empreendimento'),
                     total_valor_custos=Sum('valor_custos'),
                     total_valor_lucro=Sum('valor_lucro')
                 )
                 .order_by('vendedor__nome', 'mes'))

    vendedores = {}
    totais_mes = {
        'Janeiro': 0, 'Fevereiro': 0, 'Março': 0, 'Abril': 0, 'Maio': 0,
        'Junho': 0, 'Julho': 0, 'Agosto': 0, 'Setembro': 0, 'Outubro': 0,
        'Novembro': 0, 'Dezembro': 0
    }

    for item in relatorio:
        vendedor_nome = item['vendedor__nome']
        mes = item['mes']
        valor_empreendimento = item['total_valor_empreendimento'] or 0

        if vendedor_nome not in vendedores:
            vendedores[vendedor_nome] = {
                'Janeiro': 0, 'Fevereiro': 0, 'Março': 0, 'Abril': 0, 'Maio': 0,
                'Junho': 0, 'Julho': 0, 'Agosto': 0, 'Setembro': 0, 'Outubro': 0,
                'Novembro': 0, 'Dezembro': 0
            }
        vendedores[vendedor_nome][mes] = valor_empreendimento
        totais_mes[mes] += valor_empreendimento

    headers = ['Vendedor', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio',
               'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    data = []
    for vendedor, meses in vendedores.items():
        row = [vendedor] + [meses[mes] for mes in headers[1:]]
        data.append(row)

    total_row = ['Total'] + [totais_mes[mes] for mes in headers[1:]]
    data.append(total_row)

    # Verifica se o parâmetro 'export' está definido como "true"
    if request.GET.get('export') == "true":
        return export_to_excel(data, headers, filename='relatorio_vendas.xlsx')

    return render(request, 'relatorios_servicos.html', {
        'vendedores': vendedores,
        'totais_mes': totais_mes,
        'data': data
    })


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


def gerar_relatorio(request):
    headers = ['Vendedor', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio',
                'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    data = [
        ['Vendedor A', 1000, 1500, 1200, 1300, 1100, 1600, 1700, 1400, 1500, 1800, 1900, 2000],
        ['Vendedor B', 900, 1400, 1100, 1200, 1000, 1500, 1600, 1300, 1400, 1700, 1800, 1900],
    ]
    
    
    total_row = ['Total', 1900, 2900, 2300, 2500, 2100, 3100, 3300, 2700, 2900, 3500, 3700, 3900]
    data.append(total_row)
    
    
    if request.GET.get('export') == "true":
        return export_to_excel(data, headers, filename='relatorio_vendas.xlsx')
    
    
    return render(request, 'relatorios_servicos.html', {
        'data': data,
    })

