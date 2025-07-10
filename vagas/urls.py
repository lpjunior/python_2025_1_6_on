from django.urls import path

from . import views

urlpatterns = [
    path('', views.VagaListView.as_view(), name='vaga-list'),
    path('vagas/nova/', views.VagaCreateView.as_view(), name='vaga-create'),
    path('vagas/<int:pk>/editar/', views.VagaUpdateView.as_view(), name='vaga-update'),
    path('vagas/<int:pk>/excluir/', views.VagaDeleteView.as_view(), name='vaga-delete'),
    path('candidatar/<int:vaga_id>/', views.CandidaturaCreateView.as_view(), name='candidatar'),
]

from django.contrib.auth.views import LoginView, LogoutView

urlpatterns += [
    path('login/', LoginView.as_view(template_name='vagas/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout')
]