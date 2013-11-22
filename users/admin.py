from django.contrib import admin
from users.models import User, WallPost, Request
from django.forms import ModelForm

# Register your models here.

class CustomUserAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserAdminForm, self).__init__(*args, **kwargs)
        self.fields['achievements'].required = False

    class Meta:
         model = User

class UserAdmin(admin.ModelAdmin):
    form = CustomUserAdminForm
    list_display = ['first_name', 'last_name', 'email', 'friend_names', 'username']
    search_fields = ['first_name', 'last_name', 'email', 'username']

class PostAdmin(admin.ModelAdmin):
    list_display = ['message', 'poster', 'receiver']
    search_fields = ['message', 'poster', 'receiver']

class RequestAdmin(admin.ModelAdmin):
    list_display = ['requester', 'requestee']
    search_fields = ['requester', 'requestee']

admin.site.register(WallPost, PostAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Request, RequestAdmin)
