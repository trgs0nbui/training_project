from accounts.tasks import send_welcome_email_task

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
        send_welcome_email_task.delay(user.id)
        
    @staticmethod
    def send_welcome_email_sync(user):
        """
        Send welcome email synchronously 
        
        Args:
            user: User instance
        """
        send_welcome_email_task.apply_async(
            args=[user.id],
            countdown=0
        )
        
        
    