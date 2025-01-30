from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from .forms import CadastrarServicoforms
from .models import Servico
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.utils.timezone import now
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


@login_required 
def home(request):
    return render(request, 'index.html')

@login_required
def dash_servico(request):

    Mes = [
        ('January', 'Jan'),
        ('February', 'Feb'),
        ('March', 'Mar'),
        ('April', 'Apr'),
        ('May', 'May'),
        ('June', 'Jun'),
        ('July', 'Jul'),
        ('August', 'Aug'),
        ('September', 'Sep'),
        ('October', 'Oct'),
        ('November', 'Nov'),
        ('December', 'Dec'),
    ]
    
    data_atual = now()
    mes_atual = Mes[data_atual.month -1][1]
    ano_atual = data_atual.year
    total_valor_vendido_mes = Servico.objects.filter(
        ano=ano_atual, 
        mes=mes_atual,
    ).aggregate(total=Sum('valor_empreendimento'))['total'] or 0
    total_valor_vendido = Servico.objects.aggregate(total=Sum('valor_empreendimento'))['total'] or 0
    context = {'total_valor_vendido':total_valor_vendido,
            'total_valor_vendido_mes':total_valor_vendido_mes,
            
            }
    return render(request, 'home.html', context)

def cadastrar_servico(request):
    
    if request.method == 'POST':
        form = CadastrarServicoforms(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('todos_servicos') 
    else:
        form = CadastrarServicoforms()

    return render(request, 'servico_cadastrar.html', {'form': form})

def todos_servicos(request):
    todo_servico = Servico.objects.all()
    return render(request, 'servico_todos.html', {'todo_servico': todo_servico})


def editar_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    if request.method == 'POST':
        form = CadastrarServicoforms(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect ('todos_servicos')
    else:
        form = CadastrarServicoforms(instance=servico)
    return render(request, 'servico_editar.html', {'form': form})


class DeletarServico(DeleteView):
    model = Servico
    template_name = 'servico__confirm_delete.html'
    success_url = reverse_lazy('todos_servicos')


def detalhes_servico_json(request, id):
    ver_detalhe_servico = get_object_or_404(Servico, id=id)

    data = {
        'cliente': ver_detalhe_servico.cliente,
        'telefone': ver_detalhe_servico.telefone,
        'tipo_serviço': ver_detalhe_servico.tipo_serviço,
        'status': ver_detalhe_servico.status,
        'valor_empreendimento': ver_detalhe_servico.valor_empreendimento,
        'valor_custos': ver_detalhe_servico.valor_custos,
        'valor_lucro': ver_detalhe_servico.valor_lucro,
        'email': ver_detalhe_servico.email,
        'mes': ver_detalhe_servico.mes,
        'ano': ver_detalhe_servico.ano,
        'foto_documento': ver_detalhe_servico.foto_documento.url if ver_detalhe_servico.foto_documento else None,
        'comoprovante_endereco': ver_detalhe_servico.comoprovante_endereco.url if ver_detalhe_servico.comoprovante_endereco else None,
        'comoprovante_renda': ver_detalhe_servico.comoprovante_renda.url if ver_detalhe_servico.comoprovante_renda else None,
    }

    return JsonResponse(data)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("login.html")
        else:
            messages.error(request, "Usuário ou senha incorretos")

    return render(request, "login.html")


def logout(request):
    logout(request)
    return redirect("login")