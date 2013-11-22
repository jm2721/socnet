from django import template
from users.models import User, WallPost
from likes.models import Like

register = template.Library()

def likes(user, wallpost):
    if not isinstance(user, User):
        return_value = ''
    if not isinstance(wallpost, WallPost):
        return_value = ''
    else:
        return_value = Like.objects.filter(linked_to=wallpost, liked_by=user).exists()
    return return_value
register.filter('likes', likes)
