# urls.py
from django.urls import path
from .views import register, user_login, user_logout
from home.views import home

urlpatterns = [
    # ... other URL patterns ...
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('home/', home, name='home'),
    path('logout/', user_logout, name='logout')
]
