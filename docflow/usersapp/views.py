from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from usersapp.forms import DocFlowUserCreationForm


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

