import  json
from django.http import JsonResponse

class JsonableResponseMixin:
    """
    Mixin para suportar requisições JSON (ideal para chamadas AJAX/API)
    combinando com as CBVs genéricas de formulário.
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)

        # Se o cliente aceitar HTML, retorna comportamento padrão
        if self.request.get_preferred_type(['text/html', 'application/json']) == 'text/html':
            return response

        # Senão, responde erros via JSON
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        response = super().form.valid(form)

        # Se o cliente aceitar HTML, retorna comportamento padrão
        if self.request.get_preferred_type(['text/html', 'application/json']) == 'text/html':
            return response

        # Senão, retorna JSON com o ID do objeto
        return JsonResponse({'pk', self.object.pk })
