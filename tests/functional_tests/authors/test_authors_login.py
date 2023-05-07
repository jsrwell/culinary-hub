from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from .base import AuthorsBaseTest
from django.urls import reverse
import pytest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        # create the user and password in DB
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password
        )

        # User open the browser in login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User find the login form and the fiels to type
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # User type the username and passwords
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # The form is submited by user
        form.submit()

        # User see the message that is logged in
        self.assertIn(
            f'Your are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
