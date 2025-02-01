from django.utils.timezone import now
from .models import Servico
from django.db.models import Sum, Count

def valor_dash(request):
    total_valor_vendido = Servico.objects.aggregate(total=Sum('valor_empreendimento'))['total'] or 0
    context = {'total_valor_vendido': total_valor_vendido}

def contar_servicos_mes():
    data_atual = now()
    mes_atual = data_atual.month
    ano_atual = data_atual.year

    total_servicos_mes = Servico.objects.filter(
        data_servico__year=ano_atual, 
        data_servico__month=mes_atual
    ).count()

    total_valor_vendido_mes = Servico.objects.filter(
        data_servico__year=ano_atual, 
        data_servico__month=mes_atual
    ).aggregate(total=Sum('valor_empreendimento'))['total'] or 0

    return total_servicos_mes, total_valor_vendido_mes