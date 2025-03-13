from django.shortcuts import render, redirect
from .models import Book, CustomUser
from .forms import BookForm, CustomUserCreationForm
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'bookapp/home.html')

def create(request):
    error = ''
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма некорректна'
    form = BookForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'bookapp/create.html', data)

class BookListView(ListView):
    model = Book
    template_name = 'bookapp/home.html'
    context_object_name = 'books'
    paginate_by = 3

class BookUpdateView(UpdateView):
    model = Book
    template_name = 'bookapp/update.html'
    form_class = BookForm

class BookDeleteView(DeleteView):
    model = Book
    success_url = '/'
    template_name = 'bookapp/delete.html'

def register(request):
    error = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)
            error = 'Форма некорректна'
    form = CustomUserCreationForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'bookapp/register.html', data)    

class CustomLoginView(LoginView):
    template_name = 'bookapp/login.html'

def custom_logout(request):
    logout(request)
    return redirect('home')