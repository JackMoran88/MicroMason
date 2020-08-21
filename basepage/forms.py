from django.forms import Form
from django.forms import EmailField, CharField, BooleanField
from django.forms import EmailInput, PasswordInput, CheckboxInput


class SingInForm(Form):
    email = EmailField(widget=EmailInput({
        'id': 'i_email',
        'type': 'email',
        'class': 'input-minimal'
    }))
    password = CharField(
        max_length=120,
        widget=PasswordInput({
            'id': 'i_pass',
            'type': 'password',
            'class': 'input-minimal'
        })
    )
    remember = BooleanField(
        widget=CheckboxInput({
            'id': 'i_remember',
            'type': 'checkbox',
            'class': 'input-minimal'
        }),
        required=False
    )
