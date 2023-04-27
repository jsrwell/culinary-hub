# from django.test import TestCase
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


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
        ('email', 'The e-mail must be valid'),
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


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self):
        self.form_data = {
            'first_name': 'Testfirstname',
            'last_name': 'Testlastname',
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 't@st1ng',
            'password2': 't@st1ng',
        }
        return super().setUp()

    @parameterized.expand([
        ('first_name', 'Your first name must not be empty'),
        ('last_name', 'Your last name must not be empty'),
        ('username', 'This field must not be empty'),
        ('email', 'Your e-mail must not be empty'),
        ('password', 'Password must not be empty'),
        ('password2', 'The password must be the same and not empty'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
