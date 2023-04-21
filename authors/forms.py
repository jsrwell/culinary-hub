from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Ex.: Well')
        add_placeholder(self.fields['last_name'], 'Ex.: Jackson')
        add_placeholder(self.fields['username'], 'Ex.: yourusername0945')
        add_placeholder(self.fields['email'], 'Ex.: youremail@typed.here')
        add_placeholder(self.fields['password'], 'Type your password here')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput({
            "placeholder": "Your password must be the same"
        }),
        label='Confirm your password:',
        error_messages={
            'required': "The password don't match"
        },
    )

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
            'password': 'Password:',
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }

        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        if 'Teste' in data:
            raise ValidationError(
                'O nome %(inv)s é invalido!',
                code='invalid',
                params={'inv': '"Teste"'},
            )
        return data
