from django.urls import path
from .views import LoginView, Logout, RegisterView

urlpatterns = [    
    path('auth/register/',
        RegisterView.as_view(), name='auth_register'),

    path('auth/login/',
         LoginView.as_view(), name='auth_login'),

    path('auth/logout/',Logout.as_view(), name='auth_logout'),
]