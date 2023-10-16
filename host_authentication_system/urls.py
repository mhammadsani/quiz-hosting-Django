from django.urls import path
from host_authentication_system import views


urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('sign-up/', views.sign_up, name="signup"),
    path('login/', views.user_login, name="login"),
    path('wait/', views.waitpage, name="waitpage"),
    path('profile/', views.profile, name="profile"),
    path('logout/', views.user_logout, name="logout"),
    path('change-password/', views.change_password, name="changepassword"),
]
