from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


class AuthorRegisterUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex.: Well'),
        ('last_name', 'Ex.: Jackson'),
        ('username', 'Ex.: yourusername0945'),
        ('email', 'Ex.: youremail@typed.here'),
        ('password', 'Type your password here'),
        ('password2', 'The password must be the same'),
    ])
    def test_first_name_placeholder_is_correct(self, field, expected_placeholder):
        form = RegisterForm()
        placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, expected_placeholder)
