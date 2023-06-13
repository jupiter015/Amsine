from django.urls import path
from . import views

app_name = 'CustomizePage'

urlpatterns = [
    path('', views.index, name='index'),
    path('addLanguageLearning/', views.addLanguageLearning, name='addLanguageLearning'),
    path('getNativeLanguagePage/', views.getNativeLanguagePage, name='getNativeLanguagePage'),
    path('addNativeLanguage/', views.addNativeLanguage, name='addNativeLanguage'),
    path('getInterestPage', views.getInterestPage, name='getInterestPage'),
    path('addInterest/', views.addInterest, name='addInterest'),
]