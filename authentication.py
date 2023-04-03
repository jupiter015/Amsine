from django.utils import timezone
from django.http import HttpRequest
from LoginPage.models import SessionMeta

def validateSession(request:HttpRequest):
    if request.COOKIES.get("user_id") == None or request.COOKIES.get("session_id") == None:
        # print("Cookies does not exist")
        return False

    session = SessionMeta.objects.filter(userMeta__uuid=request.COOKIES.get("user_id"), session_id=request.COOKIES.get("session_id"))
    if len(session) != 0:
        time_diff = timezone.now() - session[0].timestamp
        # print(time_diff.total_seconds()/60)
        if time_diff.total_seconds()/60 < 15:
            return True
        session[0].delete()
        for ses in SessionMeta.objects.filter(userMeta__uuid=request.COOKIES.get("user_id")):
            ses.delete()
        return False
    # print("No data matching like this in database")
    return False