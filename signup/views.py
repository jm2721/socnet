# Create your views here.
from users.models import User
from signup.forms import SignUpForm, ConfirmationForm
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from signup import sendmail
from signup.models import ConfirmationCode
from django.core.context_processors import csrf
import hashlib
from django.contrib import messages

def sign_up(request):
    # Protect against CSRF attacks
    if request.method == 'POST': # If the form has been submitted...
        form = SignUpForm(request.POST)
        if form.is_valid():
            m1 = hashlib.sha512()
            m2 = hashlib.sha512()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            u = User.objects.create_user(username=username,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email
                                        )
            u.is_active = False
            u.save()
            code = sendmail.generate_code()
            m1.update(code)
            m2.update(username)
            ConfirmationCode.objects.create(code=m1.hexdigest(), uid=m2.hexdigest())
            sendmail.sendmail(email, code)
            return HttpResponseRedirect('/activate/') # Redirect after POST
    else:
        form = SignUpForm() # An unbound form

    return render(request, 'signup/sign_up.html', {
        'form': form,
    })

def activate(request):
    c = {}
    c.update(csrf(request))
    state = "Activate above"
    if request.method == 'POST':
        code = request.POST.get('code')
        username = request.POST.get('username')
        print code
        print username
        m1 = hashlib.sha512()
        m2 = hashlib.sha512()
        
        #code = form.cleaned_data['code']
        #uid = form.cleaned_data['uid']
        m1.update(code)
        m2.update(username)
        code_obj = ConfirmationCode.objects.filter(code=m1.hexdigest(), uid=m2.hexdigest())
        print code_obj
        if code_obj:
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()
            messages.success(request, "You have successfully activated account. You can now login")
            ConfirmationCode.objects.get(code=m1.hexdigest(), uid=m2.hexdigest()).delete()
            return HttpResponseRedirect("/")
        else:
            state = "That was incorrect"

    return render_to_response("signup/activate.html", {'state': state}, context_instance=RequestContext(request))

