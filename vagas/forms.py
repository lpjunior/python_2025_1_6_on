from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Vaga

class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = [ 'titulo', 'nivel', 'localidade', 'salario', 'descricao' ]
        labels = {
            'titulo' : 'Título',
            'nivel' : 'Nível',
            'salario' : 'Salário',
            'descricao' : 'Descrição',
        }

class CandidaturaForm(forms.Form):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    curriculo = forms.FileField()


class CandidatoSignUpForm(UserCreationForm):
    nome = forms.CharField(max_length=100)
    telefone = forms.CharField(max_length=20)
    cidade = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EmpresaSignUpForm(UserCreationForm):
    nome_empresa = forms.CharField(max_length=200)
    cnpj = forms.CharField(max_length=18)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']