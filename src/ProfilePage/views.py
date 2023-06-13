import json
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect

from HomePage.models import LanguageMeta
from ProfilePage.models import UserProfile, UserEconomy

from authentication import validateSession

# Create your views here.
def index(request:HttpRequest):
    if validateSession(request):
        userProfile = UserProfile.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0]
        if userProfile.language_learning.count() == 0:
            return redirect('/customize/')
        userEco = UserEconomy.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0]
        username = userProfile.userMeta.username
        created_at = userProfile.userMeta.created_at

        # Calculating Time
        time_diff = timezone.now() - created_at

        days = time_diff.days
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds // 60) % 60

        if days > 0:
            time_str = f"{days} day{'s' if days > 1 else ''} ago"
        elif hours > 0:
            time_str = f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            time_str = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        
        native_language = ''
        language_learning_list = []

        for lan in userProfile.language_learning.all():
            language_learning_list.append(lan.name)
        
        if userProfile.native_language != None:
            native_language = userProfile.native_language
        else:
            native_language = ''

        return render(request, 'ProfilePage/index.html', {'username': username, 'created_at': time_str, 'bio': userProfile.bio, 'language_learning': language_learning_list, 'native_language': native_language, 'interests': userProfile.interests, 'coins':userEco.amount_of_coins, 'exp':userEco.amount_of_exp, 'last_language_used': userProfile.last_language_used})
    return redirect('/login/')

def updateProfileDetails(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        data = json.loads(request.body)
        try:
            userProfile = UserProfile.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0]
            userProfile.bio = data.get('bio')
            interests = data.get('interests', [])
            userProfile.interests = interests
            userProfile.save()
            return JsonResponse({'success': True})
        except Exception as e:
            print(str(e))
            return JsonResponse({'success': False})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/profile/')


# User language details button
def getUserLanguageDetails(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
        languages = LanguageMeta.objects.all()
        user_languages = UserProfile.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0].language_learning.all()
        context = {}
        for lan in languages:
            lan_dict = {}
            if user_languages.contains(lan):
                lan_dict['selected'] = True
            else:
                lan_dict['selected'] = False
            context[lan.name] = lan_dict
        return JsonResponse(context)
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/profile/')
    
# User Interests details button
def getInterestsDetails(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
        interests = ['travelling', 'reading', 'gaming']
        user_interests = UserProfile.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0].interests
        context = {}
        for inter in interests:
            inter_dict = {}
            if inter in user_interests:
                inter_dict['selected'] = True
            else:
                inter_dict['selected'] = False
            context[inter] = inter_dict
        return JsonResponse(context)
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/profile/')
