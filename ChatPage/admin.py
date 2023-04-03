from django.contrib import admin
from .models import ChatMeta, ChatMessages

# Register your models here.
admin.site.register(ChatMeta)
admin.site.register(ChatMessages)