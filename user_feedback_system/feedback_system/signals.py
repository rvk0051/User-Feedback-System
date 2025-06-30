from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Feedback
from django.conf import settings

@receiver(post_save, sender=Feedback)
def notify_admin_on_new_feedback(sender, instance, created, **kwargs):
    if created:
        subject = f"New Feedback Submitted"
        message = f"""
        A new feedback has been submitted by {instance.user.username}.

        Subject: {instance.title}
        Status: {instance.status}
        Message:
        {instance.description}
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email for _, email in settings.ADMINS],
            fail_silently=False,
        )
