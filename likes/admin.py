from likes.models import Like
from django.contrib import admin

class LikeAdmin(admin.ModelAdmin):
    list_display = ['linked_to', 'liked_by']
    search_fields = ['linked_to', 'liked_by']

admin.site.register(Like, LikeAdmin)