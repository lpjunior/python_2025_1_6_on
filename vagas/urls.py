from django.contrib.auth.views import LoginView, LogoutView
from .views import CandidatoSignUpView, EmpresaSignUpView, DashboardEmpresaView, DashboardCandidatoView
from django.urls import path
from . import views

# rota padrão
urlpatterns = [
    path('', views.HomeView.as_view(), name='home')
]

# rota de vagas
urlpatterns += [
    path('vagas', views.VagaListView.as_view(), name='vaga-list'),
    path('vagas/nova/', views.VagaCreateView.as_view(), name='vaga-create'),
    path('vagas/<int:pk>/editar/', views.VagaUpdateView.as_view(), name='vaga-update'),
    path('vagas/<int:pk>/excluir/', views.VagaDeleteView.as_view(), name='vaga-delete'),
]

# rota de candaturas
urlpatterns += [
    path('candidatar/<int:vaga_id>/', views.CandidaturaCreateView.as_view(), name='candidatar'),
    path('candidaturas/recebidas/', views.CandidaturasRecebidasView.as_view(), name='candidaturas-recebidas'),
]

# rota de signup
urlpatterns += [
    path('signup/candidato/', CandidatoSignUpView.as_view(), name='signup_candidato'),
    path('signup/empresa/', EmpresaSignUpView.as_view(), name='signup_empresa'),
]

# rota de autenticação
urlpatterns += [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]

# rota dashboard
urlpatterns += [
    path('dashboard/empresa', DashboardEmpresaView.as_view(), name='dashboard-empresa'),
    path('dashboard/candidato', DashboardCandidatoView.as_view(), name='dashboard-candidato'),
]