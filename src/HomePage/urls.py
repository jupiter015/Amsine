from django.urls import path
from . import views

app_name = "HomePage"

urlpatterns = [
    path('', views.index),
    path('logOut/', views.logOut, name='logOut'),
    path('checkIfUserProfileCustomized/', views.checkIfUserProfileCustomized, name='checkIfUserProfileCustomized'),
    path('loadChapters', views.loadChapters, name='loadChapters'),
    path('<str:language_name>/<str:chapter_type>/<int:chapterNum>/<int:lessonNum>', views.loadLessonGame, name='loadLessonGame'),
    path('loadNextQuestion/', views.loadNextQuestion, name='loadNextQuestion'),
    path('<str:language_name>/<str:chapter_type>/<int:chapterNum>/quiz', views.loadChapterQuiz, name='loadChapterQuiz'),
    path('loadNextQuizQuestion/', views.loadNextQuizQuestion, name='loadNextQuizQuestion'),
]