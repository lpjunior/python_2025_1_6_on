import json
import platform
import smtplib
import socket
from datetime import datetime

from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from app.foms import BookForm, ContactForm
from app.mixins import JsonableResponseMixin
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

class BookUpdateView(JsonableResponseMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "app/book_form.html"
    pk_url_kwarg = "book_id"
    success_url = reverse_lazy('book_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.content_type == 'application/json':
            try:
                data = json.loads(self.request.body)
            except json.JSONDecodeError:
                data = {}
            # Substitui 'data' pelo JSON
            kwargs['data'] = data
            # Remove 'files' se existir
            kwargs.pop('files', None)
        return kwargs

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

class BookDeleteView(DeleteView):
    model = Book
    template_name = "app/book_confirm_delete.html"
    pk_url_kwarg = "book_id"
    success_url = reverse_lazy('book_list')

def contact_view(request):
    form = ContactForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        file = form.cleaned_data.get('attachment')

        if file:
            default_storage.save(f'uploads/{file.name}', file)

        smtplib.SMTP.debuglevel = 1

        email_message = EmailMessage(
            subject=f'Contato de {name}',
            body=message,
            from_email=email,
            to=['aula.sendmail@gmail.com'],
        )

        if file:
            content_type = file.content_type
            email_message.attach(file.name, file.read(), content_type)

        email_message.send()

        # Simula envio
        context = {'success': True, 'name': name }

        return render(request, 'app/contact.html', context)
    return render(request, 'app/contact.html', {'form': form})