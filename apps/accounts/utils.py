from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator


# Додаткові внутрішні механізми

def send_activation_email(user, request, to_email):
    # назва повідомлення
    email_subject = "Підтвердження акаунта на сайті foodietales.com"

    data = {
        # взнаємо наш domain
        "domain": get_current_site(request),
        # зашифровуємо айдішку юзера використовуючи secret_key
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        # генеруємо токен
        'token': default_token_generator.make_token(user),
        'user': user
    }
    # відправляємо дані в "email_template/register_confirm_email.html"
    # перетворюємо дані в строку
    message = render_to_string("email_template/register_confirm_email.html", data)

    email = EmailMessage(email_subject, message, to=[to_email])
    # для коректного відображення шаблону
    email.content_subtype = "html"
    print(email.message())
    email.send(fail_silently=True)



# lbqicmdhlscvyoaz