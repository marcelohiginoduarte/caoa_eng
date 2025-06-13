from django.db import models
from django.contrib.auth.models import User

class Lead(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    origem = models.CharField(max_length=100, choices=[
        ("site", "Site"),
        ("indicacao", "Indicação"),
        ("rede_social", "Rede Social"),
        ("outro", "Outro"),
    ])
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ("novo", "Novo"),
        ("em_contato", "Em Contato"),
        ("proposta", "Proposta Enviada"),
        ("fechado", "Fechado"),
        ("perdido", "Perdido"),
    ], default="novo")
    vendedor_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome

class Proposta(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    consumo_medio_kwh = models.DecimalField(max_digits=8, decimal_places=2)
    potencia_kwp = models.DecimalField(max_digits=6, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    payback_estimado_anos = models.DecimalField(max_digits=5, decimal_places=2)
    pdf_proposta = models.FileField(upload_to='propostas/', blank=True, null=True)
    data_envio = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Proposta - {self.lead.nome}"

class Projeto(models.Model):
    proposta = models.OneToOneField(Proposta, on_delete=models.CASCADE)
    aprovado = models.BooleanField(default=False)
    data_aprovacao = models.DateField(blank=True, null=True)
    engenheiro_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='engenheiro')
    data_instalacao_prevista = models.DateField(blank=True, null=True)
    data_instalacao_real = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Projeto - {self.proposta.lead.nome}"

class Suporte(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    assunto = models.CharField(max_length=200)
    descricao = models.TextField()
    data_abertura = models.DateTimeField(auto_now_add=True)
    resolvido = models.BooleanField(default=False)

    def __str__(self):
        return f"Suporte - {self.projeto}"

