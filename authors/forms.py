from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

# função validadora de senha forte


def strong_password(password):
    regex = re.compile(r'^(?=.[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.',
            code='Invalid',
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fields variebles
        f_first_name = self.fields['first_name']
        f_last_name = self.fields['last_name']
        f_username = self.fields['username']
        f_email = self.fields['email']
        f_password = self.fields['password']
        f_password2 = self.fields['password2']
        # placeholders input
        add_placeholder(f_first_name, 'Ex.: Well')
        add_placeholder(f_last_name, 'Ex.: Jackson')
        add_placeholder(f_username, 'Ex.: yourusername0945')
        add_placeholder(f_email, 'Ex.: youremail@typed.here')
        add_placeholder(f_password, 'Type your password here')
        add_placeholder(f_password2, 'The password must be the same')

    # rewrite the form password
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Password:',
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        # strong password validator from def out class
        validators=[strong_password]
    )
    # create for password 2 for confirmation of password
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Confirm your password:',
        error_messages={
            'required': "The password don't match"
        },
    )

    # meta to call the inputs from django
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels = {
            'first_name': 'First Name:',
            'last_name': 'Last Name:',
            'username': 'Username:',
            'email': 'E-mail:',
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }

    # validation of the comparission of password and password 2
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError({
                'password': 'The password dont match with the confirmation!',
                'password2': 'The confirmation password dont match!',
            })
