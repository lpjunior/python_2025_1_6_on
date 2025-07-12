from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('vagas', views.VagaListView.as_view(), name='vaga-list'),
    path('vagas/nova/', views.VagaCreateView.as_view(), name='vaga-create'),
    path('vagas/<int:pk>/editar/', views.VagaUpdateView.as_view(), name='vaga-update'),
    path('vagas/<int:pk>/excluir/', views.VagaDeleteView.as_view(), name='vaga-delete'),
    path('candidatar/<int:vaga_id>/', views.CandidaturaCreateView.as_view(), name='candidatar'),
]

from .views import CandidatoSignUpView, EmpresaSignUpView

urlpatterns += [
    path('signup/candidato/', CandidatoSignUpView.as_view(), name='signup_candidato'),
    path('signup/empresa/', EmpresaSignUpView.as_view(), name='signup_empresa'),
]

from django.contrib.auth.views import LoginView, LogoutView

urlpatterns += [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]