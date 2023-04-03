from django.urls import path
from . import views

app_name = 'ChatPage'

urlpatterns = [
    path('checkIfLinked/', views.checkIfLinked, name='checkIfLinked'),
    path('linkUser/', views.linkUser, name='linkUser'),
    path('getChats/', views.getChats, name='getChats'),
    path('sendMessage/', views.sendMessage, name='sendMessage'),
]