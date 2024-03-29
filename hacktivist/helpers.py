from django.core.mail import send_mail
from django.conf import settings

def send_forget_password_mail(email, token):

    subject = "Your password reser link"
    message = f"Click to reset : http://127.0.0.1:8000/account/change-password/{token}/"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]  # Convert single email to list

    send_mail(subject, message, email_from, recipient_list)
    return True



# helpers.py gpt

# from django.core.mail import send_mail
# from django.conf import settings

# def send_forget_password_mail(email, token):
#     subject = "Your password reset link"
#     message = f"Click to reset: http://127.0.0.1:8000/account/change-password/{token}/"
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message, email_from, recipient_list)
