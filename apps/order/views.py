from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from apps.order.forms import AddToCartForm, CreateOrderForm
from apps.order.models import Cart, OrderProduct


def get_cart_data(user):
    total = 0
    cart = Cart.objects.filter(user=user)
    for row in cart:
        total += row.quantity * row.product.price

    return {'total': total, 'cart': cart}


@login_required
def add_to_cart_view(request):
    data = request.GET.copy()
    data.update(user=request.user)
    request.GET = data

    form = AddToCartForm(request.GET)
    if form.is_valid():
        cd = form.cleaned_data
        csrf = request.session.get('cart_token')

        if not csrf or csrf != data.get('csrfmiddlewaretoken'):
            row = Cart.objects.filter(user=cd['user'], product=cd['product']).first()
            if row:
                Cart.objects.filter(id=row.id).update(quantity=row.quantity + cd['quantity'])
            else:
                form.save()
            request.session['cart_token'] = data.get('csrfmiddlewaretoken')
        breadcrumbs = {'current': 'Добавление в корзину'}
        return render(
            request,
            'order/added.html',
            {'product': cd['product'], 'cart': get_cart_data(cd['user']), 'breadcrumbs': breadcrumbs}
        )


@login_required
def cart(request):
    cart = get_cart_data(request.user)
    breadcrumbs = {'current': 'Корзина'}
    return render(
        request,
        'order/cart.html',
        {'cart': cart, 'breadcrumbs': breadcrumbs}
    )


@login_required
def create_order_view(request):

    error = None
    user = request.user
    cart = get_cart_data(user)
    if not cart['cart']:
        return redirect('index')

    if request.method == 'POST':
        data = request.POST.copy()
        data.update(user=user, total=cart['total'])
        request.POST = data

        form = CreateOrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save()
                    order_products = Cart.objects.filter(user=user).select_related('product')
                    for order_product in order_products:
                        OrderProduct.objects.create(
                            order=order,
                            product=order_product.product,
                            quantity=order_product.quantity,
                            price=order_product.product.price
                        )

                    Cart.objects.filter(user=user).delete()
                    breadcrumbs ={
                        reverse('cart'):'Корзина',
                        'current': 'Заказ оформлен'
                    }
                    return render(request, 'order/created.html', {'breadcrumbs': breadcrumbs})
            except Exception as e:
                error = f'Заказ не создался. {e}. Напишите, пожалуйста, нашему менеджеру.'
        else:
            error = form.errors

    else:
        form = CreateOrderForm(data={
            'phone': user.phone if user.phone else '',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })
    breadcrumbs = {
        reverse('cart'): 'Корзина',
        'current': 'Оформление заказа'
    }
    return render(request, 'order/create.html', {'cart': cart, 'error': error, 'form': form, 'breadcrumbs': breadcrumbs})

@login_required
def delete_from_cart_view(request, product_id):
    Cart.objects.filter(user=request.user, product=product_id).delete()
    return redirect('cart')