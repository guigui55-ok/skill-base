
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import requests 

from django.contrib.auth.decorators import login_required
# from test_project1.test_project1.forms.auth_forms import LoginForm, SigninForm
from ..forms.auth_forms import LoginForm, SigninForm
from django.urls import reverse


def hello_jango(request):
    print('views.py > index')
    return HttpResponse("Hello, Django!")

def test_index(request):
    print('views.py > index')
    return render(request, 'test_index.html')


# ルートページ
def index(request):
    return render(request, "index.html")

# ログインページ
def login_view(request):
    if request.user.is_authenticated:
        return redirect("members")

    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("members")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

# 新規登録ページ
def signin_view(request):
    if request.user.is_authenticated:
        return redirect("members")

    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect("members")
    else:
        form = SigninForm()
    return render(request, "signin.html", {"form": form})

# ログアウト
def logout_view(request):
    logout(request)
    return redirect("login")

# ログイン後ページ
@login_required
def members_view(request):
    return render(request, "members.html")
