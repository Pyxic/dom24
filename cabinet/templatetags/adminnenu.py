# Import template module
from django import template
# Create an object of Library()
from django.contrib.auth.models import User

from account.models import Owner, PermissionAccess, Profile

register = template.Library()
# Define the template file for the inclusion tag


@register.inclusion_tag('admin/menu.html')


# Declare function to find out the even numbers within a range
def generate_admin_menu(user):
    user = Profile.objects.get(user_id=user)
    permissions = [permission.page.name for permission in PermissionAccess.objects.filter(role=user.role, access=True)]
    return {"permissions": permissions}
