from django.contrib import admin
from .models import UserAuthenticationMeta, SessionMeta

# Register your models here.
admin.site.register(UserAuthenticationMeta)
admin.site.register(SessionMeta)