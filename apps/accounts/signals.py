from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from apps.accounts.models import User



def send_html_email(user_email, context):
    subject = "Welcome to Nairobi Business!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    text_content = "Welcome to our app!"
    html_content = render_to_string("accounts/welcome_email.html", context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=User)
def send_selcome_email(sender, instance, created, **kwargs):
    if created:
        context = {"user": instance, "fullname": instance.fullname}
        send_html_email(instance.email, context)


