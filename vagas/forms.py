from django import forms

from .models import Vaga


class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = [ 'titulo', 'descricao', 'nivel', 'localidade', 'salario' ]

class CandidaturaForm(forms.Form):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    curriculo = forms.FileField()