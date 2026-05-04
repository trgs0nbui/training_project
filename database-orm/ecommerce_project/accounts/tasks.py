from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_welcome_email_task(self, user_id):
    """
    Async task to send welcome email to newly registered user.
    Includes retry logic with exponential backoff
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Render HTML template
        context = {
            'username': user.username,
            'email': user.email,
        }
        
        html_message = render_to_string('accounts/emails/welcome_email.html')
        plain_message = strip_tags(html_message)
        
        # Send mail
        send_mail(
            subject='Welcome to my Ecommerce Platform!',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Welcome email sent successfully to {user.email}")
        return f"Welcome email sent successfully to {user.email}"
    except User.DoesNotExist:
        logger.error(f"User with ID {user_id} does not exist")
        return f"User with ID {user_id} does not exist"
    except Exception as exc:
        logger.error(f"Failed to send email for user {user_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)    