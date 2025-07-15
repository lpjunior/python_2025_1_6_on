from django.contrib import messages
from django.shortcuts import redirect
from .models import Empresa


class EmpresaRequiredMixin:
    """ Mixin para restringir acesso a usuarios com perfil de Empresas. """

    def dispatch(self, request, *args, **kwargs):
        empresa = Empresa.objects.filter(user=self.request.user).first()
        if not empresa:
            messages.error(self.request, "Apenas usuários com perfil de empresa podem acessar está página.")
            return redirect('home')
        request.empresa_logada = empresa
        return super().dispatch(request, *args, **kwargs)