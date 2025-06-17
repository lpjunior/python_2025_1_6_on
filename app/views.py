import platform
import socket
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from django.views import View
from django.views.generic import TemplateView
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

def book_list_json(request):
    books = Book.objects.all().values()
    return JsonResponse(list(books), safe=False)

def book_list(request):
    bookList = Book.objects.all()
    return render(request, "app/book_list.html", { "books": bookList })

def book_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        pages = request.POST.get("pages")
        published_date = parse_date(request.POST.get("published_date"))

        # Validação básica
        if title and author and pages and published_date:
            Book.objects.create(
                title=title,
                author=author,
                pages=pages,
                published_date=published_date
            )
            return redirect("books") # após o cadastro, volta para a listagem

    return render(request, "app/book_form.html")