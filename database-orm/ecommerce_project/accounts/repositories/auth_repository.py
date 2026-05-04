from django.contrib.auth.models import Group

class AuthRepository:
    @staticmethod
    def get_group(**data):
        return Group.objects.get(name=data)
    
    