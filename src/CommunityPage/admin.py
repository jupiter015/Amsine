from django.contrib import admin
from .models import Threads, Replies 

# Register your models here.
admin.site.register(Threads)
admin.site.register(Replies)