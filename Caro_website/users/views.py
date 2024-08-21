import json

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt

from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserForm, UserProfileForm, CheckoutForm
from .models import UserProfile
from django_user_agents.utils import get_user_agent
from .models import Order
from cart.models import Cart


def get_card_type(card_number):
    card_number = card_number.replace(' ', '')
    if card_number.startswith(('34', '37')):
        return 'American Express'
    elif card_number.startswith('4'):
        return 'Visa'
    elif card_number.startswith(('51', '52', '53', '54', '55')):
        return 'MasterCard'
    elif card_number.startswith('6'):
        return 'Discover'
    else:
        return 'Unknown'


def register(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'users/mobile/register.html'
    elif user_agent.is_tablet:
        template = 'users/tablet/register.html'
    else:
        template = 'users/register.html'

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, template, {'form': form})


def login_view(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'users/mobile/login.html'
    elif user_agent.is_tablet:
        template = 'users/tablet/login.html'
    else:
        template = 'users/login.html'

    form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('/')
    return render(request, template, {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def account(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'users/mobile/account.html'
    elif user_agent.is_tablet:
        template = 'users/tablet/account.html'
    else:
        template = 'users/account.html'
    return render(request, template)


@login_required
def edit_profile(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'users/mobile/edit_profile.html'
    elif user_agent.is_tablet:
        template = 'users/tablet/edit_profile.html'
    else:
        template = 'users/edit_profile.html'

    # Проверяем, есть ли у пользователя профиль, если нет - создаем
    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            # Получаем информацию о карте и платежной системе
            card_number = profile_form.cleaned_data.get('card_number')
            # card_type = get_card_type(card_number)
            # last_four_digits = card_number[-4:]
            # profile.payment = f'{card_type} *{last_four_digits}'
            profile_form.save()
            return redirect('account')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, template, {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def checkout(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'users/mobile/checkout.html'
    elif user_agent.is_tablet:
        template = 'users/tablet/checkout.html'
    else:
        template = 'users/checkout.html'

    user_profile = UserProfile.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)
    total_amount = sum(
        item.quantity * item.product.price for item in cart.items.all())  # метод, который вычисляет общую сумму корзины

    if request.method == 'POST':
        form = CheckoutForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            # Здесь можно добавить логику для сохранения заказа или выполнения других действий
            return redirect('account')  # URL для страницы подтверждения заказа
    else:
        form = CheckoutForm(instance=user_profile)

    return render(request, template, {'form': form, 'total_amount': total_amount})


def order_confirmation(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'users/mobile/order_confirmation.html'
    elif user_agent.is_tablet:
        template = 'users/tablet/order_confirmation.html'
    else:
        template = 'users/order_confirmation.html'
    return render(request, template)


@csrf_exempt
def process_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        order = Order.objects.create(
            user=request.user,  # предполагается, что пользователь уже аутентифицирован
            paypal_order_id=data['paypal_order_id'],
            status=data['status'],
            total_amount=data['total_amount'],
            shipping_name=data['shipping_name'],
            shipping_address=data['shipping_address'],
            shipping_city=data['shipping_city'],
            shipping_state=data['shipping_state'],
            shipping_zip_code=data['shipping_zip_code'],
            shipping_country=data['shipping_country']
        )

        # Формирование HTML-сообщения
        html_message = render_to_string('order_email.html', {
            'shipping_name': order.shipping_name,
            'shipping_address': order.shipping_address,
            'shipping_city': order.shipping_city,
            'shipping_state': order.shipping_state,
            'shipping_zip_code': order.shipping_zip_code,
            'shipping_country': order.shipping_country,
            'paypal_order_id': order.paypal_order_id,
            'total_amount': order.total_amount,
            'status': order.status,
        })

        html_message_user = render_to_string('order_receipt.html', {
            'user_name': order.user.username,
            'shipping_name': order.shipping_name,
            'shipping_address': order.shipping_address,
            'shipping_city': order.shipping_city,
            'shipping_state': order.shipping_state,
            'shipping_zip_code': order.shipping_zip_code,
            'shipping_country': order.shipping_country,
            'paypal_order_id': order.paypal_order_id,
            'total_amount': order.total_amount,
            'status': order.status,
        })
        plain_message = strip_tags(html_message)
        subject = f'Order Confirmation - {order.paypal_order_id}'
        from_email = 'basingerfelix17@gmail.com'
        to_email = request.user.email

        # Отправка письма
        send_mail(subject, plain_message, to_email, [from_email], html_message=html_message)
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message_user)
        status = data.get('status')
        if status == 'COMPLETED':  # Проверяем, что оплата была успешной
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

