from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse

import account
from account import models
from account.models import PermissionAccess


def has_access(permission_page):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user = User.objects.get(id=request.user.id)
            if PermissionAccess.objects.filter(role=user.profile.role, page__name=permission_page, access=True).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Доступ запрещен')
        return wrapper
    return decorator


def has_access_for_class(permission_page, user):
    return PermissionAccess.objects. \
            filter(role=user.profile.role, page__name=permission_page, access=True).exists()


