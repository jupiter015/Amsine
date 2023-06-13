import uuid
from django.db import models

# Create your models here.
class WaitingAuthentication(models.Model):
    username = models.CharField(max_length=8, unique=True)
    session_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email_id = models.EmailField()
    password = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)
    auth_code = models.CharField(max_length=5, editable=False)

    def __str__(self):
        return self.username