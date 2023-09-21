
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('host_authentication_system.urls')),
    path('quiz_management/', include('quiz_management.urls')),
    path('quiz_attempter_homepage/', include('quiz_attempter_management.urls')),
]
