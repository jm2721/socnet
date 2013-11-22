# Create your views here.
from likes.models import Like
from users.models import User, WallPost
from django.http import HttpResponseRedirect


def add_like(request, postid, userid):
    obj, is_new = Like.objects.get_or_create(   linked_to=WallPost.objects.get(pk=postid), 
                                                liked_by=User.objects.get(pk=userid))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))