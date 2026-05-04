from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        staff_group, _ = Group.objects.get_or_create(name='Staff')
        customer_group, _ = Group.objects.get_or_create(name='Customer')
        
        # Product permission
        product_permissions = Permission.objects.filter(
            content_type__app_label='shop',
            content_type__model='product'
        )
        
        # Admin permission for all product
        admin_group.permissions.set(product_permissions)
        
        # Staff permission for add + change product
        staff_group.permissions.set(
            product_permissions.filter(codename__in=[
                'add_product',
                'change_product',
                'view_product'
            ])
        )
        
        # Customer just view product
        customer_group.permissions.set(
            product_permissions.filter(codename='view_product')
        )
        
        self.stdout.write(self.style.SUCCESS("Roles setup done"))