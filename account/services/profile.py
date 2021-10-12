from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect

import account
from account import models
from account.models import PermissionAccess, Profile
from account.services.owner import OwnerCabinet
from dom24 import settings


def has_access(permission_page):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('account:login')
            if request.session.get(settings.USERS_SESSION_ID):
                owner_cabinet = OwnerCabinet(request)
                owner_cabinet.login_admin(request)
                # owner_cabinet.clear()
            user = User.objects.get(id=request.user.id)
            try:
                if PermissionAccess.objects.filter(role=user.profile.role, page__name=permission_page, access=True).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse('Доступ запрещен')
            except Profile.DoesNotExist:
                return HttpResponse('Доступ запрещен')
        return wrapper
    return decorator


def has_access_for_class(permission_page, user):
    return PermissionAccess.objects. \
            filter(role=user.profile.role, page__name=permission_page, access=True).exists()


