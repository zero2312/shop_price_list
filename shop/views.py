from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from shop.forms import OrderForm
from shop import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.views.decorators.http import require_POST

"""""
'base' Данная функция отображает все категории на странице.
"""""
def base(request):
    category = models.Category.objects.all()
    contact = models.Concacts.objects.all()
    return render(request,'shop/base.html', {'category': category, 'contact': contact})
"""
'all_products' Данная функция отображает все товары в магазине. 
Если в GET запросе передан параметр "search", то функция фильтрует товары по наименованию 
и описанию, содержащим указанный поисковый запрос. Если параметр не передан, 
то отображаются все товары без фильтрации. Функция 
также передает объекты категорий в шаблон для возможности их отображения на странице.
"""
def all_products(request):
    search_query = request.GET.get('search', '')
    if search_query:
        products = models.Products.objects.filter(title__icontains = search_query, description__icontains = search_query)
    else:
        category = models.Category.objects.all()
        products = models.Products.objects.all()
        contact = models.Concacts.objects.all()
    return render(request,'shop/all_products.html', {'products': products,'category': category, 'contact': contact})

"""
'categories' Данная функция отображает все товары в магазине в задоной категории.
Проверет есть ли параметр 'sort' в адресной строке, если он равен 'asc' - Сортировка по возрастанию  
Если 'desc' - Сортировка по убыванию, однако если пораметр отсутвиет фильтруем товар по категории.
"""
def categories(request,category_id):
    products = models.Products.objects.filter(category_id=category_id)
    # получаем параметры цены из запроса
    sort = request.GET.get('sort', '')
    if sort == 'asc':
        products = models.Products.objects.order_by('price')
    elif sort == 'desc':
        products = models.Products.objects.order_by('-price')
    else:
        products = models.Products.objects.all()
        products = models.Products.objects.filter(category_id=category_id)
    
    # Фильтр цен
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price and max_price:
        # Фильтруем по диапазону цен
        products = products.filter(price__range=(min_price, max_price))
    elif min_price:
        # Фильтруем по минимальной цене
        products = products.filter(price__gte=min_price)
    elif max_price:
        # Фильтруем по максимальной цене
        products = products.filter(price__lte=max_price)

    category = models.Category.objects.all()
    contact = models.Concacts.objects.all()
    return render(request,'shop/сategory.html', {'products': products,'category': category, 'contact':contact})

"""
'add_to_cart' Данная функция получает продукт по id (То есть, получаем конкретный товар)
Получаем все группы пользователей, если группа 'VIP', меняем стандартную цену на отп.
Создаём новую запись в таблице 'Cart' - 
Если запись есть прибовляем quantity (Количество +1).
"""

def add_to_cart(request, product_id):
    product = models.Products.objects.get(id=product_id)
    userGrup = Group.objects.all()
    for item in userGrup:
        if userGrup == item.name == 'VIP':
            product.price = product.wholesalePrice
    cart_item, created = models.Cart.objects.get_or_create(
        user=request.user,
        product=product,
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

"""
'remove_from_cart' Данная функция получает конкретную запись  по id 
(То есть, получаем конкретную запись из таблицы 'Cart') 
Удаляем ёё
"""

def remove_from_cart(request, cart_item_id):
    cart_item = models.Cart.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

"""
'update_cart' Данная функция уменьшает и 
увиличивает количество товара в карзине, (Смотреть html)
"""

def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(models.Cart, id=cart_item_id, user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increment':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    return redirect('cart')

@login_required
def cart(request):
    contact = models.Concacts.objects.all()
    category = models.Category.objects.all()
    cart_items = models.Cart.objects.filter(user=request.user)
    total = sum(item.get_total() for item in cart_items)
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # сохраняем данные заказа в базу данных
            order = models.Order.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                total=total,
            )
            # сохраняем содержимое корзины в базу данных
            for item in cart_items:
                models.OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price = item.product.price,
                    wholesalePrice = item.product.wholesalePrice,
                )
            # очищаем корзину
            cart_items.delete()
            # перенаправляем на страницу с подтверждением заказа
            return redirect('order_confirmation')
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total, 'category':category, 'form': form, 'contact':contact})

def order_confirmation(request):
    category = models.Category.objects.all()
    contact = models.Concacts.objects.all()
    return render(request,'shop/order_confirmation.htm', {'category':category, 'contact': contact})
