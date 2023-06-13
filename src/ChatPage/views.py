from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.db.models import Q, Count
from HomePage.models import LanguageMeta, UserMeta

from ProfilePage.models import UserProfile
from .models import ChatMeta, ChatMessages

# check if user is linked with someone AJAX
def checkIfLinked(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        chatMeta = ChatMeta.objects.filter(Q(userMeta1__uuid=request.COOKIES.get('user_id')) | Q(userMeta2__uuid=request.COOKIES.get('user_id')), active=True)
        if len(chatMeta) != 0:
            return JsonResponse({'isLinked': True})
        else:
            return JsonResponse({'isLinked': False})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/')

def linkUser(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        chatMeta = ChatMeta.objects.filter(Q(userMeta1__uuid=request.COOKIES.get('user_id')) | Q(userMeta2__uuid=request.COOKIES.get('user_id')), active=True)
        if len(chatMeta) != 0:
            chatMeta[0].active = False
            chatMeta[0].save()
        else:
            client = UserProfile.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0]
            interests = list(client.interests)
            users = UserProfile.objects.filter(native_language=client.language_learning.all()[0], language_learning=client.native_language).annotate(num_common_interests=Count('interests', filter=Q(interests__in=interests))).order_by('-num_common_interests')
            success = False
            for user in users:
                userAlreadyLinked = ChatMeta.objects.filter(Q(userMeta1__uuid=user.userMeta.uuid) | Q(userMeta2__uuid=user.userMeta.uuid), active=True)
                if len(userAlreadyLinked) != 0:
                    continue
                newChatMeta = ChatMeta(userMeta1=client.userMeta, userMeta2=user.userMeta, active=True)
                newChatMeta.save()
                success = True
                break
            return JsonResponse({'success': success})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/')

def getChats(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        chatMeta = ChatMeta.objects.filter(Q(userMeta1__uuid=request.COOKIES.get('user_id')) | Q(userMeta2__uuid=request.COOKIES.get('user_id')), active=True)[0]
        other_user = None
        if str(chatMeta.userMeta1.uuid) == request.COOKIES.get('user_id'):
            other_user = chatMeta.userMeta2
        else:
            other_user = chatMeta.userMeta1
        chatMessages = None
        cm = []
        for c in ChatMessages.objects.filter(chatMeta=chatMeta):
            cm.append({'isUser': str(c.sender.uuid) == request.COOKIES.get('user_id'), 
                       'sender': c.sender, 
                       'message': c.message, 
                       'created_at': c.getTimeBeen()})
        if len(cm) != 0:
            chatMessages = cm
        html = render_to_string('ChatPage/chats.html', {'other_user': other_user, 'chatMessages': chatMessages})
        return JsonResponse({'html': html})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/')

def sendMessage(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        chatMeta = ChatMeta.objects.filter(Q(userMeta1__uuid=request.COOKIES.get('user_id')) | Q(userMeta2__uuid=request.COOKIES.get('user_id')), active=True)[0]
        message = ChatMessages(chatMeta=chatMeta, sender=UserMeta.objects.filter(uuid=request.COOKIES.get('user_id'))[0], message=request.POST.get('message'))
        message.save()
        return JsonResponse({})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/')