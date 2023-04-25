from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


class AuthorRegisterUnitTest(TestCase):
    # tests to placeholders in the inputs
    @parameterized.expand([
        ('first_name', 'Ex.: Well'),
        ('last_name', 'Ex.: Jackson'),
        ('username', 'Ex.: yourusername0945'),
        ('email', 'Ex.: youremail@typed.here'),
        ('password', 'Type your password here'),
        ('password2', 'The password must be the same'),
    ])
    def test_fields_placeholder_is_correct(self, field, expected_placeholder):
        form = RegisterForm()
        placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, expected_placeholder)

    # tests to help text in the inputs
    @parameterized.expand([
        ('first_name', ''),
        ('last_name', ''),
        ('username', (
            'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'  # noqa E501
        )),
        ('email', ''),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )),
        ('password2', ''),
    ])
    def test_fields_help_text_is_correct(self, field, expected_help_text):
        form = RegisterForm()
        help_text = form[field].field.help_text
        self.assertEqual(help_text, expected_help_text)

    # tests to labels in the inputs
    @parameterized.expand([
        ('first_name', 'First Name:'),
        ('last_name', 'Last Name:'),
        ('username', 'Username:'),
        ('email', 'E-mail:'),
        ('password', 'Password:'),
        ('password2', 'Confirm your password:'),
    ])
    def test_fields_label_is_correct(self, field, expected_label):
        form = RegisterForm()
        label = form[field].field.label
        self.assertEqual(label, expected_label)
