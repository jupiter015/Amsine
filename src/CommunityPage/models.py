from django.utils import timezone
import uuid
from django.db import models

from HomePage.models import LanguageMeta, UserMeta

# Create your models here.
class Threads(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    userMeta = models.ForeignKey(UserMeta, on_delete=models.CASCADE)
    languageMeta = models.ForeignKey(LanguageMeta, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.userMeta.username + " : " + self.title
    
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

class Replies(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    userMeta = models.ForeignKey(UserMeta, on_delete=models.CASCADE)
    parentThread = models.ForeignKey(Threads, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.userMeta.username + " : " + self.parentThread.userMeta.username
    
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