from users.models import User
from django.forms import ModelForm
from signup.models import ConfirmationCode

class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']

class ConfirmationForm(ModelForm):
    class Meta:
        model = ConfirmationCode
        fields = ['code', 'uid']