from django.contrib import admin
from achievements.models import Achievement

class AchievementAdmin(admin.ModelAdmin):
    list_display = ['description']
    search_fields = ['description']

admin.site.register(Achievement, AchievementAdmin)