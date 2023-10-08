
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('host_authentication_system.urls')),
    path('quiz-management/', include('quiz_management.urls')),
    path('quiz-attempter-homepage/', include('quiz_attempter_management.urls')),
]
