from django.urls import path
from . import views

app_name = 'CommunityPage'

urlpatterns = [
    path('', views.index, name='index'),
    path('getThreads/', views.getThreads, name='getThreads'),
    path('addThread/', views.addThread, name='addThread'),
    path('getReplies/', views.getReplies, name='getReplies'),
    path('addReply/', views.addReply, name='addReply'),
    path('deleteThread/', views.deleteThread, name='deleteThread'),
    path('<str:thread_uuid>/', views.threadDetails, name='threadDetails'),
]