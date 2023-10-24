from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import *


class TestUrls(SimpleTestCase):
    def test_list_users_url_resolves(self):
        url = reverse("accounts:list_users")
        self.assertEquals(resolve(url).func, user_list)

    def test_user_info_url_resolves(self):
        url = reverse("accounts:user_info", args=[1])
        self.assertEquals(resolve(url).func, user_detail)

    def test_user_register_url_resolves(self):
        url = reverse("accounts:user_register")
        self.assertEquals(resolve(url).func.view_class, UserRegisterView)

    def test_user_login_resolves(self):
        url = reverse("accounts:user_login")
        self.assertEquals(resolve(url).func.view_class, UserLoginView)

    def test_user_login_resolves(self):
        url = reverse("accounts:user_logout")
        self.assertEquals(resolve(url).func.view_class, UserLogoutView)
