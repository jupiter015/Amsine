from django.contrib import admin
from .models import UserMeta, LanguageMeta, UserProgress

# Register your models here.
admin.site.register(UserMeta)
admin.site.register(LanguageMeta)
admin.site.register(UserProgress)