from django.shortcuts import render
from django.core.urlresolvers import reverse
from users.models import User, WallPost, Request
from django.views import generic
from django.template import RequestContext
from django.conf import settings
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.core.context_processors import csrf
from django.contrib.auth.views import login, logout_then_login
from django.contrib.auth import authenticate, login 
from django.shortcuts import redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from users.forms import SignUpForm, WallPostForm
from datetime import datetime
from django.utils.timezone import utc
from achievements.criteria import check_achievements, Achievement
import os.path

def base_view(request):
    return render_to_response('base.html',
                          locals(),
                          context_instance=RequestContext(request))

def search_user(request):
    if 'q' in request.POST and request.POST['q'] != '':
        query = request.POST['q']
        q_results = [u for u in User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))]
        if q_results:
            message = "Your search returned the following people: "
        else:
            message = "Your search returned no results"
    else:
        q_results = []
        message = 'Please put something in the query box.'
    c = {'message': message, 'results': q_results}
    return render(request, 'users/search_user.html', c)

def accept_or_decline(request, requester_id):
    if 'a' in request.POST:
        accepted = True
    elif 'd' in request.POST:
        accepted = False
    
    logged_in_user = User.objects.get(pk=request.user.id)
    requester = User.objects.get(pk=requester_id)

    if accepted:
        Request.objects.get(Q(requester=requester), Q(requestee=logged_in_user)).accept()
    else:
        Request.objects.get(Q(requester=requester), Q(requestee=logged_in_user)).decline()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    #redirect_to = "/" + str(request.user.id) + "/"
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

'''def sign_up(request):
    if request.method == 'POST': # If the form has been submitted...
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            User.objects.create_user(   username=username,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email)
            return render_to_response('users/login_page.html', {'state':"You have successfully created your user. You can now login"}) # Redirect after POST
    else:
        form = SignUpForm() # An unbound form

    return render(request, 'users/sign_up.html', {
        'form': form,
    })'''

def send_request(request, requestee_id):
    try:
        Request.objects.create(requester=request.user, requestee=User.objects.get(pk=requestee_id))
        request.user.achievements.add(Achievement.objects.get(title="Reaching out"))
    except ValidationError:
        # This should never happen because the user will not see the send-request button
        # unless he/she is not already friends with the person. But just in case.
        pass    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class IndexView(generic.ListView):
    model = User
    template_name = 'users/index.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)
    # Override the context if necessary
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        all_users = User.objects.all()
        first_100 = User.objects.all()[:100]
        all_posts = WallPost.objects.all()
        context['number_of_users'] = len(User.objects.all())
        context['all_users'] = all_users
        context['first_100'] = first_100
        context['all_posts'] = all_posts
        return context

class UserView(generic.DetailView):
    model = User
    template_name = 'users/user_profile.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserView, self).dispatch(*args, **kwargs)
    #   This method processes the post data.

    def post(self, request, *args , **kwargs):
        #context = self.get_context_data(**kwargs)
        now = datetime.utcnow().replace(tzinfo=utc)
        if request.method == 'POST':
            self.form = WallPostForm(request.POST)
            if self.form.is_valid():
                message = self.form.cleaned_data['message']
                WallPost.objects.create(message=message, poster=request.user, receiver=User.objects.get(pk=self.get_object().id), pub_date=now)
        else:
            self.form = WallPostForm()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        # Call base implementation to get a context
        context = super(UserView, self).get_context_data(**kwargs)
        context['all_wall_posts'] = WallPost.objects.filter(receiver=User.objects.get(pk=self.object.id))
        # Generate a list of mutual friends. Think this is ineficient.
        self.mutual_friends = []
        for f in self.object.friends.all():
            if f in User.objects.get(pk=self.request.user.id).friends.all():
                self.mutual_friends.append(f)
        context['friends'] = self.object.friends.all()
        context['mutual_friends'] = self.mutual_friends
        context['number_of_friends'] = len(self.object.friends.all())
        context['this_user'] = self.object
        context['friend_request_exists'] = Request.objects.filter(  requester=User.objects.get(pk=self.request.user.id),
                                                                    requestee=User.objects.get(pk=self.object.id)).exists()
        context['logged_in_user'] = self.request.user
        context['logged_in_as'] = self.request.user.get_full_name()

        self.form = WallPostForm()
        context['form'] = self.form
        
        return context

# Login method taken from http://solutoire.com/2009/02/26/django-series-1-a-custom-login-page/ for the most part.
def login(request):
    # Protect against CSRF attacks
    c = {}
    c.update(csrf(request))
    state = "Please log in below..."
    username = password = ''

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                check_achievements(user.id)
                return redirect('users:userview', user.id)
            else:
                state = "Your account is not active, please activate your account."
        else:
            state = "Your username and/or password were incorrect."
    return render_to_response('users/login_page.html', {'state':state, 'username': username}, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return render_to_response('users/logout_page.html')
