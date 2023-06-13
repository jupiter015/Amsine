from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('HomePage.urls')),
    path('login/', include('LoginPage.urls')),
    path('register/', include('RegisterPage.urls')),
    path('customize/', include('CustomizePage.urls')),
    path('profile/', include('ProfilePage.urls')),
    path('community/', include('CommunityPage.urls')),
    path('chat/', include('ChatPage.urls')),
    path('admin/', admin.site.urls),
]
