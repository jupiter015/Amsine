import uuid
from django.db import models
from HomePage.models import UserMeta


# Create your models here.
class UserAuthenticationMeta(models.Model):
    userMeta = models.ForeignKey(UserMeta, on_delete=models.CASCADE)
    password = models.CharField(max_length=15)

    def __str__(self):
        return self.userMeta.username

class SessionMeta(models.Model):
    userMeta = models.ForeignKey(UserMeta, on_delete=models.CASCADE)
    # user_id = models.UUIDField()
    session_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.userMeta.username