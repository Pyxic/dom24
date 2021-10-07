# Import template module
from django import template
# Create an object of Library()
from django.contrib.auth.models import User

from account.models import Owner

register = template.Library()
# Define the template file for the inclusion tag


@register.inclusion_tag('cabinet/menu.html')


# Declare function to find out the even numbers within a range
def show_menu(user):
    owner = Owner.objects.get(user_id=user)
    flats = owner.flat_set.all()
    return {"flats": flats}
