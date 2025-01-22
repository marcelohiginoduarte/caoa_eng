from .models import Servico

def valor_dash(request):
    total_valor_vendido = Servico.objects.aaggregate(total=Servico.Sum('valor_empreendimento'))['total'] or 0
    context = {'total_valor_vendido':total_valor_vendido}