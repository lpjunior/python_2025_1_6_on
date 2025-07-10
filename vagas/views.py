from datetime import datetime

import cloudinary.uploader
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View

from vagas.forms import VagaForm, CandidaturaForm
from .models import Vaga, Candidatura

class VagaListView(ListView):
    model = Vaga
    template_name = 'vagas/vaga_list.html'
    context_object_name = 'vagas'

class VagaCreateView(CreateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'vagas/vaga_form.html'
    success_url = reverse_lazy('vaga-list')

class VagaUpdateView(UpdateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'vagas/vaga_form.html'
    success_url = reverse_lazy('vaga-list')

class VagaDeleteView(DeleteView):
    model = Vaga
    template_name = 'vagas/vaga_confirm_delete.html'
    success_url = reverse_lazy('vaga-list')

class CandidaturaCreateView(View):
    def get(self, request, vaga_id):
        form = CandidaturaForm()
        return render(request, 'vagas/candidatura_form.html', {'form': form})

    def post(self, request, vaga_id):
        form = CandidaturaForm(request.POST, request.FILES)
        vaga = get_object_or_404(Vaga, id=vaga_id)
        if form.is_valid():
            Candidatura.objects.create(
                vaga=vaga,
                nome=form.cleaned_data.get('nome'),
                email=form.cleaned_data.get('email'),
                curriculo=form.cleaned_data.get('curriculo'),
            )

            date_prefix = datetime.now().strftime('%Y_%m_%d')
            filename = f'{date_prefix}_curriculo_{form.cleaned_data.get('nome')}'

            cloudinary.uploader.upload(
                file=form.cleaned_data.get('curriculo'),
                asset_folder='curriculos',
                public_id=filename,
                override=True,
                resource_type="raw"
            )

            send_mail(
                subject='Confirmação de candidatura',
                message=f'Olá {form.cleaned_data.get('nome')}, sua candidatura foi recebida!',
                from_email='contato@empregasenac.com.br',
                recipient_list=[form.cleaned_data.get('email')],
                fail_silently=True,
            )

            return redirect('vaga-list')
        return render(request, 'vagas/candidatura_form.html', {'form': form})