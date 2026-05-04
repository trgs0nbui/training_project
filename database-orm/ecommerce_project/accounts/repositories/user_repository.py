from django.contrib.auth.models import User
class UserRepository:
    @staticmethod
    def get_all():
        return User.objects.all()
    
    @staticmethod
    def get_by_id(user_id):
        return User.objects.filter(id=user_id).first()
    
    @staticmethod
    def create_user(**data):
        return User.objects.create_user(**data)
    
    @staticmethod
    def update_user(user, **data):
        for attr, value in data.items():
            setattr(user, attr, value)
            
        user.save()
        return user
    
    @staticmethod
    def delete_user(user):
        user.delete()