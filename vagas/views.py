from datetime import datetime

import cloudinary.uploader
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView

from vagas.forms import VagaForm, CandidaturaForm, CandidatoSignUpForm, EmpresaSignUpForm
from .mixins import EmpresaRequiredMixin, VagaOwnerRequiredMixin, CandidatoRequiredMixin
from .models import Vaga, Candidatura, Candidato, Empresa


class VagaListView(ListView):
    model = Vaga
    template_name = 'vagas/vaga_list.html'
    context_object_name = 'vagas'

    def get_paginate_by(self, queryset):
        try:
            return int(self.request.GET.get('por_pagina', 10))
        except (TypeError, ValueError):
            return 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        user = self.request.user
        qs = Vaga.objects.all().order_by('-criada_em')

        if user.is_authenticated and Empresa.objects.filter(user=user).exists():
            qs = qs.filter(empresa__user=user)

        if query:
           qs = qs.filter(
                Q(titulo__icontains=query) |
                Q(descricao__icontains=query) |
                Q(localidade__icontains=query)
           )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_authenticated = self.request.user.is_authenticated

        context['is_empresa'] = Empresa.objects.filter(user=self.request.user).exists() if is_authenticated else False
        context['is_candidato'] = Candidato.objects.filter(user=self.request.user).exists() if is_authenticated else False
        context['por_pagina'] = self.request.GET.get('por_pagina', 10)
        context['opcoes_por_pagina'] = ['5', '10', '20', '50', '100']
        context['query'] = self.request.GET.get('q', '')

        return context

class VagaCreateView(LoginRequiredMixin, EmpresaRequiredMixin, CreateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'vagas/vaga_form.html'
    success_url = reverse_lazy('vaga-list')

    def form_valid(self, form):
        # Associa automaticamente a vaga à empresa logada
        form.instance.empresa = self.request.empresa_logada
        return super().form_valid(form)

class VagaUpdateView(LoginRequiredMixin, EmpresaRequiredMixin, VagaOwnerRequiredMixin, UpdateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'vagas/vaga_form.html'
    success_url = reverse_lazy('vaga-list')

class VagaDeleteView(LoginRequiredMixin, EmpresaRequiredMixin, VagaOwnerRequiredMixin, DeleteView):
    model = Vaga
    template_name = 'vagas/vaga_confirm_delete.html'
    success_url = reverse_lazy('vaga-list')

class CandidaturaCreateView(LoginRequiredMixin, CandidatoRequiredMixin, View):
    def get(self, request, vaga_id):
        form = CandidaturaForm()
        return render(request, 'vagas/candidatura_form.html', {'form': form})

    def post(self, request, vaga_id):
        form = CandidaturaForm(request.POST, request.FILES)
        vaga = get_object_or_404(Vaga, id=vaga_id)
        if form.is_valid():
            curriculo_file = form.cleaned_data.get('curriculo')

            # Gera o nome do arquivo
            date_prefix = datetime.now().strftime('%Y_%m_%d')
            filename = f'{date_prefix}_curriculo_{form.cleaned_data.get('nome')}'

            # Upload no Cloudinary
            upload_result = cloudinary.uploader.upload(
                file=curriculo_file,
                asset_folder='curriculos',
                public_id=filename,
                override=True,
                resource_type="auto"
            )

            # Salva no banco
            Candidatura.objects.create(
                vaga=vaga,
                nome=form.cleaned_data.get('nome'),
                email=form.cleaned_data.get('email'),
                curriculo=upload_result.get('secure_url'),
            )

            # Envia email
            send_mail(
                subject='Confirmação de candidatura',
                message=f'Olá {form.cleaned_data.get('nome')}, sua candidatura foi recebida!',
                from_email='contato@empregasenac.com.br',
                recipient_list=[form.cleaned_data.get('email')],
                fail_silently=True,
            )

            return redirect('vaga-list')
        return render(request, 'vagas/candidatura_form.html', {'form': form})

class CandidaturasRecebidasView(LoginRequiredMixin, EmpresaRequiredMixin, ListView):
    model = Candidatura
    template_name = 'vagas/candidaturas_recebidas.html'
    context_object_name = 'candidaturas'
    paginate_by = 10

    def get_queryset(self):
        return Candidatura.objects.filter(
            vaga__empresa=self.request.empresa_logada
        ).select_related('vaga').order_by('-data_envio')

class CandidatoSignUpView(CreateView):
    model = User
    form_class = CandidatoSignUpForm
    template_name = 'registration/signup_candidato.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        Candidato.objects.create(
            user=self.object,
            nome=form.cleaned_data.get('nome'),
            telefone=form.cleaned_data.get('telefone'),
            cidade=form.cleaned_data.get('cidade'),
        )
        login(self.request, self.object)
        return response

class EmpresaSignUpView(CreateView):
    model = User
    form_class = EmpresaSignUpForm
    template_name = 'registration/signup_empresa.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        Empresa.objects.create(
            user=self.object,
            nome_empresa=form.cleaned_data.get('nome_empresa'),
            cnpj=form.cleaned_data.get('cnpj'),
        )
        login(self.request, self.object)
        return response

class HomeView(TemplateView):
    template_name = 'vagas/home.html'