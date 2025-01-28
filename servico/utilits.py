from .models import Servico
from django.db.models import Sum

def valor_dash(request):
    total_valor_vendido = Servico.objects.aggregate(total=Sum('valor_empreendimento'))['total'] or 0
    context = {'total_valor_vendido': total_valor_vendido}