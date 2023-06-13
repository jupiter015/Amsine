from smtplib import SMTPRecipientsRefused
import uuid, random, string

from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from amsine.settings import EMAIL_HOST_USER

from authentication import validateSession

from HomePage.models import UserMeta
from LoginPage.models import UserAuthenticationMeta, SessionMeta
from RegisterPage.models import WaitingAuthentication
from ProfilePage.models import UserProfile, UserEconomy

#
# /register/ page VIEW
#
def index(request):
    if validateSession(request):
        return redirect('/')
    else:
        return render(request, 'RegisterPage/index.html')

# Check if username is taken AJAX
def usernameCheck(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        users = UserMeta.objects.filter(username=request.POST.get("username"))
        if len(users) == 0:
            return JsonResponse({'available': True})
        return JsonResponse({'available': False})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/register/')

#Check if Email is already used AJAX
def checkEmailUsed(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        users = UserMeta.objects.filter(email_id=request.POST.get("email_id"))
        if len(users) == 0:
            return JsonResponse({'available': True})
        return JsonResponse({'available': False})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/register/')

# Things to do when register button is clicked AJAX
def registerButton(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        
        #Checking if email or username is taken
        if len(UserMeta.objects.filter(username=request.GET.get('username'))) != 0 or len(UserMeta.objects.filter(email_id=request.GET.get('email_id'))):
            return JsonResponse({'success':False, 'message':'Username or Email is already taken.'})

        # Creating Data
        session_id = uuid.uuid4()
        auth_code = generateAuthCode()
        message = "Your Auth Code is: " + auth_code

        # Sending mail
        try:
            # Send Mail
            send_mail(subject="Verify Your Account", message=message, from_email=EMAIL_HOST_USER, recipient_list=[request.GET.get('email_id')], fail_silently=False)

            # Generating Entry
            user_waiting = WaitingAuthentication(username=request.GET.get('username'), email_id=request.GET.get('email_id'), password=request.GET.get('password'), session_id=session_id, auth_code=auth_code)

            # Save Entry
            user_waiting.save()
        # If reciepent email is wrong 
        except SMTPRecipientsRefused:
            return JsonResponse({'success':False, 'message':'Wrong Email Address?'})
        # If some other error occured
        except Exception as e:
            return JsonResponse({'success':False, 'message':'Something went wrong..'})
        # If everything went well :thumbs_up:
        return JsonResponse({'success':True, 'session_id':session_id})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/register/')

#
# /register/verify page VIEW   
#
def email_verification_page(request:HttpRequest):
    # Validating if reached this far
    user_waiting = WaitingAuthentication.objects.filter(session_id=request.COOKIES.get('session_id'))
    if len(user_waiting) != 0:
        time_diff = timezone.now() - user_waiting[0].timestamp
        # Checking if time did NOT expire
        if time_diff.total_seconds()/60 < 1:
            return render(request, 'RegisterPage/email_verification.html')
        for user in WaitingAuthentication.objects.filter(email_id=user_waiting[0].email_id):
            user.delete()
        return redirect('/register/')
    return redirect('/register/')

# Check Auth Code AJAX
def check_auth_code(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        user_waiting = WaitingAuthentication.objects.filter(session_id=request.COOKIES.get('session_id'), auth_code=request.GET.get('auth_code'))
        if len(user_waiting) != 0:
            user = UserMeta(role='user', username=user_waiting[0].username, email_id=user_waiting[0].email_id)
            userAuthentication = UserAuthenticationMeta(userMeta=user, password=user_waiting[0].password)
            session_id = uuid.uuid4()
            sessionMeta = SessionMeta(userMeta=user, session_id=session_id)
            userProfile = UserProfile(userMeta=user)
            userEconomy = UserEconomy(userMeta=user)

            # Saving Entries
            user.save()
            userAuthentication.save()
            sessionMeta.save()
            userProfile.save()
            userEconomy.save()

            # Getting rid of entries from WaitingAuthentication
            for userInWaiting in WaitingAuthentication.objects.filter(email_id=user_waiting[0].email_id):
                userInWaiting.delete()
            
            return JsonResponse({'success':True, 'session_id':session_id, 'user_id':user.uuid})
        return JsonResponse({'success':False})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/register/')

def generateAuthCode():
    return ''.join(random.choices(string.ascii_letters, k=5)).upper()