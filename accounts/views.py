from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, UserEditForm



def login_user(request):
    if request.user.is_authenticated == True:
        return redirect("home_page:home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data.get('username'))
            login(request, user)
            return redirect('home_page:home')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form':form})


def register_user(request):
    if request.user.is_authenticated == True:
        return redirect("home_page:home")
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return HttpResponse("Passwords is not match!!!")

        user = User.objects.create(email=email, username=username, password=password1)
        login(request, user)
        return redirect("home_page:home")

    return render(request, "accounts/register.html", {})


def edit_user(request):
    user = request.user
    form = UserEditForm(instance=user)
    if request.method == "POST":
        form = UserEditForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_page:home')

    return render(request, 'accounts/edit_user.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home_page:home')
