from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from django.contrib import messages
from .models import Product, Category, Manufacturer, Trash, TrashElement
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from . import specialty_search
  
def index(request):
    return HttpResponse("Приложение для управления работает!")

def author(request):
    return HttpResponse("<div><h1>Лабу сделал:</h1><h2>Имя: Владислав</h2><h2>Фамилия: Цветков</h2><h2>Отчество: Артурович</h2><h2>Группа: 82ТП</h2></div>")

def shop(request):
    return HttpResponse('<div><h1>Тема лабы:</h1><h2 style="width: 50%">Магазин наборов для рисования граффити (баллончики, трафареты).</h2></div>')

def specialty_byid(request, id):
    return HttpResponse(specialty_search.spSearch(by_id=id))

def specialty(request):
    return HttpResponse(specialty_search.spSearch())

def product_list(request):
    products = Product.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    manufacturer_id = request.GET.get('manufacturer')
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)

    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'manufacturers': manufacturers,
        'selected_category': int(category_id) if category_id else None,
        'selected_manufacturer': int(manufacturer_id) if manufacturer_id else None,
        'search_query': search_query or '',
    }

    return render(request, 'shop/products/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'shop/products/product_detail.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    trash, created = Trash.objects.get_or_create(user=request.user)

    cart_item, item_created = TrashElement.objects.get_or_create(
        trash=trash,
        product=product,
        defaults={'quantity': 1}
    )

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'Товар "{product.name}" добавлен в корзину')
    return redirect('cart_view')


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(TrashElement, id=item_id, trash__user=request.user)

    if request.method == 'POST':
        try:
            new_quantity = int(request.POST.get('quantity'))
            if new_quantity < 1:
                messages.error(request, "Количество не может быть меньше 1")
            elif new_quantity > cart_item.product.quantity:
                messages.error(request,
                               f"Недостаточно товара на складе. Доступно: {cart_item.product.quantity}")
            else:
                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, "Количество обновлено")
        except (ValueError, TypeError):
            messages.error(request, "Некорректное количество")

    return redirect('cart_view')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(TrashElement, id=item_id, trash__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Товар "{product_name}" удален из корзины')
    return redirect('cart_view')


@login_required
def cart_view(request):
    trash, created = Trash.objects.get_or_create(user=request.user)

    cart_items = trash.items.select_related('product')
    total = sum(item.cost() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'shop/cart/cart_view.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                print(f"User created: {user.username}")  # Для отладки
                login(request, user)
                return redirect('product_list')
            except Exception as e:
                print(f"Error creating user: {e}")  # Логируем ошибку
                # Добавьте сообщение об ошибке
                messages.error(request, f"Ошибка при создании пользователя: {e}")
        else:
            # Логируем ошибки формы
            print("Form errors:")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"- {field}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'shop/auth/signup.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'shop/auth/profile.html')

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/auth/login.html', {'form': form})
def cart_count(request):
    if request.user.is_authenticated:
        count = TrashElement.objects.filter(trash__user=request.user).aggregate(
            total=Sum('quantity')
        )['total'] or 0
        return {'cart_count': count}
    return {'cart_count': 0}

def main(request):
    return HttpResponse('<div style="display: flex; align-items: center; flex-direction: column;"><h1>Добро пожаловать!</h1><div style="display: flex; justify-content: space-around; width: 100%"><h2 style="width: 50%"><a href="author/">Автор</a></h2><h2><a href="shop/">Магазин</a></h2></div></div>')