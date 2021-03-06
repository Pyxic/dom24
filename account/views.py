import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from account.forms import LoginForm, LoginOwnerForm
from account.models import Profile
from account.services.owner import OwnerCabinet
from dom24 import settings

logger = logging.getLogger(__name__)


class LoginView(View):

    def get(self, request, *args,**kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, "account/login.html", context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/admin')
        return render(request, 'account/login.html', {'form': form})


class LoginOwnerView(View):

    def get(self, request, *args, **kwargs):
        form = LoginOwnerForm(request.POST or None)
        context = {'form': form}
        return render(request, "account/login_owner.html", context)

    def post(self, request, *args, **kwargs):
        form = LoginOwnerForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/cabinet/index')
        return render(request, 'account/login_owner.html', {'form': form})


def get_user_role(request):
    if request.is_ajax():
        user = Profile.objects.get(pk=request.POST.get('pk'))
        return HttpResponse(user.role)


def logout_user(request):
    logout(request)
    return redirect('account:login')


def go_to_cabinet(request, owner_id, admin_id):
    owner_cabinet = OwnerCabinet(request)
    owner_cabinet.set_admin(admin_id)
    owner_cabinet.set_owner(owner_id)
    logger.info(owner_cabinet.users)
    admin = owner_cabinet.users['admin']
    owner_cabinet.login_owner(request)
    return redirect(f'/cabinet/index?admin={admin}')
