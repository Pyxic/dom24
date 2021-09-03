from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View

from account.forms import LoginForm


class LoginView(View):

    def get(self, request, *args,**kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, "account/login.html", context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'account/login.html', {'form': form})
