from accounts.tasks import send_welcome_email_task
import logging

logger = logging.getLogger(__name__)
class EmailService:
    
    """
    Service layer for email operations
    Decouples email sending from business logic
    """
    
    @staticmethod
    def send_welcome_email(user):
        """
        Trigger async task to send welcome email
        
        Args:
            user: User instance that was just registered
        """
        try:
            task = send_welcome_email_task.delay(user.id)
            logger.info(f"Welcome email task queued for user {user.id}: {task.id}")
            return task.id
        except Exception as e:
            logger.error(f"Failed to send welcome email (sync) for user {user.id}: {str(e)}")
            return None
    
    @staticmethod
    def send_welcome_email_sync(user):
        """
        Send welcome email synchronously 
        
        Args:
            user: User instance
        """
        try: 
            task = send_welcome_email_task.apply_async(
                args=[user.id],
                countdown=0
            )
            logger.info(f"Welcome email task sent (sync) for user {user.id}: {task.id}")
            return task.id            
        except Exception as e:
            logger.error(f"Failed to send welcome email (sync) for user {user.id}: {str(e)}")
            return None
        
        
    