from django.shortcuts import render, redirect
from .models import Book, CustomUser, Order, OrderItem
from .forms import BookForm, CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import  login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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

    def get_queryset(self):
        queryset = super().get_queryset()
        author = self.request.GET.get('author')
        if author:
            queryset = queryset.filter(author__icontains=author)
        return queryset

class BookUpdateView(UpdateView):
    model = Book
    template_name = 'bookapp/update.html'
    form_class = BookForm

class BookDeleteView(DeleteView):
    model = Book
    success_url = '/'
    template_name = 'bookapp/delete.html'

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user =  form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'bookapp/register.html', {'form': form})

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'bookapp/login.html'

def custom_logout(request):
    logout(request)
    return redirect('home')

class ProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'bookapp/profile.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user    
    
def add_to_cart(request, book_id):
    cart = request.session.get('cart', {})
    book_id_str = str(book_id)

    quantity = cart.get(book_id_str, 0) + 1
    cart[book_id] = quantity

    request.session['cart'] = cart
    return redirect('/')

def cart_view(request):
    cart = request.session.get('cart', {})
    books_in_cart = []

    for book_id, quantity in cart.items():
        try:
            book = Book.objects.get(id=book_id)
            books_in_cart.append({
                'book': book,
                'quantity': quantity,
                'total_price': round(book.price * quantity, 2)
            })
        except Book.DoesNotExist:
            continue

    total_cost = sum(item['total_price'] for item in books_in_cart)

    return render(request, 'bookapp/cart.html', {
        'books_in_cart': books_in_cart,
        'total_cost': total_cost
    })

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('cart')

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    total_price = 0
    for book_id, quantity in cart.items():
        book = Book.objects.get(id=book_id)
        total_price += book.price * quantity

    order = Order.objects.create(user=request.user, total_price=total_price)

    for book_id, quantity in cart.items():
        book = Book.objects.get(id=book_id)
        OrderItem.objects.create(order=order, book=book, quantity=quantity)

    request.session['cart'] = {}

    return redirect('/')

def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookapp/orders.html', {'orders': orders})

def check_username(request):
    username = request.GET.get('username')
    exists = get_user_model().objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})