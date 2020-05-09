from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from usersapp.forms import DocFlowUserCreationForm
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

class UserLoginView(LoginView):

    template_name = 'usersapp/login.html'


@user_passes_test(lambda user: user.is_superuser)
def register(request):
    if request.method == 'POST':
        f = DocFlowUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('docflowapp:index')

    else:
        f = DocFlowUserCreationForm()

    return render(request, 'usersapp/register.html', {'form': f, 'nbar': 'register'})


def user(request):

    return render(request, 'usersapp/user.html', {user: request.user})


def getnewTokenUser(request):

    user = request.user
    try:
        token = user.auth_token
        token.delete()
        token = Token.objects.create(user=user)
    except:
        token = Token.objects.create(user=user)

    data = {'token': token.key}

    return JsonResponse(data)



