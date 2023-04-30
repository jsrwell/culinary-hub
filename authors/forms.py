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
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.',
        ),
            code='invalid',
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

    # rewrite the form first_name
    first_name = forms.CharField(
        error_messages={'required': 'Your first name must not be empty'},
        label='First Name:',
    )

    # rewrite the form first_name
    last_name = forms.CharField(
        error_messages={'required': 'Your last name must not be empty'},
        label='Last Name:',
    )
    # rewrite the form username
    username = forms.CharField(
        error_messages={'required': 'This field must not be empty',
                        'min_length': 'Username must have at least 4 characters',  # noqa E501
                        'max_length': 'Username must have at maximum 150 characters',  # noqa E501
                        },
        min_length=4, max_length=150,
        label='Username:',
        help_text={
            'Username must have letters, number or @.+-_ only.',
            'The lenght should be between 4 and 150 characters.',
        })

    # rewrite the form e-mail
    email = forms.EmailField(
        error_messages={'required': 'Your e-mail must not be empty'},
        label='E-mail:',
        help_text='The e-mail must be valid'
    )

    # rewrite the form password
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password:',
        error_messages={
            'required': 'Password must not be empty',
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.',
        ),
        # strong password validator from def out class
        validators=[strong_password],
    )
    # create for password 2 for confirmation of password
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirm your password:',
        error_messages={
            'required': 'The password must be the same and not empty'
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

    # validation of the comparission of password and password 2
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'password and confirmation password must be equal',
                code='invalid',
            ),

            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
