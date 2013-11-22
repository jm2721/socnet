from datetime import datetime
from django.conf import settings
from users.models import Request, User

def default(request):

    # you can declare any variable that you would like and pass 
    # them as a dictionary to be added to each template's context like so:
    if request.user.is_anonymous():
        logged_in_as = 'Anon'
        request_set = ''
        achievements = ''
    else:
        logged_in_as = request.user
        request_set = Request.objects.filter(requestee=User.objects.get(pk=request.user.id))
        achievements = User.objects.get(pk=request.user.id).achievements.all()

    return dict(
        logged_in_as = logged_in_as,
        request_set = request_set,
        achievements = achievements
    )
