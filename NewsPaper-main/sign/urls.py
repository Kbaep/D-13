from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import upgrade_author, BaseRegisterView

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='sign/signup.html'),
         name='signup'),
    path('upgrade_author/', upgrade_author, name='upgrade_author'),
]