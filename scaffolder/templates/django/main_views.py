from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse

from .forms import UserForm


def index(request):
    return render(request, 'main.html')


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        redirect('/')
    else:
        # Return an 'invalid login' error message.
        raise JsonResponse(status=400, data={}, safe=False)


def logout(request):
    logout(request)
    redirect('/')


def create_user(request):
    f = UserForm(request.POST)

    if not f.is_valid():
        raise JsonResponse({}, status=400, safe=False)
    else:
        f.save()
        response = {
            'user': {
                'username': request.POST.get('username'),
                'email': request.POST.get('email'),
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
            }
        }
        JsonResponse(response, status=400, safe=False)
