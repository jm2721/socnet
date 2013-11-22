from tastypie.resources import ModelResource
from users.models import User


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
