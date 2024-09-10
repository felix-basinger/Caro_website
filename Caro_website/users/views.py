import json
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash, get_user_model
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from .tasks import send_order_confirmation_email, send_password_reset_email
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserForm, UserProfileForm, CheckoutForm, \
    PasswordResetConfirmForm, PasswordResetRequestForm, SetNewPasswordForm
from .models import UserProfile, CustomUser
from django_user_agents.utils import get_user_agent
from .models import Order, PasswordResetCode
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

    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
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
        item.quantity * item.product.price for item in cart.items.all())

    discounted_total_amount = sum(
        item.quantity * item.product.discounted_price for item in cart.items.all()
    )

    if request.method == 'POST':
        form = CheckoutForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = CheckoutForm(instance=user_profile)

    return render(request, template, {
        'form': form,
        'total_amount': total_amount,
        'discounted_total_amount': discounted_total_amount,
    })


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
            user=request.user,
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

        send_order_confirmation_email.delay(order.id, request.user.email)

        status = data.get('status')
        if status == 'COMPLETED':
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def password_reset_request(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'users/mobile/password_reset_request.html'
    elif user_agent.is_tablet:
        template = 'users/tablet/password_reset_request.html'
    else:
        template = 'users/password_reset_request.html'

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = CustomUser.objects.get(email=email)
                request.session['reset_email'] = email
                send_password_reset_email.delay(email)
                return redirect('password_reset_code')
            except CustomUser.DoesNotExist:
                messages.error(request, 'This email is not registered. Please sign up.')
                return redirect('register')
    else:
        form = PasswordResetRequestForm()
    return render(request, template, {'form': form})


def password_reset_code(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'users/mobile/password_reset_code.html'
    elif user_agent.is_tablet:
        template = 'users/tablet/password_reset_code.html'
    else:
        template = 'users/password_reset_code.html'
    if request.method == 'POST':
        if 'resend_code' in request.POST:
            email = request.session.get('reset_email')
            if email:
                reset_code = PasswordResetCode.objects.filter(user__email=email).last()
                if reset_code and reset_code.created_at >= timezone.now() - timedelta(minutes=2):
                    messages.error(request, 'You must wait 2 minutes before resending the code.')
                else:
                    send_password_reset_email.delay(email)
                    messages.success(request, 'A new reset code has been sent to your email.')
                return redirect('password_reset_code')

        elif 'submit_code' in request.POST:
            form = PasswordResetConfirmForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data.get('code')
                try:
                    reset_code = PasswordResetCode.objects.get(
                        code=code,
                        created_at__gte=timezone.now() - timedelta(minutes=2)
                    )
                    return redirect('set_new_password', user_id=reset_code.user.id)
                except PasswordResetCode.DoesNotExist:
                    messages.error(request, 'Invalid or expired code.')
            return redirect('password_reset_code')
    else:
        form = PasswordResetConfirmForm()

    return render(request, template, {'form': form})


def set_new_password(request, user_id):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'users/mobile/set_new_password.html'
    elif user_agent.is_tablet:
        template = 'users/tablet/set_new_password.html'
    else:
        template = 'users/set_new_password.html'
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()
            login(request, user)
            messages.success(request, 'Your password has been successfully reset.')
            return redirect('account')
    else:
        form = SetNewPasswordForm()
    return render(request, template, {'form': form})


@csrf_exempt
def resend_reset_code(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        if not email:
            return JsonResponse({'status': 'error', 'message': 'Email not found in session.'}, status=400)

        reset_code = PasswordResetCode.objects.filter(user__email=email).last()

        if reset_code and reset_code.created_at >= timezone.now() - timedelta(minutes=2):
            return JsonResponse({'status': 'error', 'message': 'Please wait 2 minutes before resending the code.'},
                                status=400)

        # Отправляем код снова
        send_password_reset_email.delay(email)
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

