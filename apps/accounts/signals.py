from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from apps.accounts.models import User



@receiver(post_save, sender=User)
def send_selcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Nairobi Business Directory!"
        from_email = None
        to_email = [instance.email]
        context = {"user": instance, "fullname": instance.fullname}

        html_content = render_to_string("accounts/welcome_email.html", context)
        text_content = "Welcome to Nairobi Business Directory! We're excited to have you on board."
        
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()


