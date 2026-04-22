from accounts.repositories.user_repository import UserRepository
from django.core.exceptions import ObjectDoesNotExist

class UserService:
    @staticmethod
    def list_users():
        return UserRepository.get_all()
    
    @staticmethod
    def get_user(user_id):
        user = UserRepository.get_by_id(user_id)
        
        if not user:
            raise ObjectDoesNotExist("User can not be found")
        return user
    
    @staticmethod
    def create_user(data):
        return UserRepository.create_user(**data)
    
    @staticmethod
    def update_user(user_id, data):
        user = UserService.get_user(user_id)
        return UserRepository.update_user(user, **data)
    
    @staticmethod
    def delete_user(user_id):
        user = UserService.get_user(user_id)
        UserRepository.delete_user(user)