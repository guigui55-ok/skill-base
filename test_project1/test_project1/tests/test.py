from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTestCase(TestCase):

    def setUp(self):
        """テスト用ユーザー作成"""
        self.client = Client()
        self.test_user_email = "testuser@example.com"
        self.test_user_password = "StrongPass123!"
        self.user = User.objects.create_user(
            username="testuser",
            email=self.test_user_email,
            password=self.test_user_password
        )

    # -----------------------
    # ユーザー登録（サインイン）
    # -----------------------
    def test_signup_success(self):
        """正しい情報でサインイン成功"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'NewStrongPass123!',
            'password2': 'NewStrongPass123!'
        })
        self.assertEqual(response.status_code, 302)  # リダイレクト
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_password_mismatch(self):
        """パスワード確認と不一致"""
        response = self.client.post(reverse('signup'), {
            'username': 'user1',
            'email': 'user1@example.com',
            'password1': 'pass12345',
            'password2': 'pass123'
        })
        self.assertContains(response, "パスワードが一致しません", html=True)

    def test_signup_duplicate_email(self):
        """メール重複チェック"""
        response = self.client.post(reverse('signup'), {
            'username': 'user2',
            'email': self.test_user_email,  # 既存ユーザー
            'password1': 'AnotherPass123!',
            'password2': 'AnotherPass123!'
        })
        self.assertContains(response, "このメールアドレスは既に使用されています", html=True)

    # -----------------------
    # ログイン
    # -----------------------
    def test_login_success(self):
        """正しい情報でログイン成功"""
        response = self.client.post(reverse('login'), {
            'username': self.test_user_email,
            'password': self.test_user_password
        })
        self.assertEqual(response.status_code, 302)  # ログイン後リダイレクト
        # セッションにユーザーがセットされているか確認
        response = self.client.get(reverse('members'))
        self.assertEqual(str(response.context['user']), 'testuser')

    def test_login_wrong_password(self):
        """パスワード間違い"""
        response = self.client.post(reverse('login'), {
            'username': self.test_user_email,
            'password': 'WrongPass'
        })
        self.assertContains(response, "パスワードが違います", html=True)

    def test_login_nonexistent_user(self):
        """存在しないユーザー"""
        response = self.client.post(reverse('login'), {
            'username': 'notexist@example.com',
            'password': 'anyPass123'
        })
        self.assertContains(response, "ユーザーが存在しません", html=True)

    # -----------------------
    # ログアウト
    # -----------------------
    def test_logout(self):
        """ログアウト処理"""
        self.client.login(username=self.test_user_email, password=self.test_user_password)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('members'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('members'))

    # -----------------------
    # アクセス制御
    # -----------------------
    def test_access_members_without_login(self):
        """未ログインでメンバー画面にアクセス"""
        response = self.client.get(reverse('members'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('members'))

    def test_access_members_with_login(self):
        """ログイン済みでメンバー画面にアクセス"""
        self.client.login(username=self.test_user_email, password=self.test_user_password)
        response = self.client.get(reverse('members'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "メンバー用ページ")  # テンプレート内の文言を確認

