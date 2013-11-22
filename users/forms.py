from django.forms import ModelForm
from users.models import User, WallPost

class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']

class WallPostForm(ModelForm):
    class Meta:
        model = WallPost
        fields = ['message']
    