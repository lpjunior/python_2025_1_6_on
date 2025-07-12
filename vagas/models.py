from django.contrib.auth.models import User
from django.db import models

NIVEIS = (
    ('estagio', 'Estágio'),
    ('trainner', 'Trainner'),
    ('junior', 'Júnior'),
    ('pleno', 'Pleno'),
    ('senior', 'Sênior'),
)

class Vaga(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    nivel = models.CharField(max_length=10, choices=NIVEIS)
    localidade = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    empresa = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.nivel}"

class Candidatura(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    curriculo = models.FileField(upload_to='curriculos/')
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.vaga}"

class Candidato(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    cidade = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_empresa = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18)

    def __str__(self):
        return self.nome_empresa