from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from .models import Order, CustomUser
from django.utils.crypto import get_random_string
from .models import PasswordResetCode


@shared_task
def send_order_confirmation_email(order_id, user_email):
    order = Order.objects.get(id=order_id)

    # Формирование HTML-сообщений
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
    to_email = user_email

    # Отправка писем
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message_user)
    send_mail(subject, plain_message, to_email, [from_email], html_message=html_message)


@shared_task
def send_password_reset_email(user_email):
    try:
        user = CustomUser.objects.get(email=user_email)
    except CustomUser.DoesNotExist:
        # Обработка ситуации, когда пользователь не найден
        raise ValueError(f"No user with email {user_email} found.")

    # Генерация кода
    code = get_random_string(length=6, allowed_chars='0123456789')

    # Сохранение кода в базе данных
    PasswordResetCode.objects.create(user=user, code=code)

    # Формирование письма
    html_message = render_to_string('password_reset_email.html', {'code': code})
    plain_message = strip_tags(html_message)
    subject = 'Password Reset Code'
    from_email = 'basingerfelix17@gmail.com'

    # Отправка письма
    send_mail(subject, plain_message, from_email, [user_email], html_message=html_message)


