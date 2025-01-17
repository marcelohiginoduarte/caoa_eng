from django.shortcuts import render
from .models import Venda
from .forms import VendasExternasForms


def CadastrarVenda(request):

    if request.method == 'POST':
        form = VendasExternasForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return ('todasvendas')
    else:
        form = VendasExternasForms()
    
    return render(request, 'vendascadastrar.html', {'form': form})
