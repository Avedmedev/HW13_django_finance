from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, decorators
from django.contrib import messages


# Create your views here.
from .forms import RegisterForm, LoginForm   #, ProfileForm


def signup_user(request):
    if request.user.is_authenticated:
        return redirect(to='financeapp:main')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('financeapp:main')
        else:
            return render(request, 'users/signup.html', context={'form': form})

    return render(request, 'users/signup.html', context={'form': RegisterForm()})


def login_user(request):
    if request.user.is_authenticated:
        return redirect(to='financeapp:main')

    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect('users:login')

        login(request, user)
        return redirect(to='financeapp:main')

    return render(request, 'users/login.html', context={'form': LoginForm()})


@decorators.login_required
def logout_user(request):
    logout(request)
    return redirect('financeapp:main')


# @decorators.login_required()
# def profile(request):
#     if request.method == "POST":
#         form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Your profile is updated")
#             return redirect('users:profile')
#         else:
#             return render(request, 'users/signup.html', context={'form': form})
#
#     return render(request, 'users/profile.html', context={'form': ProfileForm(instance=request.user.profile)})
