from django.contrib import messages
from django.shortcuts import redirect
from .models import Empresa, Vaga, Candidato


class EmpresaRequiredMixin:
    """ Mixin para restringir acesso a usuarios com perfil de Empresas. """

    def dispatch(self, request, *args, **kwargs):
        empresa = Empresa.objects.filter(user=self.request.user).first()
        if not empresa:
            messages.error(self.request, "Apenas usuários com perfil de empresa podem acessar está página.")
            return redirect('home')
        request.empresa_logada = empresa
        return super().dispatch(request, *args, **kwargs)

class VagaOwnerRequiredMixin:
    """
    Garante que a vaga acessada pertence a empresa logada.
    Deve ser usado com views que recebem 'pk' como parametro.
    """

    def dispatch(self, request, *args, **kwargs):
        vaga = Vaga.objects.filter(pk=kwargs.get('pk'), empresa=request.empresa_logada).first()
        if not vaga:
            messages.error(request, "Você não tem permissão para gerenciar esta vaga.")
            return redirect('vaga-list')
        return super().dispatch(request, *args, **kwargs)

class CandidatoRequiredMixin:
    """ Mixin para restringir acesso a usuarios com perfil de Candidato. """

    def dispatch(self, request, *args, **kwargs):
        if not Candidato.objects.filter(user=request.user).exists():
            messages.error(request, "Apenas usuários com perfil de candidato podem acessar está página.")
            return redirect('vaga-list')
        return super().dispatch(request, *args, **kwargs)