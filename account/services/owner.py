from django.contrib.auth import login
from django.contrib.auth.models import User

from account.models import Owner
from dom24 import settings


class OwnerCabinet:

    def __init__(self, request):
        """
        Initialize the OwnerCabinet.
        """
        self.session = request.session
        users = self.session.get(settings.USERS_SESSION_ID)

        if not users:
            # save an empty cart in the session
            users = self.session[settings.USERS_SESSION_ID] = {}
        self.users = users

    def set_admin(self, admin):
        self.users['admin'] = admin
        self.save()

    def set_owner(self, owner):
        self.users['owner'] = owner
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def clear(self):
        # remove cart from session
        del self.session[settings.USERS_SESSION_ID]
        self.save()

    def login_owner(self, request):
        owner = User.objects.get(id=self.session[settings.USERS_SESSION_ID]['owner'])
        login(request, owner, backend='django.contrib.auth.backends.ModelBackend')

    def login_admin(self, request):
        admin = User.objects.get(id=self.session[settings.USERS_SESSION_ID]['admin'])
        login(request, admin, backend='django.contrib.auth.backends.ModelBackend')
