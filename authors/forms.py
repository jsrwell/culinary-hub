from django import forms
from django.contrib.auth.models import User


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

        widgets = {
            'password': forms.PasswordInput(),
        }
