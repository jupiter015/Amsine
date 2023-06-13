import uuid
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from .models import UserAuthenticationMeta, SessionMeta
from authentication import validateSession

# Create your views here.
def index(request:HttpRequest):
    if validateSession(request):
        return redirect("/")
    return render(request, 'LoginPage/index.html')

def validateLogin(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        user = UserAuthenticationMeta.objects.filter(userMeta__username=request.POST.get("username"), password=request.POST.get("password"))
        if len(user) != 0:
            new_session_id = uuid.uuid4()
            new_session = SessionMeta(userMeta = user[0].userMeta, session_id = new_session_id)
            new_session.save()
            return JsonResponse({"validation":True, "user_id": user[0].userMeta.uuid, "session_id": new_session_id})
        return JsonResponse({"validation":False})

    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/login/')