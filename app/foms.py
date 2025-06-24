from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta: # classe interna para configuração do formulário
        model = Book # qual o model será utilizado como base
        fields = ['title', 'author', 'pages', 'published_date'] # quais campos do model serão expostos no formulário
        widgets = {
            'published_date' : forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }
        labels = {
            'title' : 'Título do Livro',
            'author' : 'Autor do Livro',
            'pages' : 'Número de páginas',
            'published_date' : 'Data de Publicação',
        }
