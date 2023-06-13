from django.urls import path
from . import views

app_name = "ProfilePage"

urlpatterns = [
    path('', views.index, name='index'),
    path('updateProfileDetails/', views.updateProfileDetails, name='updateProfileDetails'),
    path('getUserLanguageDetails/', views.getUserLanguageDetails, name='getUserLanguageDetails'),
    path('getInterestsDetails/', views.getInterestsDetails, name='getInterestsDetails'),
]