from django.db import models
from django.utils import timezone
from HomePage.models import UserMeta

class ChatMeta(models.Model):
    userMeta1 = models.ForeignKey(UserMeta, on_delete=models.CASCADE, related_name='chatmeta_usermeta1')
    userMeta2 = models.ForeignKey(UserMeta, on_delete=models.CASCADE, related_name='chatmeta_usermeta2')
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.userMeta1.username + " : " + self.userMeta2.username + " : " + str(self.active)

class ChatMessages(models.Model):
    chatMeta = models.ForeignKey(ChatMeta, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserMeta, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.CharField(max_length=200, null=False, blank=False, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.sender.username + " | " + self.chatMeta.userMeta1.username + " : " + self.chatMeta.userMeta2.username

    def getTimeBeen(self) -> str:
        time_diff = timezone.now() - self.timestamp
        time_str = ''
        days = time_diff.days
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds // 60) % 60

        if days > 0:
            time_str = f"{days} day{'s' if days > 1 else ''} ago"
        elif hours > 0:
            time_str = f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            time_str = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        
        return time_str