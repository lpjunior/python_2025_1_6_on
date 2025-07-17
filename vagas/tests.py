from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from vagas.models import Candidato, Empresa, Vaga

class CandidaturaAccessTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Usuário candidato
        self.candidato_user = User.objects.create_user(username='candidatoTest1', password='senha@123')
        self.candidato = Candidato.objects.create(
            user=self.candidato_user,
            nome='Luis',
            telefone='(21) 1234-5678',
            cidade='Rio de Janeiro'
        )

        # Usuário Empresa
        self.empresa_user = User.objects.create_user(username='empresaTest1', password='senha@123')
        self.empresa = Empresa.objects.create(
            user=self.empresa_user,
            nome_empresa='Empresa X',
            cnpj='12.345.678/0001-90'
        )

        # Vaga criada pela empresa
        self.vaga = Vaga.objects.create(
            titulo= 'Dev Python',
            descricao = 'Desenvolvedor Python com Django',
            nivel = 'junior',
            localidade = 'Remoto',
            salario = 4000.00,
            empresa = self.empresa
        )

        self.url_candidatura = reverse('candidatar', args=[self.vaga.pk])

    def test_candidato_acessa_formulario(self):
        self.client.login(username='candidatoTest1', password='senha@123')
        response = self.client.get(self.url_candidatura)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Candidatura')

    def test_empresa_acessa_formulario(self):
        self.client.login(username='empresaTest1', password='senha@123')
        response = self.client.get(self.url_candidatura)
        self.assertRedirects(response, reverse('vaga-list'))
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("perfil de candidato" in str(m) for m in messages))

    def test_usuario_nao_autenticado_redirecionado_para_login(self):
        response = self.client.get(self.url_candidatura)
        self.assertRedirects(response, f'/login/?next={self.url_candidatura}')


# Testes para garantir que apenas a empresa dona da vaga possa editar/excluir