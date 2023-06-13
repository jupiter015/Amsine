import uuid

from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from CommunityPage.models import Replies, Threads
from HomePage.models import LanguageMeta, UserMeta
from ProfilePage.models import UserProfile

from authentication import validateSession

# Create your views here.
def index(request:HttpRequest):
    if validateSession(request):
        user = UserMeta.objects.filter(uuid=request.COOKIES.get('user_id'))[0]
        userProfile = UserProfile.objects.filter(userMeta=user)[0]
        if userProfile.language_learning.count() == 0:
            return redirect('/customize/')
        return render(request, 'CommunityPage/index.html', {'last_language_used': userProfile.last_language_used})
    else:
        return redirect('/login/')

#
# Get Threads AJAX
#
def getThreads(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        language = LanguageMeta.objects.filter(name=request.POST.get('language_name'))
        if len(language) != 0:
            threads = Threads.objects.filter(languageMeta=language[0]).order_by('-timestamp')
            if len(threads) != 0:
                threads_data = []

                for thread in threads:
                    number_of_replies = Replies.objects.filter(parentThread=thread).count()
                    thread_data = {
                        'uuid': thread.uuid,
                        'userMeta': thread.userMeta,
                        'title': thread.title,
                        'created_at': thread.getTimeBeen(),
                        'number_of_replies' : number_of_replies,
                    }
                    threads_data.append(thread_data)
                html = render_to_string('CommunityPage/threadsList.html', {'threadsList': threads_data})
                return JsonResponse({'html': html})
            return JsonResponse({'error_message': 'No Threads found.'})
        else:
            return JsonResponse({'error_message':'Something wrong occured'})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/community/')

#
# Add Thread AJAX
#
def addThread(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        new_thread = Threads(
            userMeta=UserMeta.objects.filter(uuid=request.COOKIES.get('user_id'))[0],
            languageMeta=LanguageMeta.objects.filter(name=request.POST.get('language_name'))[0],
            title=request.POST.get('title')
        )
        new_thread.save()
        return JsonResponse({})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/community/')
    
#
# Thread Details HTML
#
def threadDetails(request:HttpRequest, thread_uuid:str):
    if validateSession(request):
        thread = Threads.objects.filter(uuid=uuid.UUID(thread_uuid))
        if len(thread) != 0:
            ownsThread = False
            thread_data = {
                'uuid': thread[0].uuid,
                'language_name':thread[0].languageMeta.name,
                'userMeta': thread[0].userMeta,
                'title': thread[0].title,
                'created_at': thread[0].getTimeBeen(),
            }
            if str(thread[0].userMeta.uuid) == request.COOKIES.get('user_id'):
                ownsThread = True
            return render(request, 'CommunityPage/threadDetails.html', {'thread':thread_data, 'ownsThread': ownsThread})
        else:
            return render(request, 'CommunityPage/threadDetails.html', {'error': 'Thread like that was not found. :('})
    else:
        return redirect('/login/')

#
# Delete Thread AJAX
#
#
def deleteThread(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        thread = Threads.objects.filter(uuid=request.POST.get('thread_uuid'))
        if len(thread) != 0:
            if str(thread[0].userMeta.uuid) == request.COOKIES.get('user_id'):
                thread[0].delete()
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'error_message':'Something wrong occured'})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/community/')

# Get Replies AJAX
#
def getReplies(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        thread = Threads.objects.filter(uuid=request.GET.get('thread_uuid'))
        if len(thread) != 0:
            replies = Replies.objects.filter(parentThread=thread[0])
            if len(replies) != 0:
                replies_data = []

                for reply in replies:
                    reply_data = {
                        'uuid': reply.uuid,
                        'userMeta': reply.userMeta,
                        'message': reply.message,
                        'created_at': reply.getTimeBeen(),
                    }
                    replies_data.append(reply_data)
                html = render_to_string('CommunityPage/repliesList.html', {'repliesList': replies_data})
                return JsonResponse({'html': html})
            return JsonResponse({'error_message': 'No Replies found.'})
        else:
            return JsonResponse({'error_message':'Something wrong occured'})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/community/')

def addReply(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        new_reply = Replies(
            userMeta=UserMeta.objects.filter(uuid=request.COOKIES.get('user_id'))[0],
            parentThread = Threads.objects.filter(uuid=request.POST.get('thread_uuid'))[0],
            message=request.POST.get('reply')
        )
        new_reply.save()
        return JsonResponse({})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/community/')