import json
import platform
import socket
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from app.foms import BookForm
from app.models import Person, Book


# View 1 - Hello World (FBV)
def hello_view(request):
    response = { "message": "Hello, World!" }
    return JsonResponse(response)

# View 1 - Hello World (CBV)
class BaseHelloView(View):
    base_message = "Hello, World from CBV!"

    def get(self, request):
        return JsonResponse({
            'message': f'{self.base_message} - {datetime.now()}!'
        })

class HelloWorldView(BaseHelloView):
    base_message = "Hello, World!"

class ServerInfoView(View):
    def get(self, request):
        hostname = socket.gethostname()
        python_version = platform.python_version()
        return JsonResponse({
            'python_version': python_version,
            'hostname': hostname
        })

class WelcomeView(TemplateView):
    template_name = "app/welcome.html" #<project_root>/templates/app/welcome.html

    def get_context_data(self, **kwargs): #sobreescrita
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name', 'Visitante')
        return context

class PeopleView(View):
    def get(self, request):
        people = Person.objects.all() # SELECT * FROM person
        data = [{ 'name': p.name, 'age': p.age } for p in people]
        return JsonResponse({'people': data})

# ---- x ---- x ---- x ---- x ---- x ---- x ---- x ---- x ---- x ----

class BookListJsonView(View):
    def get(self, request):
        books = Book.objects.all().values()
        return JsonResponse(list(books), safe=False)

class BookListView(ListView):
    model = Book
    template_name = "app/book_list.html"
    context_object_name = "books"

class BookGetView(DetailView):
    model = Book
    template_name = "app/book_detail.html"
    context_object_name = "book"
    pk_url_kwarg = "book_id"

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = "app/book_form.html"
    success_url = reverse_lazy('book_list')  # redireciona após o cadastro

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "app/book_form.html"
    pk_url_kwarg = "book_id"
    success_url = reverse_lazy('book_list')

class BookDeleteView(DeleteView):
    model = Book
    template_name = "app/book_confirm_delete.html"
    pk_url_kwarg = "book_id"
    success_url = reverse_lazy('book_list')