from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
import re

# ログインフォーム（Django 標準 AuthenticationForm を利用）
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="ユーザー名またはメール",
        widget=forms.TextInput(attrs={"placeholder": "ユーザー名またはメール", "class": "form-control"})
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={"placeholder": "パスワード", "class": "form-control"})
    )

# 新規登録フォーム
class SigninForm(forms.ModelForm):
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={"placeholder": "パスワード", "class": "form-control"})
    )
    password2 = forms.CharField(
        label="パスワード確認",
        widget=forms.PasswordInput(attrs={"placeholder": "パスワード確認", "class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "ユーザー名", "class": "form-control"}),
            "email": forms.EmailInput(attrs={"placeholder": "メールアドレス", "class": "form-control"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("このメールアドレスは既に登録されています。")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        # パスワード強度チェック（簡易例）
        if password1 != password2:
            raise ValidationError("パスワードが一致しません。")
        if len(password1) < 8:
            raise ValidationError("パスワードは8文字以上で設定してください。")
        if not re.search(r"[A-Z]", password1):
            raise ValidationError("パスワードには大文字を含めてください。")
        if not re.search(r"[0-9]", password1):
            raise ValidationError("パスワードには数字を含めてください。")
        return password2
