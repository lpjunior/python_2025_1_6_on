from vagas.models import Empresa, Candidato

def perfil_usuario(request):
    user = request.user
    is_empresa = False
    is_candidato = False

    if user.is_authenticated:
        is_empresa = Empresa.objects.filter(user=user).exists()
        is_candidato = Candidato.objects.filter(user=user).exists()

    return {
        'is_empresa': is_empresa,
        'is_candidato': is_candidato
    }